"""Trava de contexto visual do Science Studio (vídeos de canal dark, 100% IA).

REGRA ABSOLUTA (pedido do operador, 2026-11-08): PROIBIDO qualquer frame visual fora
do contexto do roteiro. Se a cena fala de música, o frame mostra música daquele estilo;
se fala de um átomo, o frame mostra átomos. Nada genérico, nada aleatório.

Como a regra é aplicada (determinística, falha fechada, sem bypass):

1. Proveniência estrutural: todo asset gerado por IA recebe uma entrada no ledger
   `assets/prompts.json` ligando arquivo → cena → prompt exato usado na geração.
   O gate prova o vínculo comparando os tokens do prompt com os tokens do roteiro da cena.
2. matching léxico: assets curados (sem ledger) só passam se o NOME do arquivo citar
   o contexto da cena (token comum após normalização de acentos/plural e famílias de domínio).
3. Falha fechada: asset sem prova de contexto, ledger inválido, cena sem tokens de roteiro
   ou prompt fora de contexto BLOQUEIAM o vídeo. Nunca existe "aproximado o bastante".

Famílias de domínio são DADOS declarados (ex.: átomo↔atom, música↔music), não inferência
semântica. Família ausente só torna o gate mais estrito, nunca mais frouxo.

Este módulo é stdlib-only e não importa `studio` (studio importa este módulo).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

LEDGER_NAME = 'prompts.json'
REPORT_NAME = 'context_report.json'

# Palavras funcionais PT/EN e enchimento de prompt de geração. Nada aqui é termo de assunto.
STOPWORDS = frozenset({
    # funcionais PT
    'de', 'da', 'do', 'das', 'dos', 'que', 'com', 'por', 'para', 'no', 'na', 'nos', 'nas',
    'em', 'um', 'uma', 'uns', 'umas', 'ao', 'aos', 'se', 'seu', 'sua', 'seus', 'suas',
    'ele', 'ela', 'eles', 'elas', 'isso', 'isto', 'aquilo', 'como', 'sobre', 'entre',
    'pelo', 'pela', 'pelos', 'pelas', 'ser', 'tem', 'ter', 'foi', 'sao', 'esta', 'mais',
    'menos', 'muito', 'toda', 'todo', 'todas', 'todos', 'onde', 'quando', 'entao', 'esse',
    'essa', 'este', 'esta', 'the', 'of', 'and', 'in', 'on', 'to', 'a', 'an', 'is', 'are',
    # enchimento de prompt/estilo visual (não é assunto)
    'arte', 'art', 'estilo', 'style', 'desenho', 'imagem', 'image', 'cena', 'scene',
    'mostrando', 'showing', 'detailed', 'cinematic', 'comic', 'detailed', 'composition',
    'generous', 'safe', 'margins', 'isolated', 'main', 'subject', 'transparent',
    'background', 'foreground', 'text', 'watermark', 'logo', 'lettering', 'speech',
    'balloons', 'balloon', 'same', 'visual', 'texture', 'closeup', 'wide', 'shot',
})

# Famílias de domínio declaradas como dados: token → representante canônico da família.
# Extenso apenas por edição explícita; ausência = gate mais estrito (nunca mais frouxo).
DOMAIN_FAMILIES: tuple[tuple[str, ...], ...] = (
    ('atomo', 'atom', 'atomico', 'atomic', 'subatomico', 'subatomic'),
    ('musica', 'music', 'musical', 'cancao', 'song', 'melodia', 'melody', 'instrumento', 'instrument'),
    ('eletron', 'electron', 'eletronica', 'electronic'),
    ('espaco', 'space', 'cosmos', 'cosmico', 'cosmic', 'universo', 'universe', 'galaxia',
     'galaxy', 'estrela', 'star', 'estelar', 'stellar', 'planeta', 'planet'),
    ('celula', 'cell', 'dna', 'gene', 'genetica', 'genetic', 'organismo', 'organism',
     'biologia', 'biology', 'proteina', 'protein'),
    ('cerebro', 'brain', 'neuronio', 'neuron', 'mente', 'mind'),
    ('energia', 'energy', 'foton', 'photon', 'quantum', 'quantico', 'quantica'),
    ('historia', 'history', 'historico', 'historic', 'antiguidade', 'antiquity'),
    ('agua', 'water', 'oceano', 'ocean', 'mar', 'sea', 'rio', 'river'),
    ('luz', 'light', 'optico', 'optical', 'optica'),
    ('computador', 'computer', 'tecnologia', 'technology', 'algoritmo', 'algorithm',
     'codigo', 'code', 'robot', 'robo'),
)
_FAMILY: dict[str, str] = {}
for _family in DOMAIN_FAMILIES:
    _canonical = _family[0]
    for _member in _family:
        _FAMILY[_member] = _canonical

_TOKEN = re.compile(r'[^\W_]+', re.UNICODE)


class OffContextError(ValueError):
    """Nenhum asset disponível está no contexto do roteiro da cena."""


def fold(text: str) -> str:
    decomposed = unicodedata.normalize('NFD', (text or '').casefold())
    return ''.join(char for char in decomposed if unicodedata.category(char) != 'Mn')


def normalize(token: str) -> str:
    # Plural simples PT/EN ('atomos'→'atomo', 'waves'→'wave'); depois família de domínio.
    if len(token) >= 5 and token.endswith('s') and not token.endswith('ss'):
        token = token[:-1]
    return _FAMILY.get(token, token)


def tokens(text: str) -> set[str]:
    folded = fold(text)
    return {
        normalize(token)
        for token in _TOKEN.findall(folded)
        if len(token) >= 3 and token not in STOPWORDS
    }


def context_tokens(*texts: str) -> set[str]:
    result: set[str] = set()
    for text in texts:
        result |= tokens(text)
    return result


def asset_name_tokens(stem: str) -> set[str]:
    return tokens(stem.replace('-', ' ').replace('_', ' '))


def match_score(context: set[str], asset: set[str]) -> int:
    # Normaliza de novo por robustez: conjuntos crus e saídos de tokens() produzem o mesmo score.
    return len({normalize(token) for token in context} & {normalize(token) for token in asset})


# ---------------------------------------------------------------- ledger de proveniência

def ledger_file(root: Path) -> Path:
    return Path(root) / 'assets' / LEDGER_NAME


def load_ledger(root: Path) -> dict:
    path = ledger_file(root)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'ledger de proveniencia ilegivel ({LEDGER_NAME}): {error}') from error
    if not isinstance(data, dict):
        raise ValueError(f'ledger de proveniencia invalido: raiz nao e objeto ({LEDGER_NAME})')
    return data


def record_generation(root, relpath, scene, kind, prompt, seed, generated=True) -> None:
    """Vincula arquivo gerado por IA → cena → prompt exato. Upsert idempotente."""
    path = ledger_file(root)
    data = load_ledger(root)
    data[Path(relpath).as_posix()] = {
        'scene': int(scene), 'kind': str(kind), 'prompt': str(prompt),
        'seed': seed, 'generated': bool(generated),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


# ---------------------------------------------------------------- gate

def _layer_verdict(layer: dict, scene_index: int, context: set[str], ledger: dict) -> dict:
    rel = Path(layer.get('path', '')).as_posix()
    entry = ledger.get(rel)
    if entry is not None:
        if not entry.get('generated'):
            return {'verdict': 'fail', 'score': 0, 'evidence': (
                'asset sem prova de geracao IA no ledger (generated=false); '
                'apague o arquivo e regenere no contexto da cena')}
        if entry.get('scene') != scene_index:
            return {'verdict': 'fail', 'score': 0, 'evidence': (
                f"ledger vincula o asset a cena {entry.get('scene')}, nao a cena {scene_index}")}
        prompt_tokens = context_tokens(str(entry.get('prompt', '')))
        score = match_score(context, prompt_tokens)
        if score < 1:
            return {'verdict': 'fail', 'score': 0, 'evidence': (
                'prompt de geracao nao cita o contexto do roteiro desta cena')}
        return {'verdict': 'proven', 'score': score,
                'evidence': 'gerado por IA para esta cena a partir do roteiro (ledger)'}
    score = match_score(context, asset_name_tokens(Path(rel).stem))
    if score >= 1:
        return {'verdict': 'named', 'score': score,
                'evidence': 'nome do asset cita o contexto da cena'}
    return {'verdict': 'fail', 'score': 0, 'evidence': (
        'sem proveniencia de contexto: nome sem termo do roteiro e sem entrada no ledger')}


def _write_report(root: Path, report: dict) -> None:
    path = Path(root) / REPORT_NAME
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def gate_visual_context(project: dict, project_root) -> tuple[bool, str]:
    """Gate deterministico: todo frame deve estar no contexto do roteiro. Falha fechada."""
    root = Path(project_root)
    try:
        ledger = load_ledger(root)
    except ValueError as error:
        return False, f'Contexto visual: {error}'
    problems: list[str] = []
    scenes_report: list[dict] = []
    proven = 0
    for index, scene in enumerate(project.get('scenes', [])):
        context = context_tokens(
            str(project.get('topic', '')), str(scene.get('narration', '')),
            str(scene.get('visual', '')), str(scene.get('sd_prompt', '')),
        )
        scene_report = {'scene': index, 'context_tokens': len(context), 'layers': []}
        if not context:
            problems.append(f'Cena {index}: contexto do roteiro vazio (nada a comparar)')
        for layer in scene.get('layers', []):
            verdict = _layer_verdict(layer, index, context, ledger)
            scene_report['layers'].append({'path': layer.get('path'), **verdict})
            if verdict['verdict'] == 'fail':
                problems.append(
                    f"Cena {index}: {layer.get('path')} FORA DO CONTEXTO — {verdict['evidence']}")
            else:
                proven += 1
        scenes_report.append(scene_report)
    _write_report(root, {
        'policy': 'PROIBIDO frame visual fora do contexto do roteiro (falha fechada)',
        'scenes': scenes_report,
        'violations': problems,
    })
    if problems:
        return False, 'Contexto visual: ' + '; '.join(problems[:5])
    return True, (f'Contexto visual: todos os frames no contexto do roteiro '
                  f'({proven} camadas com proveniencia)')


def select_scene_assets(index: list[dict], scene: dict, topic: str = '') -> tuple[dict, dict, int]:
    """Escolhe (frente, fundo, score) dentro do contexto; levanta OffContextError se zero.

    Usado por build_layers: substitui o comportamento antigo que, sem casamento, escolhia
    silenciosamente o primeiro asset em ordem alfabética (frame fora de contexto).
    """
    context = context_tokens(topic, str(scene.get('narration', '')),
                             str(scene.get('visual', '')), str(scene.get('sd_prompt', '')))
    ranked = sorted(index, key=lambda item: (-match_score(context, item['tokens']),
                                             item['path'].name))
    if not ranked or match_score(context, ranked[0]['tokens']) == 0:
        sample = ', '.join(sorted(context)[:8]) or '(vazio)'
        raise OffContextError(
            f'nenhum asset no contexto do roteiro da cena (tokens do roteiro: {sample})')
    foreground = ranked[0]
    # O fundo precisa TAMBÉM estar no contexto: sem segundo asset casado, reusa o primeiro.
    background = foreground
    if len(ranked) > 1 and match_score(context, ranked[1]['tokens']) > 0:
        background = ranked[1]
    return foreground, background, match_score(context, foreground['tokens'])
