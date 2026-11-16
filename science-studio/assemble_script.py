"""Consolida os fragmentos de capítulo num `project.json` válido do Science Studio.

O roteiro longo é produzido em capítulos paralelos (uma unidade de sessão por capítulo). Este
montador junta os fragmentos e aplica a verificação que o compositor não faz sozinho: orçamento de
palavras por cena, repetição, fragmento curto, cobertura de claims e soma de duração.

Uso:
    python science-studio/assemble_script.py .work/electron-factory-90min \
        --topic "O Elétron: descoberta e curiosidades" --profile full-documentary

Ler os fragmentos de `<projeto>/script/chapter-*.json`, cada um no formato:
    {"chapter": 1, "title": "...", "scenes": [
        {"narration": "...", "visual": "...", "duration": 60,
         "claims": ["id-da-fonte"], "transition": "cut", "sd_prompt": "..."}]}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROFILES = {
    'short': (60, 1080, 1920),
    'youtube': (600, 1920, 1080),
    'documentary': (3600, 1920, 1080),
    'full-documentary': (5400, 1920, 1080),
}
WORDS_PER_MINUTE = (108, 136)
ABBREVIATIONS = {'J.J.', 'J.', 'G.', 'Dr.', 'Sr.', 'g-2', 'E.U.A.', 'p.ex.', 'a.C.', 'd.C.'}


def word_budget(duration: int) -> tuple[int, int]:
    low = round(duration * WORDS_PER_MINUTE[0] / 60)
    high = round(duration * WORDS_PER_MINUTE[1] / 60)
    return low, high


def count_words(text: str) -> int:
    return len([token for token in text.split() if token.strip()])


def check_scene(index: int, scene: dict, evidence: set[str]) -> list[str]:
    problems: list[str] = []
    narration = scene.get('narration', '')
    duration = scene.get('duration', 0)
    if not narration.strip():
        problems.append(f'cena {index}: narração vazia')
    if not scene.get('visual', '').strip():
        problems.append(f'cena {index}: visual vazio')
    if not scene.get('sd_prompt', '').strip():
        problems.append(f'cena {index}: sd_prompt vazio (arte não pode ser genérica)')
    if scene.get('transition', 'cut') not in ('cut', 'fade'):
        problems.append(f'cena {index}: transição inválida {scene.get("transition")!r}')

    claims = scene.get('claims') or []
    if not claims:
        problems.append(f'cena {index}: sem claims')
    for claim in claims:
        if claim not in evidence:
            problems.append(f'cena {index}: claim sem fonte no ledger: {claim}')

    low, high = word_budget(duration)
    words = count_words(narration)
    if words < low:
        problems.append(
            f'cena {index}: subnarrada — {words} palavras para {duration}s (mínimo {low}). '
            'Cena subnarrada produz silêncio e reprova o vídeo.'
        )
    elif words > high:
        problems.append(f'cena {index}: {words} palavras para {duration}s (máximo {high})')

    protected = narration
    for abbreviation in ABBREVIATIONS:
        protected = protected.replace(abbreviation, abbreviation.replace('.', '\u0000'))
    tokens = protected.split()
    for token in set(tokens):
        if len(token) > 3 and tokens.count(token) > 2:
            problems.append(f'cena {index}: palavra repetida "{token}" ({tokens.count(token)}x)')
    for sentence in [part.strip() for part in protected.split('.') if part.strip()]:
        if len(sentence.split()) <= 2:
            problems.append(f'cena {index}: fragmento curto "{sentence}"')
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Monta o project.json a partir dos capítulos')
    parser.add_argument('project_dir', type=Path)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--profile', default='full-documentary', choices=sorted(PROFILES))
    parser.add_argument('--out', type=Path)
    parser.add_argument('--allow-words-out-of-range', action='store_true')
    args = parser.parse_args(argv)

    root: Path = args.project_dir
    duration, width, height = PROFILES[args.profile]

    sources_file = root / 'sources.json'
    if not sources_file.is_file():
        print(f'assemble: corpus ausente: {sources_file}', file=sys.stderr)
        return 1
    sources = json.loads(sources_file.read_text(encoding='utf-8')).get('sources', [])
    known = {item.get('id') for item in sources}
    # Cada capítulo pode trazer fontes próprias verificadas; o montador funde sem duplicar.
    for extra in sorted((root / 'script').glob('*-sources.json')):
        try:
            payload = json.loads(extra.read_text(encoding='utf-8'))
        except json.JSONDecodeError as error:
            print(f'assemble: {extra.name} ignorado (JSON inválido: {error})', file=sys.stderr)
            continue
        for item in payload.get('sources', []):
            usable = (
                item.get('id') and item.get('url') and item.get('accessed') and item.get('excerpt')
            )
            if usable and item['id'] not in known:
                sources.append(item)
                known.add(item['id'])
    evidence = {
        item['id']
        for item in sources
        if item.get('id') and item.get('url') and item.get('accessed') and item.get('excerpt')
    }
    if not evidence:
        print('assemble: nenhuma fonte utilizável (id+url+accessed+excerpt)', file=sys.stderr)
        return 1

    # `chapter-NN-sources.json` é ledger de fontes, não capítulo: fica fora dos fragmentos.
    fragments = [
        path
        for path in sorted((root / 'script').glob('chapter-*.json'))
        if not path.name.endswith('-sources.json')
    ]
    if not fragments:
        print(f'assemble: nenhum fragmento em {root / "script"}', file=sys.stderr)
        return 1

    scenes: list[dict] = []
    chapters: list[dict] = []
    problems: list[str] = []
    for fragment_path in fragments:
        try:
            fragment = json.loads(fragment_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as error:
            problems.append(f'{fragment_path.name}: JSON inválido — {error}')
            continue
        chapter_scenes = fragment.get('scenes', [])
        if not chapter_scenes:
            problems.append(f'{fragment_path.name}: sem cenas')
            continue
        chapters.append(
            {
                'chapter': fragment.get('chapter'),
                'title': fragment.get('title', ''),
                'scenes': len(chapter_scenes),
            }
        )
        for scene in chapter_scenes:
            index = len(scenes) + 1
            problems.extend(check_scene(index, scene, evidence))
            scenes.append(
                {
                    'narration': scene['narration'].strip(),
                    'visual': scene['visual'].strip(),
                    'duration': int(scene.get('duration', 60)),
                    'claims': list(scene.get('claims') or []),
                    'transition': scene.get('transition', 'cut'),
                    'sd_prompt': scene['sd_prompt'].strip(),
                    'chapter': fragment.get('chapter'),
                }
            )

    total = sum(scene['duration'] for scene in scenes)
    if abs(total - duration) > 0.1:
        problems.append(f'duração total {total}s difere do alvo {duration}s')

    hard = problems
    if args.allow_words_out_of_range:
        hard = [p for p in problems if 'palavras para' not in p or 'subnarrada' in p]

    report = {
        'chapters': chapters,
        'scenes': len(scenes),
        'total_duration': total,
        'target_duration': duration,
        'sources_usable': len(evidence),
        'problems': problems[:60],
        'problem_count': len(problems),
    }

    if hard:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print(f'\nassemble: BLOQUEADO — {len(hard)} problema(s) impedem montar o projeto', file=sys.stderr)
        return 2

    out = args.out or (root / 'project.json')
    project = {
        'version': '0.2',
        'language': 'pt-BR',
        'profile': args.profile,
        'speech_balloons': False,
        'size': [width, height],
        'fps': 30,
        'duration': duration,
        'topic': args.topic,
        'sources': sources,
        'chapters': chapters,
        'scenes': scenes,
    }
    out.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding='utf-8')
    report['written'] = str(out)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if problems:
        print(f'assemble: montado com {len(problems)} aviso(s) de palavra', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
