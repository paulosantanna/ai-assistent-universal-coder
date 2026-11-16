"""Compare the existing natural-language probes with hybrid retrieval."""
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT / 'rag-graph-laya-mcp'))
from app.reversa import retrieve

baseline = json.loads((OUT / 'holdout.json').read_text(encoding='utf-8'))
rows = []
for case in baseline['cases']:
    matches = retrieve(case['question'], 10, 'hybrid')['evidence']
    rank = next((i for i, item in enumerate(matches, 1) if item['path'] == case['expected_path']), None)
    rows.append({**case, 'lexical_rank': case['rank'], 'hybrid_rank': rank})
report = {'label': 'comparação exploratória não independente; caminho esperado não é o único possível',
          'count': len(rows), 'lexical_recall_at_10': baseline['recall_at_10'],
          'hybrid_recall_at_10': sum(x['hybrid_rank'] is not None for x in rows) / len(rows), 'cases': rows}
(OUT / 'hybrid-evaluation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
