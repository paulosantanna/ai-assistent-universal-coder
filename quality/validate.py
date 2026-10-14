"""Deterministic TLC/CodENavi gates. Never execute imported skill helpers."""
import argparse
import ast
import collections
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

from common import ROOT, architect, files, module, package_hash, read_json, safe_path, sha, workspace_files, write_json
from protocol import probe


def distribution(root, catalog):
    errors = []
    declared = {s['path'] for s in catalog['skills']}
    found = {p.relative_to(root).as_posix() for p in workspace_files(root)
             if re.fullmatch(r'00_skills/\([a-z0-9-]+\)/[a-z0-9-]+/SKILL\.md', p.relative_to(root).as_posix())}
    for p in sorted(found ^ declared):
        errors.append({'code': 'unregistered-or-missing-skill', 'path': p})
    names = [name for s in catalog['skills'] for name in [s['id'], *s['aliases']]]
    if len(names) != len(set(names)):
        errors.append({'code': 'duplicate-discovery-name', 'path': '00_skills/catalog.json'})
    native = {p.parent.name for p in (root/'.agents/skills').glob('*/SKILL.md')}
    if native != set(names):
        errors.append({'code': 'native-discovery-drift', 'path': '.agents/skills'})
    registry = (root/'00_skills/skills.registry.yaml').read_text(encoding='utf-8-sig')
    ids = re.findall(r'^- id: (.+)$', registry, re.M)
    if len(ids) != len(set(ids)) or set(ids) != set(names):
        errors.append({'code': 'registry-distribution-drift', 'path': '00_skills/skills.registry.yaml'})
    expected={name:s for s in catalog['skills'] for name in [s['id'],*s['aliases']]}
    for item in yaml.safe_load(registry).get('skills',[]):
        skill=expected.get(item['id'])
        if skill and (item.get('path')!=skill['path'] or item.get('mission')!=skill['description']):
            errors.append({'code':'registry-routing-drift','path':'00_skills/skills.registry.yaml'})
    for skill in catalog['skills']:
        entry = safe_path(root, skill['path'])
        if entry.parent.parent.name != '('+skill['category']+')':
            errors.append({'code': 'category-drift', 'path': skill['path']})
    return errors


def reviews(root, catalog):
    errors, assessed = [], 0
    baseline = read_json(root/'quality/skills-baseline.json')['skills']
    for s in catalog['skills']:
        path = safe_path(root, s['path']).parent
        digest = package_hash(path)
        if baseline.get(s['id']) == digest:
            continue
        review = root/'quality/reviews'/f"{s['id']}.json"
        if not review.is_file():
            errors.append({'code': 'new-or-changed-skill-needs-review', 'path': s['path']})
            continue
        data = read_json(review)
        phrases = data.get('positive_triggers', [])
        negative = data.get('negative_scope', [])
        valid = (data.get('package_hash') == digest and len(phrases) >= 3 and len(set(phrases)) == len(phrases)
                 and all(isinstance(p, str) and p.strip() in s['description'] for p in phrases)
                 and len(negative) >= 3 and len(set(negative)) == len(negative)
                 and data.get('verification', {}).get('kind') in {'structural-and-syntax', 'behavioral'})
        if not valid:
            errors.append({'code': 'invalid-skill-review', 'path': review.relative_to(root).as_posix()})
        else:
            assessed += 1
        for resource in files(path):
            if resource.suffix=='.md' and '/references/tlc/' not in resource.as_posix():
                text=resource.read_text(encoding='utf-8-sig')
                if len(text.splitlines())>300 and not re.search(r'table of contents|sum[aá]rio|contents',text,re.I):
                    errors.append({'code':'long-module-needs-contents','path':resource.relative_to(root).as_posix()})
    return errors, assessed


