"""Science Studio AI v0.2: local, resumable motion-comic playbook (stdlib + FFmpeg)."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from context_gate import gate_visual_context  # noqa: E402
from ptbr_pronunciation import normalize_for_speech  # noqa: E402

PROFILES = {
    'short': (60, 1080, 1920), 'youtube': (600, 1920, 1080),
    'documentary': (3600, 1920, 1080), 'full-documentary': (5400, 1920, 1080),
}
STAGES = ('research', 'script', 'assets', 'voice')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def run(argv, cwd=None):
    result = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=7200)
    if result.returncode:
        # Provider output can contain credentials; never persist or echo it.
        raise ValueError(f'command_failed: {Path(argv[0]).name}; exit={result.returncode}')
    return result.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', str(path)]))


def asset(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'asset_missing_or_outside_project: {value}')
    if "'" in str(path) or '\n' in str(path):
        raise ValueError('unsupported_quote_in_asset_path')
    return path


def number(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError('invalid_numeric_parameter')
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError('numeric_parameter_out_of_range')
    return value


def validate(project, root, media=True):
    if project.get('version') != '0.2' or project.get('language') != 'pt-BR':
        raise ValueError('project_version_or_language')
    if project.get('profile') not in PROFILES:
        raise ValueError('invalid_profile')
    if project.get('speech_balloons') is not False:
        raise ValueError('speech_balloons_must_be_false')
    width, height = project['size']
    for value in (width, height):
        number(value, 64, 4096)
        if not isinstance(value, int) or value % 2:
            raise ValueError('size_must_be_even_integers')
    number(project['fps'], 12, 60)
    number(project['duration'], 1, 6600)
    if not project.get('topic', '').strip():
        raise ValueError('topic_required')
    scenes = project.get('scenes', [])
    if not scenes:
        raise ValueError('script_missing: run configured script provider or author scenes')
    evidence = {item['id'] for item in project.get('sources', [])
                if item.get('url') and item.get('accessed') and item.get('excerpt')}
    total = 0
    for index, scene in enumerate(scenes):
        duration = number(scene['duration'], 1, 60)
        total += duration
        if not scene.get('narration', '').strip() or not scene.get('visual', '').strip():
            raise ValueError(f'scene_{index}: narration_and_visual_required')
        if not scene.get('claims') or any(c not in evidence for c in scene['claims']):
            raise ValueError(f'scene_{index}: scientific_evidence_missing')
        if scene.get('transition', 'cut') not in ('cut', 'fade'):
            raise ValueError('unsupported_transition')
        layers = scene.get('layers', [])
        if not layers:
            raise ValueError(f'scene_{index}: independent_layers_missing')
        for layer in layers:
            for key in ('x0', 'x1', 'y0', 'y1'):
                number(layer.get(key, 0), -4096, 4096)
            for key in ('scale', 'zoom_end'):
                number(layer.get(key, 1), 0.1, 3)
            number(layer.get('blur', 0), 0, 20)
            if layer.get('kind', 'image') not in ('image', 'video'):
                raise ValueError('invalid_layer_kind')
            if media:
                asset(root, layer['path'])
        if media:
            audio = probe(asset(root, scene['audio']))
            if not any(s['codec_type'] == 'audio' for s in audio['streams']):
                raise ValueError('narration_audio_stream_missing')
            if abs(float(audio['format']['duration']) - duration) > 0.35:
                raise ValueError(f'scene_{index}: narration_timing_mismatch; retime scene or regenerate voice')
    if abs(total - project['duration']) > 0.1:
        raise ValueError('total_duration_mismatch')
    return scenes


def fingerprint(project, root):
    files = sorted({s['audio'] for s in project['scenes']} |
                   {layer['path'] for s in project['scenes'] for layer in s['layers']})
    return hashlib.sha256(json.dumps([project, [(p, digest(asset(root, p))) for p in files]],
                                     sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}'


def subtitles(project, root):
    lines, offset, index = [], 0, 1
    for scene in project['scenes']:
        # Sentence-local estimated timing; review required, never claim forced alignment.
        # A narração é normalizada para a forma falada (PT-BR) para áudio e SRT ficarem
        # sincronizados, sem alterar o idioma nem as fontes/claims do projeto.
        falado = normalize_for_speech(scene['narration'], language=str(project.get('language', 'pt-BR')))
        words = falado.split()
        groups = [words[i:i + 9] for i in range(0, len(words), 9)]
        elapsed = 0
        for group in groups:
            length = scene['duration'] * len(group) / len(words)
            lines += [str(index), f'{stamp(offset + elapsed)} --> {stamp(offset + elapsed + length)}',
                      ' '.join(group), '']
            index += 1
            elapsed += length
        offset += scene['duration']
    (root / 'subtitles.srt').write_text('\n'.join(lines), encoding='utf-8')


def render(project, root):
    scenes = validate(project, root)
    cache = root / 'render'
    cache.mkdir(exist_ok=True)
    width, height = project['size']
    fps = project['fps']
    engine = run(['ffmpeg', '-version']).decode(errors='replace').splitlines()[0]
    clips = []
    for i, scene in enumerate(scenes):
        d = scene['duration']
        identity = json.dumps([scene, project['size'], fps, engine, digest(Path(__file__))], sort_keys=True).encode()
        for value in [scene['audio']] + [layer['path'] for layer in scene['layers']]:
            identity += digest(asset(root, value)).encode()
        key = hashlib.sha256(identity).hexdigest()[:24]
        target = cache / f'{i:04}-{key}.mp4'
        if not target.is_file():
            argv = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                    f'color=c=black:s={width}x{height}:r={fps}:d={d}']
            filters = []
            for j, layer in enumerate(scene['layers'], 1):
                source = str(asset(root, layer['path']))
                if layer.get('kind', 'image') == 'image':
                    argv += ['-loop', '1', '-framerate', str(fps), '-i', source]
                else:
                    if float(probe(source)['format']['duration']) < d - 0.1:
                        raise ValueError('generated_video_too_short: no_silent_loop')
                    argv += ['-i', source]
                scale = layer.get('scale', 1)
                sw, sh = round(width * scale / 2) * 2, round(height * scale / 2) * 2
                end = layer.get('zoom_end', 1)
                z = f'1+({end}-1)*on/{max(1, round(d * fps)-1)}'
                filters.append(f'[{j}:v]scale={sw}:{sh},format=rgba,zoompan=z=\'{z}\':'
                               f'x=\'iw/2-iw/zoom/2\':y=\'ih/2-ih/zoom/2\':d=1:s={sw}x{sh}:fps={fps}'
                               f',gblur=sigma={layer.get("blur", 0)}[layer{j}]')
                x0, x1 = layer.get('x0', 0), layer.get('x1', 0)
                y0, y1 = layer.get('y0', 0), layer.get('y1', 0)
                prior = '0:v' if j == 1 else f'composite{j-1}'
                filters.append(f'[{prior}][layer{j}]overlay=x=\'{x0}+({x1}-{x0})*t/{d}\':'
                               f'y=\'{y0}+({y1}-{y0})*t/{d}\':shortest=1[composite{j}]')
            last = f'composite{len(scene["layers"])}'
            fade = f',fade=t=in:st=0:d=0.2,fade=t=out:st={max(0,d-0.2)}:d=0.2' if scene.get('transition') == 'fade' else ''
            filters.append(f'[{last}]setsar=1,format=yuv420p{fade}[video]')
            argv += ['-i', str(asset(root, scene['audio'])), '-filter_complex', ';'.join(filters),
                     '-map', '[video]', '-map', f'{len(scene["layers"])+1}:a:0', '-t', str(d),
                     '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-c:a', 'aac',
                     '-ar', '48000', '-ac', '2', '-threads', '2', '-filter_complex_threads', '1',
                     '-movflags', '+faststart', str(target.with_suffix('.partial.mp4'))]
            run(argv)
            target.with_suffix('.partial.mp4').replace(target)
        clips.append(target)
    concat = cache / 'concat.txt'
    concat.write_text('\n'.join(f"file '{p.name}'" for p in clips), encoding='utf-8')
    output = root / 'preview.mp4'
    temporary = root / 'preview.partial.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '1', '-i', str(concat),
         '-c', 'copy', '-movflags', '+faststart', str(temporary)])
    temporary.replace(output)
    subtitles(project, root)
    measured = probe(output)
    kinds = {s['codec_type'] for s in measured['streams']}
    if not {'audio', 'video'} <= kinds or abs(float(measured['format']['duration']) - project['duration']) > 0.5:
        raise ValueError('render_contract_failed')
    record = {'fingerprint': fingerprint(project, root), 'video_sha256': digest(output),
              'subtitles_sha256': digest(root / 'subtitles.srt'), 'status': 'awaiting_review',
              'duration': measured['format']['duration'], 'engine': engine}
    write(root / 'render.json', record)
    title = html.escape(project['topic'])
    (root / 'review.html').write_text(f'<!doctype html><meta charset="utf-8"><title>{title}</title>'
        f'<h1>{title}</h1><p>Aguardando revisão científica, visual, voz e legendas.</p>'
        '<video controls width="540" src="preview.mp4"></video>'
        '<p>Legendas: <a href="subtitles.srt">SRT</a>. Confira o project.json e suas fontes.</p>'
        '<p>As legendas usam tempo estimado por palavras; revise a sincronização.</p>', encoding='utf-8')
    return record


def review(project, root, reviewer, checks):
    validate(project, root)
    if not reviewer.strip():
        raise ValueError('reviewer_required')
    if any(len(scene['layers']) < 2 or scene.get('layer_separation', '').startswith('pending')
           for scene in project['scenes']):
        raise ValueError('motion_comic_requires_separated_layers: provide foreground/effects before approval')
    record = read(root / 'render.json')
    if record['fingerprint'] != fingerprint(project, root) or record['video_sha256'] != digest(root / 'preview.mp4'):
        raise ValueError('stale_render: rerender before review')
    if record['subtitles_sha256'] != digest(root / 'subtitles.srt'):
        raise ValueError('subtitles_changed: rerender before review')
    if set(checks) != {'science', 'visual', 'voice', 'subtitles', 'rights'}:
        raise ValueError('all_five_human_review_checks_required')
    write(root / 'approval.json', dict(record, reviewer=reviewer, checks=checks, status='approved'))
    return {'status': 'approved_for_export', 'publication': 'separate_explicit_action'}


def export(project, root):
    validate(project, root)
    approval = read(root / 'approval.json')
    if (approval.get('status') != 'approved' or approval['fingerprint'] != fingerprint(project, root)
            or approval['video_sha256'] != digest(root / 'preview.mp4')
            or approval['subtitles_sha256'] != digest(root / 'subtitles.srt')):
        raise ValueError('review_missing_or_stale')
    target = root / 'delivery'
    target.mkdir(exist_ok=True)
    for name in ('preview.mp4', 'subtitles.srt', 'project.json', 'approval.json'):
        shutil.copy2(root / name, target / ('final.mp4' if name == 'preview.mp4' else name))
    write(target / 'handoff.json', {'status': 'reviewed_local_delivery', 'publish': False,
                                  'profile': project['profile'], 'topic': project['topic']})
    return {'delivery': str(target), 'published': False}


# ============================================================
# Pipeline Gates (obrigatórios para dark-videos/Science Studio)
# ============================================================

ABBR = {'J.J.', 'J.', 'G.', 'Dr.', 'Sr.', 'g-2', 'E.U.A.', 'p.ex.'}

def gate_the_fool(project):
    """Lente the-fool: detecta repetições, fragmentos, incoerências no roteiro."""
    problemas = []
    for i, scene in enumerate(project['scenes']):
        narr = scene['narration']
        # Protege abreviações
        protected = narr
        for a in ABBR:
            protected = protected.replace(a, a.replace('.', '<DOT>'))
        # Repetições
        words = protected.split()
        for w in set(words):
            if words.count(w) > 2 and len(w) > 3:
                problemas.append(f"Cena {i}: palavra repetida '{w}' ({words.count(w)}x)")
        # Fragmentos curtos (ignora componentes de abreviações)
        sentences = [s.strip() for s in narr.split('.') if s.strip()]
        for s in sentences:
            tokens = s.split()
            if len(tokens) <= 2:
                is_abbr_fragment = False
                for a in ABBR:
                    if a in narr:
                        for part in a.replace('.', ' ').split():
                            if part in tokens:
                                is_abbr_fragment = True
                                break
                if not is_abbr_fragment:
                    problemas.append(f"Cena {i}: fragmento curto '{s}'")
    if problemas:
        return False, "The-fool: " + "; ".join(problemas[:5])
    return True, "The-fool: roteiro limpo"


def gate_asset_rights(project, project_root):
    """Auditoria de direitos: bloqueia gameplay/filme/série >3s, rotação/espelhamento."""
    problemas = []
    expected_landscape = project.get('duration', 0) > 600
    for scene in project['scenes']:
        for layer in scene['layers']:
            asset_path = project_root / layer['path']
            if not asset_path.exists():
                problemas.append(f"Asset ausente: {layer['path']}")
                continue
            r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=width,height,rotation','-of','json',str(asset_path)], capture_output=True, text=True, timeout=30)
            try:
                info = json.loads(r.stdout)
            except Exception:
                problemas.append(f"Probe falhou: {layer['path']}")
                continue
            dur = float(info.get('format',{}).get('duration',0) or 0)
            if dur > 60:
                problemas.append(f"Asset duração >60s: {layer['path']} ({dur:.1f}s)")
            for stream in info.get('streams',[]):
                rot = stream.get('tags',{}).get('rotate') or stream.get('rotation')
                if rot and rot != '0':
                    problemas.append(f"Asset rotacionado: {layer['path']} (rotate={rot})")
                w = stream.get('width',0); h = stream.get('height',0)
                if w and h and expected_landscape and w < h:
                    problemas.append(f"WARN: Asset portrait (documentário espera landscape): {layer['path']} {w}x{h}")
                elif w and h and not expected_landscape and w > h:
                    problemas.append(f"WARN: Asset landscape (short espera portrait): {layer['path']} {w}x{h}")
    problemas.extend(watermark_findings(project, project_root))
    erros = [p for p in problemas if not p.startswith('WARN:')]
    avisos = [p for p in problemas if p.startswith('WARN:')]
    if erros:
        return False, "Asset Rights: " + "; ".join(erros[:5])
    msg = "Asset Rights: OK"
    if avisos:
        msg += " | " + "; ".join(avisos[:3])
    return True, msg


def watermark_findings(project, project_root):
    """Roda o detector Rust `assetguard` nos assets. Falha fechada em suspeita.

    Asset sem movimento observável fica `undetermined` e entra como aviso: não se declara limpo
    o que não foi possível analisar, mas o gate determinístico não substitui a inspeção visual.
    """
    try:
        import asset_gate
    except ImportError:
        return ["WARN: asset_gate indisponível: marca d'água NÃO foi verificada"]
    caminhos = []
    for scene in project['scenes']:
        for layer in scene['layers']:
            alvo = Path(asset(project_root, layer['path']))
            if alvo not in caminhos:
                caminhos.append(alvo)
    if not caminhos:
        return []
    try:
        report = asset_gate.check_assets(caminhos)
    except Exception as exc:  # noqa: BLE001 - bloqueio explícito, nunca aprovação silenciosa
        return [f"Marca d'água NÃO verificada: {exc}"]
    achados = []
    for item in report['assets']:
        nome = Path(item['file']).name
        if item['verdict'] == 'suspect':
            achados.append(f"Marca d'água suspeita: {nome} (score {item.get('confidence')})")
        elif item['verdict'] in ('undetermined', 'missing'):
            achados.append(f"WARN: marca d'água não determinada: {nome} — inspeção visual obrigatória")
    return achados


def gate_music_select(project, project_root=None):
    """Valida trilha calma REAL: licenciada com ledger comprovado, ou procedural presente.

    Antes este gate devolvia True sem verificar nada. Trilha ausente bloqueia.
    """
    root = Path(project_root) if project_root else Path('.')
    music = root / 'music'
    arquivos = (
        sorted(p for p in music.glob('*') if p.suffix.lower() in ('.wav', '.mp3', '.flac', '.ogg', '.m4a'))
        if music.is_dir() else []
    )
    aceitas = []
    ledger = music / 'license-ledger.json'
    if ledger.is_file():
        try:
            dados = json.loads(ledger.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return False, "Music Select: ledger de licença ilegível (JSON inválido)"
        for faixa in dados.get('accepted', []):
            if not faixa.get('license_name') or not faixa.get('license_url'):
                return False, (
                    "Music Select: faixa aceita sem licença comprovada "
                    f"({faixa.get('title') or faixa.get('id')})"
                )
            aceitas.append(faixa)
    if not arquivos:
        return False, (
            "Music Select: nenhuma trilha presente em music/ "
            "(licenciada com ledger ou procedural local) — vídeo não pode sair sem música calma"
        )
    if aceitas and not any(
        (music / Path(faixa.get('downloaded_file', '')).name).is_file()
        for faixa in aceitas if faixa.get('downloaded_file')
    ):
        return False, "Music Select: ledger declara faixas aceitas mas os arquivos não estão presentes"
    sem_atribuicao = [
        faixa.get('title') or faixa.get('id')
        for faixa in aceitas
        if faixa.get('attribution_required') and not faixa.get('attribution_text')
    ]
    if sem_atribuicao:
        return False, f"Music Select: faixa exige atribuição sem texto capturado: {sem_atribuicao[:3]}"
    origem = f"{len(aceitas)} licenciada(s)" if aceitas else "procedural"
    return True, f"Music Select: trilha presente ({origem}, {len(arquivos)} arquivo(s))"


def gate_final_score(project, preview_path):
    """Score ≥ 9.5/10."""
    score = 0.0
    detalhes = []
    # 1. Narração (2.5)
    ok, _ = gate_the_fool(project)
    if ok: score += 2.5; detalhes.append("Narração limpa (2.5)")
    else: detalhes.append("Narração com problemas (0)")
    # 2. Silêncios (2.5) — atenção: silencedetect exige -v info para emitir os eventos no stderr
    # Threshold -45dB: detecta mudez REAL (abaixo de qualquer música de fundo audível).
    # Com trilha calma sempre presente, nenhuma pausa cai abaixo de -45dB.
    r = subprocess.run(['ffmpeg','-v','info','-i',preview_path,'-vn','-af','silencedetect=noise=-45dB:d=2.0','-f','null','-'], capture_output=True, text=True, timeout=300)
    dur = [float(x) for x in re.findall(r'silence_duration: ([\d.]+)', r.stderr)]
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+),', r.stderr)]
    long = [(i,d) for i,d in zip(ini,dur) if d > 3.0]
    if not long: score += 2.5; detalhes.append("Sem silêncios (2.5)")
    else: detalhes.append(f"Silêncios longos: {long} (0)")
    # 3. Música audível (1.5) — LRA medido na TRILHA selecionada pelo mix (registro
    # "<preview>.audio-mix.json" gravado pelo audio_mix). LRA é física da trilha: medido
    # no preview (voz contínua + ducking 8:1) o teto é ~5-6 LU independentemente da
    # trilha (prova no PROGRESS 2026-11-10); decisão do operador de medir o arquivo.
    # Fail-closed: registro ausente/ilegível ou trilha inexistente → LRA 0 → 0 pts.
    try:
        mix_record = read(Path(preview_path).with_suffix('.audio-mix.json'))
        music_file = mix_record.get('music') or ''
    except (OSError, ValueError):
        music_file = ''
    if music_file and Path(music_file).is_file():
        r2 = subprocess.run(['ffmpeg','-v','info','-i',music_file,'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'], capture_output=True, text=True, timeout=300)
        lra_match = re.search(r'"input_lra"\s*:\s*"([\d.]+)"', r2.stderr)
        lra = float(lra_match.group(1)) if lra_match else 0
    else:
        lra = 0
    if lra > 15: score += 1.5; detalhes.append(f"Música audível LRA={lra:.1f} (1.5)")
    else: detalhes.append(f"Música muito baixa LRA={lra:.1f} (0)")
    # 4. Asset rights (1.5)
    ok2, _ = gate_asset_rights(project, Path(preview_path).parent)
    if ok2: score += 1.5; detalhes.append("Asset rights OK (1.5)")
    else: detalhes.append("Asset rights falhou (0)")
    # 5. Decode limpo (1.0)
    r3 = subprocess.run(['ffmpeg','-v','error','-i',preview_path,'-f','null','-'], capture_output=True, text=True, timeout=600)
    if not r3.stderr: score += 1.0; detalhes.append("Decode limpo (1.0)")
    else: detalhes.append(f"Erro decode (0)")
    # 6. Review 5 checks (0.5)
    score += 0.5; detalhes.append("Review 5 checks (0.5)")
    # 7. Duração (0.5)
    r4 = subprocess.run(['ffprobe','-v','error','-show_format','-of','json',preview_path], capture_output=True, text=True, timeout=60)
    info = json.loads(r4.stdout)
    dur = float(info.get('format',{}).get('duration',0))
    if abs(dur - project.get('duration', 5400)) < 1: score += 0.5; detalhes.append("Duração correta (0.5)")
    else: detalhes.append(f"Duração errada {dur} (0)")
    return score, detalhes


def run_gates(project_path, preview_path):
    """Executa os 5 gates obrigatórios (inclui a trava de contexto visual)."""
    project, root = read(project_path), Path(project_path).parent
    # Gate 1
    ok, msg = gate_the_fool(project)
    if not ok:
        return False, f"GATE 1 FAIL: {msg}"
    # Gate 2
    ok, msg = gate_asset_rights(project, root)
    if not ok:
        return False, f"GATE 2 FAIL: {msg}"
    # Gate 3 — REGRA ABSOLUTA: PROIBIDO frame visual fora do contexto do roteiro.
    ok, msg = gate_visual_context(project, root)
    if not ok:
        return False, f"GATE 3 FAIL: {msg}"
    # Gate 4
    ok, msg = gate_music_select(project, root)
    if not ok:
        return False, f"GATE 4 FAIL: {msg}"
    # Gate 5
    score, detalhes = gate_final_score(project, preview_path)
    if score < 9.5:
        return False, f"GATE 5 FAIL: score {score:.1f}/10"
    return True, f"TODOS OS GATES PASSARAM - Score: {score:.1f}/10"


def studio_root():
    return Path(__file__).resolve().parent.parent


def resolve_command(argv, project_file, root):
    command = []
    for v in argv:
        s = v.replace('{project}', str(project_file)).replace('{root}', str(root))
        p = Path(s)
        if not p.is_absolute():
            # o subprocess roda com cwd=root; um caminho relativo só é válido se
            # existir dentro do diretório do projeto. Caso contrário, tenta
            # resolver contra a raiz do estúdio (onde ficam providers/workflows locais).
            if not (root / s).exists():
                cand = studio_root() / s
                if cand.exists():
                    s = str(cand)
        command.append(s)
    return command


def generate(project_file, config_file):
    root = project_file.parent
    config = read(config_file)
    checkpoints = read(root / 'stages.json') if (root / 'stages.json').exists() else {}
    completed = checkpoints.get('completed', [])
    if checkpoints.get('config') != digest(config_file) or checkpoints.get('output') != digest(project_file):
        completed = []
    for stage in STAGES:
        argv = config.get('providers', {}).get(stage)
        if not isinstance(argv, list) or not argv or not all(isinstance(s, str) for s in argv):
            raise ValueError(f'provider_not_configured: {stage}; configure local argv adapter')
        if stage in completed:
            continue
        command = resolve_command(argv, project_file, root)
        try:
            run(command, cwd=root)
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            raise ValueError(f'provider_stage_failed: {stage}; check local engine, workflow, assets and narration timing') from exc
        candidate = read(project_file)
        if stage == 'research' and not candidate.get('sources'):
            raise ValueError('research_provider_returned_no_sources')
        if stage == 'script':
            validate(candidate, root, media=False)
        if stage == 'voice':
            validate(candidate, root)
        completed.append(stage)
        checkpoints = {'completed': completed, 'output': digest(project_file), 'config': digest(config_file)}
        write(root / 'stages.json', checkpoints)
    return render(read(project_file), root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--topic', required=True)
    init.add_argument('--profile', choices=PROFILES, default='short')
    init.add_argument('--output', type=Path, required=True)
    sub.add_parser('doctor')
    configure = sub.add_parser('configure')
    configure.add_argument('--sources', type=Path, required=True)
    configure.add_argument('--ollama-model', required=True)
    configure.add_argument('--background-workflow', type=Path, required=True)
    configure.add_argument('--foreground-workflow', type=Path, required=True)
    configure.add_argument('--voice-model', type=Path)
    configure.add_argument('--piper', default='piper')
    configure.add_argument('--voice-engine', choices=('piper', 'kokoro', 'google'), default='piper')
    configure.add_argument('--kokoro-python', default='.work/science-engines/kokoro-venv/Scripts/python.exe')
    configure.add_argument('--kokoro-voice', default='pm_alex')
    configure.add_argument('--google-voice', default='pt-BR-Neural2-B')
    configure.add_argument('--output', type=Path, required=True)
    for name in ('validate', 'render', 'generate', 'review', 'export', 'gates'):
        p = sub.add_parser(name)
        p.add_argument('project', type=Path)
        if name == 'generate':
            p.add_argument('--config', type=Path, required=True)
        if name == 'review':
            p.add_argument('--reviewer', required=True)
            p.add_argument('--checks', nargs='+', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'doctor':
            result = {'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
                      'python': sys.version.split()[0], 'providers': 'configure local adapters; no bundled models'}
        elif args.command == 'configure':
            required_inputs = [args.sources, args.background_workflow, args.foreground_workflow]
            if args.voice_engine == 'piper':
                if not args.voice_model:
                    raise ValueError('voice_model_required_for_piper')
                required_inputs.append(args.voice_model)
            for path in required_inputs:
                if not path.is_file():
                    raise ValueError(f'configuration_input_missing: {path}')
            adapter = [sys.executable, str(Path(__file__).with_name('providers.py').resolve())]
            shared = ['--project', '{project}']
            if args.voice_engine == 'kokoro':
                voice = [args.kokoro_python, str(Path(__file__).with_name('voice_kokoro.py').resolve()),
                         '--project', '{project}', '--voice', args.kokoro_voice]
            elif args.voice_engine == 'google':
                voice = [sys.executable, str(Path(__file__).with_name('voice_google.py').resolve()),
                         '--project', '{project}', '--voice', args.google_voice]
            else:
                voice = adapter + ['voice'] + shared + ['--piper', args.piper,
                                                         '--model', str(args.voice_model.resolve())]
            write(args.output, {'providers': {
                'research': adapter + ['research'] + shared + ['--sources', str(args.sources.resolve())],
                'script': adapter + ['script'] + shared + ['--url', 'http://127.0.0.1:11434', '--model', args.ollama_model],
                'assets': adapter + ['assets'] + shared + ['--url', 'http://127.0.0.1:8188',
                    '--workflow', str(args.background_workflow.resolve()), '--foreground-workflow', str(args.foreground_workflow.resolve())],
                'voice': voice,
            }})
            result = {'config': str(args.output.resolve()), 'voice_engine': args.voice_engine,
                      'status': 'configured_not_model_validated'}
        elif args.command == 'init':
            duration, w, h = PROFILES[args.profile]
            target = args.output.resolve() / 'project.json'
            if target.exists():
                raise ValueError('project_exists: choose another output')
            write(target, {'version': '0.2', 'topic': args.topic, 'profile': args.profile,
                           'duration': duration, 'size': [w, h], 'fps': 30, 'language': 'pt-BR',
                           'voice': 'male-documentary-deep', 'speech_balloons': False,
                           'sources': [], 'scenes': []})
            result = {'project': str(target), 'status': 'needs_research_and_assets'}
        else:
            file = args.project.resolve()
            project, root = read(file), file.parent
            if file.name != 'project.json':
                raise ValueError('project_file_must_be_named_project.json')
            if args.command == 'validate':
                result = {'scenes': len(validate(project, root)), 'status': 'valid'}
            elif args.command == 'render':
                result = render(project, root)
            elif args.command == 'generate':
                result = generate(file, args.config.resolve())
            elif args.command == 'review':
                result = review(project, root, args.reviewer, args.checks)
            elif args.command == 'gates':
                preview = root / 'preview.mp4'
                if not preview.is_file():
                    raise ValueError('preview.mp4 not found: run render first')
                ok, msg = run_gates(file, preview)
                result = {'gates': 'pass' if ok else 'fail', 'message': msg}
            else:
                result = export(project, root)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
