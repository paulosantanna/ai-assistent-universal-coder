"""Driver resumível da produção de documentário (documentary-factory).

O render de 90 minutos é um trabalho de horas. Este driver existe para que a produção seja
retomável: cada etapa verifica o que já está pronto e só refaz o que falta, registrando o estado
em `factory-state.json`. Interromper e retomar não perde trabalho válido.

Etapas (todas idempotentes):
    preflight  confere pré-requisitos reais (ffmpeg, motores, projeto)
    voice      narração Kokoro por cena (pula cenas já sintetizadas)
    layers     anexa as camadas do manifesto `assets/layers.json` ao project.json
    render     compõe as cenas e concatena o preview
    mix        mixagem documental com trilha calma e ducking
    gates      gates determinísticos (narração, direitos+marca d'água, música, score)
    status     mostra o progresso

Uso:
    python science-studio/factory_production.py <projeto> status
    python science-studio/factory_production.py <projeto> --all
    python science-studio/factory_production.py <projeto> render

A etapa `judge` (The-Fool adversarial, nota >= 9,5) NÃO é automatizada aqui de propósito: exige
contexto virgem e julgamento por evidência, conforme `documentary-adversarial-judge`.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
STUDIO = Path(__file__).resolve().parent / 'studio.py'
KOKORO_VENV = WORKSPACE / '.work' / 'science-engines' / 'kokoro-venv' / 'Scripts' / 'python.exe'
STATE_NAME = 'factory-state.json'


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sh(argv: list[str], *, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    print('  $ ' + ' '.join(str(part) for part in argv), flush=True)
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)


def project_of(root: Path) -> dict:
    project_file = root / 'project.json'
    if not project_file.is_file():
        raise SystemExit(f'factory: project.json ausente em {root}')
    return json.loads(project_file.read_text(encoding='utf-8'))


def scenes_missing_audio(project: dict, root: Path) -> list[int]:
    missing = []
    for index, scene in enumerate(project['scenes']):
        audio = scene.get('audio')
        if not audio or not (root / audio).is_file():
            missing.append(index)
    return missing


def step_preflight(root: Path, state: dict) -> bool:
    problems = []
    if not STUDIO.is_file():
        problems.append(f'studio.py ausente: {STUDIO}')
    for tool in ('ffmpeg', 'ffprobe'):
        if sh([tool, '-version']).returncode != 0:
            problems.append(f'{tool} não está no PATH')
    if not KOKORO_VENV.is_file():
        problems.append(f'venv do Kokoro ausente: {KOKORO_VENV}')
    project = project_of(root)
    scenes = project.get('scenes', [])
    if not scenes:
        problems.append('project.json sem cenas')
    total = sum(scene.get('duration', 0) for scene in scenes)
    if scenes and abs(total - project.get('duration', 0)) > 0.1:
        problems.append(f'soma das cenas ({total}s) difere da duração do projeto')
    state['preflight'] = {
        'status': 'failed' if problems else 'complete',
        'problems': problems,
        'scenes': len(scenes),
        'total_duration': total,
    }
    if problems:
        print('preflight FALHOU:')
        for problem in problems:
            print(f'  - {problem}')
        return False
    print(f'preflight OK: {len(scenes)} cenas, {total}s')
    return True


def step_voice(root: Path, state: dict) -> bool:
    project = project_of(root)
    missing = scenes_missing_audio(project, root)
    if not missing:
        print(f'voice: {len(project["scenes"])} cenas já narradas — nada a fazer')
        state['voice'] = {'status': 'complete', 'scenes': len(project['scenes'])}
        return True
    print(f'voice: {len(missing)} cena(s) sem áudio — sintetizando o projeto inteiro')
    result = sh([str(KOKORO_VENV), str(WORKSPACE / 'science-studio' / 'voice_kokoro.py'),
                 '--project', str(root / 'project.json'), '--voice', state.get('voice_name', 'pm_alex'),
                 '--device', 'cuda'], timeout=21600)
    print(result.stdout.strip()[-1500:])
    if result.returncode != 0:
        print(result.stderr.strip()[-2000:], file=sys.stderr)
        state['voice'] = {'status': 'failed', 'stderr': result.stderr.strip()[-800:]}
        return False
    state['voice'] = {'status': 'complete', 'scenes': len(project['scenes'])}
    return True


def step_layers(root: Path, state: dict) -> bool:
    manifest_file = root / 'assets' / 'layers.json'
    project_file = root / 'project.json'
    project = project_of(root)
    if not manifest_file.is_file():
        print(f'layers: manifesto ausente: {manifest_file}')
        state['layers'] = {'status': 'blocked', 'reason': 'manifesto de camadas ausente'}
        return False
    manifest = load(manifest_file)
    entries: dict[str, list[dict]] = {str(key): value for key, value in manifest.get('scenes', {}).items()}
    problemas = []
    for index, scene in enumerate(project['scenes']):
        layers = entries.get(str(index))
        if not layers:
            problemas.append(f'cena {index}: sem camadas no manifesto')
            continue
        if len(layers) < 2:
            problemas.append(f'cena {index}: {len(layers)} camada(s) — o contrato exige >= 2')
        for layer in layers:
            if not (root / layer['path']).is_file():
                problemas.append(f'cena {index}: asset ausente {layer["path"]}')
        scene['layers'] = layers
    state['layers'] = {'status': 'failed' if problemas else 'complete',
                       'problems': problemas[:20]}
    if problemas:
        print('layers BLOQUEADO:')
        for problem in problemas[:10]:
            print(f'  - {problem}')
        return False
    project_file.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'layers OK: {len(project["scenes"])} cenas com camadas anexadas')
    return True


def step_render(root: Path, state: dict) -> bool:
    preview = root / 'preview.mp4'
    record = load(root / 'render.json')
    if preview.is_file() and record.get('status') == 'awaiting_review':
        print('render: preview já existe — pulando (apague preview.mp4 para refazer)')
        state['render'] = {'status': 'complete', 'skipped': True}
        return True
    result = sh([sys.executable, str(STUDIO), 'render', str(root / 'project.json')], timeout=43200)
    print(result.stdout.strip()[-2000:])
    if result.returncode != 0:
        print(result.stderr.strip()[-3000:], file=sys.stderr)
        state['render'] = {'status': 'failed', 'stderr': result.stderr.strip()[-800:]}
        return False
    state['render'] = {'status': 'complete', 'skipped': False}
    return True


def step_mix(root: Path, state: dict) -> bool:
    record = load(root / 'render.json')
    if record.get('audio_mix'):
        print('mix: já aplicado (render.json registra audio_mix) — pulando')
        state['mix'] = {'status': 'complete', 'skipped': True, 'music': record.get('audio_mix')}
        return True
    music = state.get('music_file')
    if music and not Path(music).is_file():
        print(f'mix: trilha declarada não existe: {music}')
        return False
    argv = [sys.executable, str(WORKSPACE / 'science-studio' / 'audio_mix.py'),
            '--input', str(root / 'preview.mp4'), '--in-place', '--record', str(root / 'render.json')]
    if music:
        argv += ['--music', music]
    result = sh(argv, timeout=7200)
    print(result.stdout.strip()[-1500:])
    if result.returncode != 0:
        print(result.stderr.strip()[-2500:], file=sys.stderr)
        state['mix'] = {'status': 'failed', 'stderr': result.stderr.strip()[-800:]}
        return False
    state['mix'] = {'status': 'complete', 'skipped': False, 'music': music or 'procedural'}
    return True


def step_gates(root: Path, state: dict) -> bool:
    result = sh([sys.executable, str(STUDIO), 'gates', str(root / 'project.json')], timeout=3600)
    print(result.stdout.strip()[-2000:])
    ok = result.returncode == 0
    state['gates'] = {'status': 'pass' if ok else 'fail',
                      'stdout': result.stdout.strip()[-600:],
                      'stderr': result.stderr.strip()[-600:]}
    if not ok:
        print(result.stderr.strip()[-2000:], file=sys.stderr)
    return ok


STEPS = {
    'preflight': step_preflight,
    'voice': step_voice,
    'layers': step_layers,
    'render': step_render,
    'mix': step_mix,
    'gates': step_gates,
}
ORDER = ['preflight', 'voice', 'layers', 'render', 'mix', 'gates']


def show_status(root: Path, state: dict) -> None:
    project = load(root / 'project.json')
    scenes = project.get('scenes', [])
    print(f'projeto   : {root}')
    print(f'cenas     : {len(scenes)} | duração alvo: {project.get("duration", "?")}s')
    if scenes:
        print(f'narradas  : {len(scenes) - len(scenes_missing_audio(project, root))}/{len(scenes)}')
        com_camadas = sum(1 for scene in scenes if len(scene.get('layers', [])) >= 2)
        print(f'camadas   : {com_camadas}/{len(scenes)} com >= 2 camadas')
    for name in ORDER:
        entry = state.get(name)
        marker = entry.get('status') if entry else 'pendente'
        detail = ''
        if name == 'gates' and entry:
            detail = f" — {entry.get('stdout', '')[:80]}"
        print(f'{name:10}: {marker}{detail}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Driver resumível da produção de documentário')
    parser.add_argument('project_dir', type=Path)
    parser.add_argument('steps', nargs='*', choices=[*ORDER, 'status'], default=['status'])
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--music', help='faixa de trilha calma licenciada (senão usa a procedural)')
    parser.add_argument('--voice-name', default='pm_alex')
    args = parser.parse_args(argv)

    root: Path = args.project_dir
    if not root.is_dir():
        raise SystemExit(f'factory: diretório inexistente: {root}')
    state_file = root / STATE_NAME
    state = load(state_file)
    if args.music:
        state['music_file'] = args.music
    state.setdefault('voice_name', args.voice_name)

    if args.all:
        wanted = list(ORDER)
    elif args.steps and args.steps != ['status']:
        wanted = [step for step in args.steps if step != 'status']
    else:
        wanted = []

    if not wanted:
        show_status(root, state)
        save(state_file, state)
        return 0

    for name in wanted:
        print(f'== {name} ==')
        if not STEPS[name](root, state):
            save(state_file, state)
            print(f'\nfactory: parou em "{name}" — corrija e retome (o trabalho anterior foi preservado)')
            return 1
        save(state_file, state)

    save(state_file, state)
    show_status(root, state)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