def schema_valid(value):
    """Validate the supported object-schema structure, not arbitrary schema vocabularies."""
    if not isinstance(value, dict) or value.get('type') != 'object':
        return False
    props, required = value.get('properties', {}), value.get('required', [])
    if not isinstance(props, dict) or not isinstance(required, list) or any(not isinstance(k,str) for k in required) or len(required) != len(set(required)):
        return False
    if any(not isinstance(k, str) or k not in props for k in required):
        return False
    if not isinstance(value.get('additionalProperties', False), (dict, bool)):
        return False
    types = {'string', 'number', 'integer', 'boolean', 'object', 'array', 'null'}
    for prop in props.values():
        if not isinstance(prop, dict):
            return False
        t = prop.get('type')
        if t is not None and not (t in types if isinstance(t, str) else isinstance(t, list) and all(x in types for x in t)):
            return False
        if t == 'object' and not schema_valid(prop):
            return False
        if t == 'array' and not isinstance(prop.get('items'), dict):
            return False
    return True


def tools_valid(tools):
    if not isinstance(tools, list) or not tools:
        return False
    names = []
    for tool in tools:
        if not isinstance(tool, dict) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', tool.get('name', '')):
            return False
        if not isinstance(tool.get('description'), str) or not tool['description'].strip() or not schema_valid(tool.get('inputSchema')):
            return False
        names.append(tool['name'])
    return len(names) == len(set(names))


def capabilities(root, inventory, runtime=False):
    errors, states = [], []
    listed = inventory.get('mcps', [])
    actual = {p.name for p in root.glob('*-mcp') if p.is_dir()}
    paths = [c.get('path') for c in listed]
    if len(paths) != len(set(paths)) or actual != set(paths):
        errors.append({'code': 'mcp-inventory-drift', 'path': 'quality/capabilities.json'})
    legacy = {'kinghost-control-mcp', 'kinghost-commerce-mcp', 'dark-videos-pipeline-mcp', 'continuous-training-mcp'}
    for kind, entries in [('mcp', listed), ('lsp', inventory.get('lsps', []))]:
        seen = set()
        for c in entries:
            path = safe_path(root, c['path'])
            valid = (c.get('id') not in seen and c.get('owner') == 'codenavi-agent'
                     and c.get('secret_policy') == 'runtime-references-only' and path.exists())
            seen.add(c.get('id'))
            state = c.get('state')
            if state in {'adapter', 'quarantined'}:
                valid = valid and kind == 'mcp' and c['path'] in legacy and bool(c.get('reason')) and c.get('baseline_hash') == package_hash(path)
                status = 'ADAPTER' if state == 'adapter' else 'QUARANTINED'
                if runtime and state == 'adapter':
                    p = subprocess.run(c['smoke'], cwd=path, env=probe.environment(), capture_output=True, timeout=15)
                    response = json.loads(p.stdout)
                    valid = valid and p.returncode == 0 and response.get('health', {}).get('success') is True
            elif state == 'active':
                expected = 'jsonrpc-stdio' if kind == 'mcp' else 'lsp-content-length'
                command = c.get('command', [])
                valid = valid and c.get('protocol') == expected and isinstance(command, list) and len(command) >= 2
                valid = valid and all(isinstance(arg,str) for arg in command) and c.get('entrypoint') in command
                valid = valid and Path(command[0]).name.lower() not in {'sh','bash','cmd','cmd.exe','powershell','pwsh'} and not any(arg in {'-c','-e','--eval'} for arg in command)
                valid = valid and safe_path(path, c.get('entrypoint', '')).is_file()
                if kind == 'mcp':
                    valid = valid and tools_valid(c.get('tools'))
                else:
                    languages,extensions=c.get('languages'),c.get('file_extensions')
                    valid = valid and isinstance(languages,list) and bool(languages) and all(isinstance(x,str) and x.strip() for x in languages)
                    valid = valid and isinstance(extensions,list) and bool(extensions) and all(isinstance(x,str) and re.fullmatch(r'\.[A-Za-z0-9_.-]+',x) for x in extensions)
                status = 'STATIC_ONLY'
                if runtime and valid:
                    result = probe(command, path, kind)
                    valid = result['passed'] and (kind != 'mcp' or (tools_valid(result['tools']) and result['tools'] == c['tools']))
                    status = 'PROTOCOL_PASS' if valid else 'PROTOCOL_FAIL'
            else:
                valid, status = False, 'INVALID_STATE'
            if not valid:
                errors.append({'code': f'{kind}-contract-failed', 'path': c['path']})
            states.append({'id': c.get('id'), 'kind': kind, 'state': status, 'reason': c.get('reason')})
    # Explicit LSP descriptors belong to the inventory; docs and editor extensions are not servers.
    declared = {c['path'] for c in inventory.get('lsps', [])}
    discovered = {p.relative_to(root).as_posix() for p in root.glob('*-lsp') if p.is_dir()}
    if discovered != declared:
        errors.append({'code': 'lsp-inventory-drift', 'path': 'quality/capabilities.json'})
    configs=[]
    for p in workspace_files(root):
        if '/references/' in p.as_posix() or p.suffix not in {'.json','.toml','.yaml','.yml'}:
            continue
        named=p.name in {'lsp.json','.lsp.json','mcp.json','.mcp.json','mcp-config.json'}
        declared_keys=re.search(r'(?m)(?:["\'](?:mcpServers|mcp_servers|languageServers|languageServer|lspServers)["\']\s*:|^\s*\[mcp_servers[.\]])',p.read_text(encoding='utf-8-sig'))
        if named or declared_keys:
            configs.append(p)
    registered = set(inventory.get('configuration_files', []))
    for config in configs:
        if config.relative_to(root).as_posix() not in registered:
            errors.append({'code': 'unregistered-server-config', 'path': config.relative_to(root).as_posix()})
    return errors, states


