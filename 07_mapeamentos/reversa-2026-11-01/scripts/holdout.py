"""Frozen natural-language retrieval probes, limited to known source paths."""
import json
from corpus import OUT, search

cases = [
    ('Qual arquivo salva hashes dos arquivos instalados?', 'lib/installer/manifest.js'),
    ('Como detectar quais engines estão instaladas?', 'lib/installer/detector.js'),
    ('Como a atualização lida com arquivos modificados?', 'lib/commands/update.js'),
    ('Quais pastas o framework permite escrever?', 'lib/installer/policy.js'),
    ('Como remover instalação e manter especificações?', 'lib/commands/uninstall.js'),
    ('Qual comando exporta diagramas Mermaid?', 'lib/commands/export-diagrams.js'),
    ('Onde ficam dados do projeto e fases pendentes?', 'templates/state.json'),
    ('Quais são as dependências e requisitos de Node?', 'package.json'),
    ('Como funciona a escrita de skills e arquivos de entrada?', 'lib/installer/writer.js'),
    ('Como ocorre a seleção de times e agentes?', 'lib/installer/prompts.js'),
    ('Que tipos de projetos o ciclo forward aceita?', 'agents/reversa-forward/SKILL.md'),
    ('Qual é a licença do bundle impeccable?', 'agents/impeccable/LICENSE'),
]
result = []
for question, path in cases:
    matches = search(question, 10)
    rank = next((i for i, item in enumerate(matches, 1) if item['path'] == path), None)
    result.append({'question': question, 'expected_path': path, 'rank': rank})
report = {'label': 'avaliação exploratória manual não independente; fontes esperadas por caminho',
          'count': len(cases), 'recall_at_10': sum(r['rank'] is not None for r in result) / len(result),
          'recall_at_5': sum(r['rank'] is not None and r['rank'] <= 5 for r in result) / len(result),
          'cases': result}
(OUT / 'holdout.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
