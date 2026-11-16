import json
import re
from pathlib import Path
from scan import OUT, ROOT, TARGET, scan

before = json.loads((OUT / 'inventory.json').read_text(encoding='utf-8'))
after = scan(persist=False, collect_signals=False, verbose=False)
old = {r['name']: r for r in before['repositories']}
new = {r['name']: r for r in after['repositories']}
errors = []
if set(old) != set(new):
    errors.append('Cobertura de diretórios mudou')
for name in old.keys() & new.keys():
    if old[name]['source_fingerprint'] != new[name]['source_fingerprint']:
        errors.append('Fontes mudaram: ' + name)
    if old[name]['git'] != new[name]['git']:
        errors.append('Estado Git mudou: ' + name)
    if new[name]['errors']:
        errors.append('Erro de leitura: ' + name)
    if not (OUT / 'repositorios' / (name + '.md')).is_file():
        errors.append('Nota ausente: ' + name)
for path in OUT.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if not link.startswith(('http:', 'https:', '#')) and not (path.parent / link.split('#')[0]).exists():
            errors.append('Link ausente: ' + str(path.relative_to(OUT)) + ' → ' + link)
result = {'status': 'PASS' if not errors else 'FAIL', 'directories': len(new), 'files': sum(len(r['files']) for r in new.values()), 'errors': errors, 'checked_at': after['captured_at'], 'scope': 'cobertura, fingerprints, Git, erros e links; sem validação semântica ou execução dos projetos'}
(OUT / 'verificacao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(bool(errors))
