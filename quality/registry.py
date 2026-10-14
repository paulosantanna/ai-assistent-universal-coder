"""Synchronize one canonical catalog with native discovery and distribution pointers."""
import datetime
import json
from pathlib import Path
import re

from common import architect, package_hash, read_json, sha, write_json


def frontmatter(root, text):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text.replace('\r\n', '\n'), re.S)
    if not match:
        raise ValueError('Missing skill frontmatter')
    return architect(root).parse_frontmatter(match[1])[0]


def register(root, entry_path, source):
    path = root/entry_path
    text = path.read_text(encoding='utf-8')
    fm = frontmatter(root, text)
    catalog = read_json(root/'00_skills/catalog.json')
    if any(s['id'] == fm['name'] for s in catalog['skills']):
        raise ValueError('Canonical skill already registered')
    catalog['skills'].append(dict(id=fm['name'], aliases=[], path=entry_path, category=path.parent.parent.name[1:-1],
                                 description=fm['description'], owner_agent='codenavi-agent', risk_level='medium',
                                 runtime_binding='instruction_only', source=source, lines=len(text.splitlines()), sha256=sha(path.read_bytes())))
    catalog['skills'].sort(key=lambda s:s['id'])
    catalog['updated'] = datetime.date.today().isoformat()
    write_json(root/'00_skills/catalog.json', catalog)
    native = root/'.agents/skills'/fm['name']/'SKILL.md'
    native.parent.mkdir(parents=True, exist_ok=True)
    native.write_text('---\nname: '+fm['name']+'\ndescription: '+json.dumps(fm['description'],ensure_ascii=False)+
                      '\nlicense: '+str(fm.get('license','CC-BY-4.0'))+'\nmetadata:\n  author: '+json.dumps(str(fm['metadata']['author']))+
                      '\n  version: '+str(fm['metadata']['version'])+'\n  owner_agent: codenavi-agent\n---\n\n# '+fm['name']+
                      '\n\nRead and follow `'+entry_path+'` and its relevant local modules.\n\nGovernance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.\n',encoding='utf-8',newline='\n')
    return catalog['skills'][-1] if catalog['skills'][-1]['id']==fm['name'] else next(s for s in catalog['skills'] if s['id']==fm['name'])


def sync_distribution(root):
    catalog = read_json(root/'00_skills/catalog.json')
    path=root/'00_skills/skills.registry.yaml'
    existing=path.read_text(encoding='utf-8-sig') if path.exists() else 'skills:\n'
    names=set(re.findall(r'^- id: (.+)$',existing,re.M))
    registry = [existing.rstrip()]
    for s in catalog['skills']:
        for name in [s['id'], *s['aliases']]:
            if name in names:
                pattern=r'(?ms)^- id: '+re.escape(name)+r'\n.*?(?=^- id: |\Z)'
                block=re.search(pattern,registry[0])
                if block:
                    import yaml
                    current=yaml.safe_load('skills:\n'+block[0])['skills'][0]
                    if current.get('mission')!=s['description']:
                        revised=re.sub(r'^  mission: .*$',lambda m:'  mission: '+json.dumps(s['description'],ensure_ascii=False),block[0],flags=re.M)
                        registry[0]=registry[0][:block.start()]+revised+registry[0][block.end():]
                continue
            registry += ['- id: '+name, '  path: '+s['path'], '  owner_agent: codenavi-agent', '  risk_level: '+s['risk_level'],
                         '  mission: '+json.dumps(s['description'],ensure_ascii=False), '  capabilities: []']
    (root/'00_skills/skills.registry.yaml').write_text('\n'.join(registry)+'\n',encoding='utf-8',newline='\n')
    index = ['# Skills canônicas', '', 'Updated: '+catalog['updated'], 'Entry point: [contrato](STANDARD.md), [catálogo](catalog.json), [esteira](../quality/README.md).', '',
             f"{len(catalog['skills'])} pacotes canônicos. Adaptações herdam AGENTS.md; disponibilidade externa deve ser comprovada ao executar.", '']
    for category in sorted({s['category'] for s in catalog['skills']}):
        index += ['## '+category, '']
        for s in catalog['skills']:
            if s['category']==category:
                index.append('- ['+s['id']+']('+s['path'].removeprefix('00_skills/')+') — '+s['description'].split(' Use when')[0])
        index.append('')
    (root/'00_skills/INDEX.md').write_text('\n'.join(index),encoding='utf-8',newline='\n')


def structural_review(root, skill, positives, negatives, source):
    write_json(root/'quality/reviews'/f"{skill['id']}.json",dict(skill=skill['id'],package_hash=package_hash((root/skill['path']).parent),
               positive_triggers=positives, negative_scope=negatives, source=source,
               verification=dict(kind='structural-and-syntax',runtime_evaluated=False,routing='Static wording assessment; no measured trigger accuracy'),
               effectiveness='Not measured; structural acceptance does not establish enterprise performance'))