def security_and_syntax(root):
    errors, counts = [], collections.Counter()
    pattern = re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,255}|github_pat_[A-Za-z0-9_]{50,255}|sk-(?:proj-)?[A-Za-z0-9_-]{40,255}|(?:AKIA|ASIA)[A-Z0-9]{16})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    for path in workspace_files(root):
        if path.is_symlink():
            errors.append({'code': 'symlink-not-allowed', 'path': path.relative_to(root).as_posix()})
            continue
        data = path.read_bytes()
        rel = path.relative_to(root).as_posix()
        if path.name in {'.env', 'Cookies', 'auth.json', 'credentials.json', 'id_rsa', 'id_ed25519'}:
            errors.append({'code': 'credential-artifact', 'path': rel})
        if pattern.search(data):
            errors.append({'code': 'possible-secret', 'path': rel})
        if path.suffix == '.py':
            try:
                ast.parse(data, filename=rel)
                counts['python'] += 1
            except (SyntaxError, ValueError):
                errors.append({'code': 'python-syntax', 'path': rel})
        if path.suffix in {'.js', '.mjs', '.cjs'}:
            p = subprocess.run(['node', '--check', str(path)], capture_output=True, timeout=15)
            if p.returncode:
                errors.append({'code': 'javascript-syntax', 'path': rel})
            else:
                counts['javascript'] += 1
    return errors, dict(counts)


def executable_resources(root):
    errors=[]
    for source in read_json(root/'00_skills/upstream.manifest.json')['skills']:
        package=safe_path(root,source['installed_path'])
        for resource in source['files']:
            if not resource.get('executable'):
                continue
            path=safe_path(package,resource['installed'])
            valid=bool(path.stat().st_mode & 0o111)
            if sys.platform=='win32':
                if not (root/'.git').exists():
                    continue  # The exact exported mode is enforced by the Linux CI checkout.
                indexed=subprocess.run(['git','ls-files','--stage','--',path.relative_to(root).as_posix()],cwd=root,capture_output=True,check=True).stdout
                valid=indexed.startswith(b'100755 ')
            if not valid:
                errors.append({'code':'source-helper-not-executable','path':path.relative_to(root).as_posix()})
    return errors


