import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
REPO = OUT.parents[1] / '02_repositorios/reversa'
folder = OUT / 'dataset-candidate'
manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
groups, seen, errors = {}, set(), []
for split in ('train', 'validation', 'test'):
    path = folder / (split + '.jsonl')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['files'][path.name]: errors.append('dataset hash: ' + split)
    rows = [json.loads(x) for x in raw.decode('utf-8').splitlines()]
    if len(rows) != manifest['counts'][split]: errors.append('count: ' + split)
    groups[split] = {r['provenance']['group'] for r in rows}
    for row in rows:
        p = row['provenance']
        source = (REPO / p['path']).read_bytes()
        if hashlib.sha256(source).hexdigest() != p['sha256']: errors.append('source drift: ' + p['path'])
        chunk = '\n'.join(source.decode('utf-8-sig').splitlines()[p['start_line']-1:p['end_line']])
        key = hashlib.sha256(chunk.encode('utf-8')).hexdigest()
        if key in seen: errors.append('duplicate chunk')
        seen.add(key)
        user = row['messages'][1]['content']
        answer = row['messages'][2]['content']
        if p['negative']:
            if 'Nenhuma fonte recuperada.' not in user or 'Não há evidência suficiente' not in answer: errors.append('negative contract')
        elif chunk not in user or chunk not in answer or '[1]' not in answer: errors.append('extractive contract')
        if row['review']['approved'] or p['human_reviewed']: errors.append('unexpected approval')
for i, left in enumerate(groups):
    for right in list(groups)[i+1:]:
        if groups[left] & groups[right]: errors.append('group leakage')
report = {'status': 'PASS' if not errors else 'FAIL', 'examples': len(seen), 'errors': errors,
          'limits': 'Formatação, rastreabilidade e grupos de caminhos; não mede qualidade das respostas ou independência entre projetos.'}
(folder / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
raise SystemExit(bool(errors))
