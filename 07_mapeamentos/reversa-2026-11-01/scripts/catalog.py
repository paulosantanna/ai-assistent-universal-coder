import json
import re
from collections import Counter
from corpus import OUT, REPO

manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
files = manifest['files']
counts = Counter(x['path'].split('/')[0] for x in files)
lines = ['# Catálogo de fontes', '', 'Updated: 2026-11-01. Entry point: [README](README.md).', '', '## Cobertura por área', '']
lines += [f'- `{name}`: {count} arquivos indexados.' for name, count in sorted(counts.items())]
lines += ['', '## Catálogo de capacidades declaradas', '', 'As descrições abaixo são metadados declarados nos arquivos de origem; não constituem validação funcional nem autorização para instalar personas.', '', '| Capacidade | Fonte |', '|---|---|']
skills = sorted(x['path'] for x in files if re.fullmatch(r'agents/[^/]+/SKILL\.md', x['path']))
for path in skills:
    name = path.split('/')[1]
    lines.append(f'| {name} | [SKILL.md](../../02_repositorios/reversa/{path}) |')
lines += ['', '## Código executável', '', 'Referências por arquivo:']
for x in files:
    path = x['path']
    if path.startswith(('bin/', 'lib/', 'scripts/')):
        lines.append(f'- [{path}](../../02_repositorios/reversa/{path}) — {x["lines"]} linhas; SHA-256 `{x["sha256"]}`.')
lines += ['', 'A lista integral, inclusive arquivos de documentação e templates, está em [manifest.json](manifest.json), com linhas, bytes, hashes e exclusões.']
(OUT / 'CATALOGO.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(len(skills), 'capacidades catalogadas')
