#!/usr/bin/env python3
"""Registra uma skill canônica na descoberta do workspace.

Faz a manutenção de três superfícies que a validação exige em sincronia:

1. entrada de compatibilidade em ``skills/<id>/SKILL.md`` (aponta para o canônico);
2. entrada em ``00_skills/catalog.json`` (id, path, categoria, descrição, risk, sha256, linhas);
3. entrada em ``00_skills/skills.registry.yaml``.

A entrada canônica ``00_skills/(categoria)/<id>/SKILL.md`` é a fonte de verdade; este script
não a cria nem a edita. Faixa de risco é declarada por variável de ambiente opcional
``SKILL_RISK`` (``medium`` por padrão, ``high`` para skills que bloqueiam ou reiniciam produção).

Uso:
    python "00_skills/(creation)/skill-factory/scripts/register-skill.py" <id> [<id> ...]
    python "00_skills/(creation)/skill-factory/scripts/register-skill.py" --all <categoria>
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CATALOG_ROOT = ROOT / '00_skills'
COMPAT_ROOT = ROOT / 'skills'
# Descoberta nativa exigida pela validação, além da entrada de compatibilidade.
NATIVE_ROOTS = (ROOT / '.agents/skills', ROOT / '.codex/skills')
CATEGORIES = ('architecture', 'cloud', 'creation', 'decision-making', 'design', 'development',
              'gtm', 'learning', 'mapping', 'monitoring', 'performance', 'quality', 'security',
              'tooling', 'web-automation')
RISK_HIGH = {'documentary-adversarial-judge', 'documentary-factory'}


def frontmatter(path):
    """Lê name/description do frontmatter sem depender de YAML externo."""
    text = path.read_text(encoding='utf-8-sig')
    if not text.startswith('---'):
        raise ValueError(f'{path}: frontmatter ausente')
    block = text.split('---', 2)[1]
    fields = {}
    key = None
    for raw in block.splitlines():
        if not raw.strip():
            continue
        match = re.match(r'^(\w+):\s*(.*)$', raw)
        if match:
            key, value = match.group(1), match.group(2).strip()
            fields[key] = value
        elif key:
            fields[key] += ' ' + raw.strip()
    for name in ('name', 'description'):
        if not fields.get(name):
            raise ValueError(f'{path}: campo {name} ausente no frontmatter')
    fields['description'] = fields['description'].strip().strip('"').strip("'").strip()
    return fields


def locate(skill_id):
    for category in CATEGORIES:
        candidate = CATALOG_ROOT / f'({category})' / skill_id / 'SKILL.md'
        if candidate.is_file():
            return category, candidate
    raise FileNotFoundError(f'skill canônica não encontrada: {skill_id}')


def write_compat(skill_id, meta):
    """Escreve a entrada de compatibilidade e a entrada de descoberta nativa.

    A validação exige que a descrição nativa seja idêntica à canônica e que o texto aponte
    para o pacote canônico — por isso as três superfícies recebem o mesmo corpo.
    """
    body = (
        '---\n'
        f'name: {skill_id}\n'
        f'description: "{meta["description"]}"\n'
        'license: CC-BY-4.0\n'
        'metadata:\n'
        '  author: AEOS\n'
        '  version: 1.0.0\n'
        '  owner_agent: codenavi-agent\n'
        '---\n\n'
        f'# {skill_id}\n\n'
        f'Read and follow `00_skills/({meta["category"]})/{skill_id}/SKILL.md` and its relevant '
        'local modules.\n\n'
        'Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent '
        'identity.\n')
    written = []
    for base in (COMPAT_ROOT, *NATIVE_ROOTS):
        if base is not COMPAT_ROOT and not base.is_dir():
            continue
        target = base / skill_id / 'SKILL.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')
        written.append(target)
    return written


def update_catalog(records):
    path = CATALOG_ROOT / 'catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    index = {entry['id']: entry for entry in catalog['skills']}
    added, updated = [], []
    for record in records:
        (updated if record['id'] in index else added).append(record['id'])
        index[record['id']] = record
    catalog['skills'] = sorted(index.values(), key=lambda item: item['id'])
    catalog['updated'] = records[0]['updated']
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return added, updated


def update_registry(records):
    path = CATALOG_ROOT / 'skills.registry.yaml'
    lines = path.read_text(encoding='utf-8').splitlines()
    ids = {record['id'] for record in records}
    kept, skip = [], False
    for line in lines:
        if line.startswith('- id:'):
            skip = line.split('- id:', 1)[1].strip() in ids
        if not skip:
            kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    for record in records:
        kept += [
            f"- id: {record['id']}",
            f"  path: {record['path']}",
            '  owner_agent: codenavi-agent',
            f"  risk_level: {record['risk_level']}",
            f"  mission: '{record['description'].replace(chr(39), chr(39) * 2)}'",
            '  capabilities: []',
        ]
    path.write_text('\n'.join(kept) + '\n', encoding='utf-8')


def main(argv):
    if len(argv) >= 2 and argv[0] == '--all':
        category = argv[1]
        directory = CATALOG_ROOT / f'({category})'
        skill_ids = sorted(path.parent.name for path in directory.glob('*/SKILL.md'))
    elif argv:
        skill_ids = argv
    else:
        print(__doc__)
        return 1

    risk_override = os.environ.get('SKILL_RISK', '').strip()
    records = []
    for skill_id in skill_ids:
        category, canonical = locate(skill_id)
        meta = frontmatter(canonical)
        if meta['name'] != skill_id:
            raise ValueError(f'{canonical}: name "{meta["name"]}" difere da pasta "{skill_id}"')
        digest = hashlib.sha256(canonical.read_bytes()).hexdigest()
        lines = len(canonical.read_text(encoding='utf-8-sig').splitlines())
        if lines > 100:
            raise ValueError(f'{canonical}: {lines} linhas excede o limite de 100')
        meta['category'] = category
        records.append({
            'id': skill_id,
            'aliases': [],
            'path': f'00_skills/({category})/{skill_id}/SKILL.md',
            'category': category,
            'description': meta['description'],
            'owner_agent': 'codenavi-agent',
            'risk_level': risk_override or ('high' if skill_id in RISK_HIGH else 'medium'),
            'runtime_binding': 'instruction_only',
            'source': 'workspace',
            'lines': lines,
            'sha256': digest,
            'updated': '2026-10-31',
        })
        for target in write_compat(skill_id, meta):
            print(f'entry   {target.relative_to(ROOT)}')

    added, updated = update_catalog(records)
    update_registry(records)
    print(f'catalog added={added} updated={updated}')
    print(f'registry synced: {len(records)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
