"""Constrói `assets/layers.json` — o manifesto de camadas exigido pelo compositor.

Restrições reais do compositor (`studio.py render`), descobertas na verificação:

1. Ele escala CADA camada para `1920*scale x 1080*scale`, ou seja **força a proporção do canvas**.
   Um asset 4:3 entregue cru sai esticado. Solução: pré-renderizar cada camada num quadro de
   proporção 16:9, e então `scale` só define o tamanho, sem distorção.
2. `scale` e `zoom_end` precisam estar em [0.1, 3]. Escalar um GIF pequeno até cobrir o quadro
   exigiria escala 5+ e seria recusado.
3. Camada `video` precisa ter duração >= duração da cena (não há laço silencioso). GIF animado de
   2 s não entra cru — vira clipe de 60 s.
4. A camada de frente precisa de **transparência real** para o fundo aparecer. VP9 com alpha
   perdeu o canal nesta instalação (verificado); **qtrle/argb preserva** (verificado: alpha 0–255).

Camada 1 (fundo): asset coberto e recortado para 1920x1080, `scale=1.0`.
Camada 2 (frente): asset contido em quadro 960x540 com padding transparente, `scale=0.5`.

Geometria determinística pelo índice da cena: duas execuções produzem o mesmo manifesto.

Uso:
    python science-studio/build_layers.py <projeto> [--skip-encode] [--only N]

REGRA DE CONTEXTO (trava visual): cada cena só recebe assets cujos nomes citam o
contexto do roteiro (narração/visual/sd_prompt, via context_gate). Cena sem nenhum
asset em contexto BLOQUEIA a execução (exit 2) — nunca mais é atribuído um asset
arbitrário fora de contexto.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import context_gate

CANVAS = (1920, 1080)
FG_FRAME = (960, 540)
FG_SCALE = round(FG_FRAME[0] / CANVAS[0], 4)  # 0.5
CLIP_SECONDS = 60


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, capture_output=True, text=True)


def probe(path: Path) -> dict:
    out = run(['ffprobe', '-v', 'error', '-show_entries',
               'stream=width,height,codec_type,pix_fmt,duration',
               '-show_entries', 'format=duration', '-of', 'json', str(path)])
    try:
        return json.loads(out.stdout or '{}')
    except json.JSONDecodeError:
        return {}


def meta(path: Path) -> tuple[int, int, float]:
    info = probe(path)
    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'video':
            duration = float(stream.get('duration') or info.get('format', {}).get('duration') or 0)
            return int(stream.get('width') or 0), int(stream.get('height') or 0), duration
    return 0, 0, 0.0


def gif_cadence(source: Path, workdir: Path) -> tuple[Path, float]:
    """Extrai os quadros do GIF e devolve a máscara de sequência + a cadência original.

    Por que não usar `-stream_loop` nem `-ignore_loop` direto no GIF: verificado nesta instalação,
    o metadado do GIF mente (reporta 1 quadro a 100 fps) e o loop do demuxer não produz os 60 s —
    os clipes saíam com a duração de um único play (4 s, 8 s, 36 s). Extrair os quadros e tratar
    como sequência image2 com `-loop 1` é determinístico: produz exatamente a duração pedida.
    """
    frames_dir = workdir / source.stem
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob('f_*.png'):
        old.unlink()
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), str(frames_dir / 'f_%04d.png')])
    count = len(list(frames_dir.glob('f_*.png')))
    if count == 0:
        raise ValueError(f'gif_sem_quadros: {source.name}')

    out = run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries',
               'frame=duration', '-of', 'json', str(source)])
    try:
        durations = [float(f['duration']) for f in json.loads(out.stdout or '{}').get('frames', [])
                     if f.get('duration')]
    except (ValueError, TypeError, json.JSONDecodeError):
        durations = []
    total = sum(durations)
    # Preserva a cadência real quando o metadado é confiável; senão usa 12 fps (típico de GIF).
    fps = count / total if total > 0.2 and count > 1 else 12.0
    return frames_dir / 'f_%04d.png', max(4.0, min(30.0, fps))


def source_args(source: Path, workdir: Path) -> list[str]:
    """Argumentos de entrada ffmpeg que produzem fluxo contínuo e loopável."""
    if source.suffix.lower() == '.gif':
        pattern, fps = gif_cadence(source, workdir)
        return ['-loop', '1', '-framerate', f'{fps:.4f}', '-i', str(pattern)]
    return ['-loop', '1', '-framerate', '24', '-i', str(source)]


def border_luma(source: Path) -> float:
    """Luminância média da borda do asset.

    Decide se o fundo branco do diagrama deve virar transparência. Sem PIL, assume borda clara
    (o caso mais comum em diagrama científico) e aplica a chave — errar para transparente é
    visualmente melhor que entregar um painel branco chapado.
    """
    try:
        from PIL import Image
    except ImportError:
        return 255.0
    tmp = Path(tempfile.gettempdir()) / f'assetguard-border-{source.stem}.png'
    if run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-frames:v', '1',
            str(tmp)]).returncode != 0 or not tmp.is_file():
        return 255.0
    try:
        image = Image.open(tmp).convert('L')
    except OSError:
        return 255.0
    width, height = image.size
    band = max(2, min(width, height) // 40)
    samples = []
    for x in range(width):
        for y in (*range(band), *range(height - band, height)):
            samples.append(image.getpixel((x, y)))
    for y in range(height):
        for x in (*range(band), *range(width - band, width)):
            samples.append(image.getpixel((x, y)))
    return sum(samples) / len(samples) if samples else 255.0


def encode_cover(source: Path, target: Path, workdir: Path, seconds: int = CLIP_SECONDS) -> bool:
    """Fundo: cobre 1920x1080 e recorta o excesso. Nunca distorce, nunca deixa barra."""
    _, _, existing = meta(target)
    if target.is_file() and existing >= seconds - 0.5:
        return True
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        source_kind = source_args(source, workdir)
    except ValueError as error:
        print(f'  fundo FALHOU {source.name}: {error}', file=sys.stderr)
        return False
    # O fundo é BACKDROP, não ilustração: escurecido, dessaturado e desfocado para não competir
    # com o diagrama da frente. Sem isto o asset colorido aparece ampliado e borrado, o que
    # destrói a leitura documental (defeito observado no primeiro render de sondagem).
    result = run(['ffmpeg', '-v', 'error', '-y', *source_kind, '-t', str(seconds), '-an', '-sn',
                  '-vf', f'scale={CANVAS[0]}:{CANVAS[1]}:force_original_aspect_ratio=increase,'
                         f'crop={CANVAS[0]}:{CANVAS[1]},gblur=sigma=18,'
                         f'eq=brightness=-0.34:contrast=1.06:saturation=0.45,format=yuv420p',
                  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-r', '24',
                  '-movflags', '+faststart', str(target)])
    if result.returncode != 0:
        print(f'  fundo FALHOU {source.name}: {result.stderr.strip()[:150]}', file=sys.stderr)
        return False
    return True


def encode_alpha(source: Path, target: Path, workdir: Path, seconds: int = CLIP_SECONDS) -> bool:
    """Frente: asset contido em quadro 16:9 com padding TRANSPARENTE, em qtrle/argb.

    O padding transparente é o que permite o fundo aparecer por trás do asset.
    """
    _, _, existing = meta(target)
    if target.is_file() and existing >= seconds - 0.5:
        return True
    target.parent.mkdir(parents=True, exist_ok=True)
    width, height = FG_FRAME
    try:
        source_kind = source_args(source, workdir)
    except ValueError as error:
        print(f'  frente FALHOU {source.name}: {error}', file=sys.stderr)
        return False
    # Diagramas científicos costumam vir com fundo BRANCO. Colocado sobre o backdrop, isso vira um
    # painel branco chapado (defeito observado). Quando a borda do asset é clara, o branco é
    # chaveado para transparente e o desenho flutua sobre o fundo.
    key = ''
    if border_luma(source) > 170:
        key = 'colorkey=0xFFFFFF:similarity=0.14:blend=0.10,'
    result = run(['ffmpeg', '-v', 'error', '-y', *source_kind, '-t', str(seconds), '-an', '-sn',
                  # Caixa explícita nas DUAS dimensões: com altura automática (-2) o escalador
                  # pode devolver imagem maior que o quadro de padding e o `pad` recusa.
                  '-vf', f'scale={width - 80}:{height - 80}:force_original_aspect_ratio=decrease,'
                         f'{key}format=rgba,'
                         f'eq=brightness=-0.04:saturation=0.92,'
                         f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=#00000000',
                  '-c:v', 'qtrle', '-pix_fmt', 'argb', '-r', '24', str(target)])
    if result.returncode != 0:
        print(f'  frente FALHOU {source.name}: {result.stderr.strip()[:150]}', file=sys.stderr)
        return False
    # O alpha tem de existir de fato: verificado, não presumido.
    info = probe(target)
    pix = next((s.get('pix_fmt') for s in info.get('streams', []) if s.get('codec_type') == 'video'), '')
    if pix != 'argb':
        print(f'  frente SEM ALPHA {source.name}: pix_fmt={pix}', file=sys.stderr)
        return False
    return True


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Gera assets/layers.json')
    parser.add_argument('project_dir', type=Path)
    parser.add_argument('--skip-encode', action='store_true')
    parser.add_argument('--only', type=int, help='processa apenas a cena N (diagnóstico)')
    args = parser.parse_args(argv)

    root: Path = args.project_dir
    project = json.loads((root / 'project.json').read_text(encoding='utf-8'))
    scenes = project['scenes']

    candidates = sorted(
        p for p in (root / 'assets' / 'candidates').rglob('*')
        if p.is_file() and p.suffix.lower() in ('.gif', '.png', '.jpg', '.jpeg', '.webp', '.bmp')
    )
    if not candidates:
        print('build_layers: nenhum asset em assets/candidates', file=sys.stderr)
        return 1

    index = []
    for path in candidates:
        width, height, duration = meta(path)
        if not width or not height:
            print(f'  ignorado (ilegível): {path.name}', file=sys.stderr)
            continue
        index.append({'path': path, 'tokens': context_gate.asset_name_tokens(path.stem),
                      'width': width, 'height': height})
    print(f'assets legíveis: {len(index)} de {len(candidates)}')

    if not args.skip_encode:
        # Fundos para todos (clipes pequenos e rápidos). A frente com alpha é codificada sob
        # demanda no laço: só ~21 dos 38 assets são escolhidos como frente, e qtrle é pesado.
        workdir = root / 'assets' / '_gifframes'
        print('pré-processando fundos:')
        ok_bg = sum(
            1 for item in index
            if encode_cover(item['path'], root / 'assets' / 'bg' / f"{item['path'].stem}.mp4",
                            workdir)
        )
        print(f'  fundos prontos: {ok_bg}/{len(index)}')
        print('frentes com alpha: codificadas sob demanda')

    topic = str(project.get('topic', ''))
    # Passada 1 (pura): seleção com a trava de contexto. Falha ANTES de codificar qualquer coisa.
    escolhas: dict[int, tuple[dict, dict, int]] = {}
    violacoes: list[str] = []
    for position, scene in enumerate(scenes):
        if args.only is not None and position != args.only:
            continue
        try:
            escolhas[position] = context_gate.select_scene_assets(index, scene, topic)
        except context_gate.OffContextError as error:
            violacoes.append(f'cena {position}: {error}')
    if violacoes:
        print('build_layers: PROIBIDO frame fora do contexto — cenas bloqueadas:', file=sys.stderr)
        for violation in violacoes:
            print(f'  {violation}', file=sys.stderr)
        print('  → adquira/curadoria assets EM CONTEXTO para essas cenas; não existe bypass.',
              file=sys.stderr)
        return 2

    scenes_map: dict[str, list[dict]] = {}
    relatorio = []
    for position, scene in enumerate(scenes):
        if args.only is not None and position != args.only:
            continue
        foreground, background, match_score = escolhas[position]

        bg_clip = root / 'assets' / 'bg' / f"{background['path'].stem}.mp4"
        fg_clip = root / 'assets' / 'fg' / f"{foreground['path'].stem}.mov"
        workdir = root / 'assets' / '_gifframes'
        if not bg_clip.is_file():
            if args.skip_encode or not encode_cover(background['path'], bg_clip, workdir):
                print(f'cena {position}: clipe de fundo ausente ({bg_clip.name})', file=sys.stderr)
                return 2
        # Reencoda se o clipe existir mas estiver curto ou ilegível (clipe truncado de execução
        # anterior falhada não pode passar por válido).
        if not (meta(bg_clip)[2] >= CLIP_SECONDS - 0.5):
            if args.skip_encode or not encode_cover(background['path'], bg_clip, workdir):
                print(f'cena {position}: clipe de fundo inválido ({bg_clip.name})', file=sys.stderr)
                return 2
        if not (meta(fg_clip)[2] >= CLIP_SECONDS - 0.5):
            if args.skip_encode or not encode_alpha(foreground['path'], fg_clip, workdir):
                print(f'cena {position}: clipe de frente inválido ({fg_clip.name})',
                      file=sys.stderr)
                return 2

        fg_x = round((CANVAS[0] - FG_FRAME[0] * 1.0) / 2)   # 480
        fg_y = round((CANVAS[1] - FG_FRAME[1] * 1.0) / 2)   # 270
        drift_x = 20 if position % 3 else -16
        drift_y = 10 if position % 2 else -8

        scenes_map[str(position)] = [
            {   # fundo: preenche o quadro, zoom lento para haver movimento
                'path': rel(bg_clip, root),
                'kind': 'video',
                'scale': 1.0,
                'zoom_end': 1.04,
                'x0': 0, 'y0': 0, 'x1': 0, 'y1': 0,
                'blur': 0,
            },
            {   # frente: o fenômeno da cena, com transparência real, em deriva lenta
                'path': rel(fg_clip, root),
                'kind': 'video',
                'scale': FG_SCALE,
                'zoom_end': round(FG_SCALE * 1.07, 4),
                'x0': fg_x, 'y0': fg_y, 'x1': fg_x + drift_x, 'y1': fg_y + drift_y,
                'blur': 0,
            },
        ]
        relatorio.append({'scene': position, 'background': background['path'].name,
                          'foreground': foreground['path'].name, 'match_score': match_score})

    target = root / 'assets' / 'layers.json'
    if args.only is None:
        manifest = {
            'canvas': list(CANVAS),
            'clip_seconds': CLIP_SECONDS,
            'scenes': scenes_map,
            'report': {
                'scenes': len(scenes_map),
                'distinct_foregrounds': len({i['foreground'] for i in relatorio}),
                'distinct_backgrounds': len({i['background'] for i in relatorio}),
                'scenes_without_keyword_match': sum(1 for i in relatorio if i['match_score'] == 0),
            },
        }
        target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        print()
        print(f"cenas: {manifest['report']['scenes']}")
        print(f"frentes distintas: {manifest['report']['distinct_foregrounds']}")
        print(f"fundos distintos: {manifest['report']['distinct_backgrounds']}")
        print(f"cenas sem casamento por palavra-chave: {manifest['report']['scenes_without_keyword_match']}")
        print(f'manifesto: {target}')
    else:
        print(json.dumps(scenes_map, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