def validate(root, runtime=False):
    # Bound all catalog/source paths before the reused validator can read a resource.
    catalog = read_json(root/'00_skills/catalog.json')
    for s in catalog['skills']:
        safe_path(root,s['path'])
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s['id']) or any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',n) for n in s['aliases']):
            raise ValueError('Unsafe skill identity')
    for s in read_json(root/'00_skills/upstream.manifest.json')['skills']:
        package=safe_path(root,s['installed_path'])
        for resource in s['files']:
            safe_path(package,resource['installed'])
    local = module(root/'00_skills/(creation)/skill-factory/scripts/validate-workspace.py', 'workspace_validator')
    base = local.validate(root)
    errors = [{'code': 'skill-contract', 'path': e['scope']} for e in base['errors']]
    catalog = read_json(root/'00_skills/catalog.json')
    errors += distribution(root, catalog)
    review_errors, reviewed = reviews(root, catalog)
    errors += review_errors
    capability_errors, states = capabilities(root, read_json(root/'quality/capabilities.json'), runtime)
    errors += capability_errors
    syntax_errors, syntax = security_and_syntax(root)
    errors += syntax_errors
    errors += executable_resources(root)
    errors += workflows(root)
    lock = read_json(root/'quality/tlc-upstream.json')
    if not re.fullmatch('[0-9a-f]{40}', lock.get('commit', '')) or lock.get('repository') != 'tech-leads-club/agent-skills':
        errors.append({'code': 'invalid-tlc-source-lock', 'path': 'quality/tlc-upstream.json'})
    return {'status': 'FAIL' if errors else 'PASS', 'scope': 'Structural, integrity, distribution, syntax and declared protocol gates; not a certification of enterprise effectiveness',
            'counts': {**base['counts'], **syntax, 'changed_skills_assessed': reviewed}, 'capabilities': states,
            'categories':dict(sorted(collections.Counter(s['category'] for s in catalog['skills']).items())),
            'lsp_count': len(read_json(root/'quality/capabilities.json')['lsps']), 'errors': errors, 'warnings': base['warnings'], 'tlc_commit': lock['commit']}


def workflows(root):
    errors=[]
    for path in (root/'.github/workflows').glob('*.y*ml'):
        try:
            data=yaml.load(path.read_text(encoding='utf-8'),Loader=yaml.BaseLoader)
            if not isinstance(data,dict) or not data.get('on') or not isinstance(data.get('jobs'),dict) or not data['jobs']:
                raise ValueError('Invalid workflow envelope')
            if data.get('permissions',{}).get('contents')!='read':
                raise ValueError('Workflow must default to read-only contents')
            for name,job in data['jobs'].items():
                for step in job.get('steps',[]):
                    action=step.get('uses','')
                    if action and not action.startswith('./') and not re.fullmatch('[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[a-f0-9]{40}',action):
                        raise ValueError('Third-party action is not pinned')
                    if step.get('continue-on-error')=='true':
                        raise ValueError('Failure suppression is forbidden')
                if job.get('continue-on-error')=='true':
                    raise ValueError('Failure suppression is forbidden')
        except (yaml.YAMLError,ValueError,TypeError,AttributeError):
            errors.append({'code':'workflow-contract','path':path.relative_to(root).as_posix()})
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, default=ROOT/'.aeos/quality')
    parser.add_argument('--runtime', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        report = validate(args.root.resolve(), args.runtime)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        report = {'status': 'FAIL', 'errors': [{'code': 'gate-execution-failed', 'detail': type(exc).__name__}]}
    write_json(args.out/'report.json', report)
    (args.out/'summary.md').write_text('# Capability quality: '+report['status']+'\n\n'+json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'counts': report.get('counts'), 'errors': report['errors'], 'lsp_count': report.get('lsp_count')}))
    return int(report['status'] != 'PASS')


if __name__ == '__main__':
    sys.exit(main())
