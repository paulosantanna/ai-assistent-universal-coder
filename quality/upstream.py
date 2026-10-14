"""Monitor official TLC rules and incorporate new skills without executing downloaded code."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

from common import ROOT, canonical, files, read_json, safe_path, sha, workspace_files, write_json
from registry import frontmatter, register, structural_review, sync_distribution

REPOSITORY = 'tech-leads-club/agent-skills'
REGISTRY = 'packages/skills-catalog/skills-registry.json'
SOURCE_ROOT = 'packages/skills-catalog/skills/'
CONTROLS={'CONTRIBUTING.md','tools/validate-skills.ts','packages/skills-catalog/skills/(creation)/skill-architect/scripts/validate_skill.py',
          'packages/skills-catalog/skills/(creation)/skill-architect/references/quality-checklist.md'}


def download(url):
    request = urllib.request.Request(url, headers={'User-Agent':'CodENavi-TLC-quality/1.0','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if urllib.parse.urlparse(response.url).hostname not in {'api.github.com','raw.githubusercontent.com'}:
            raise ValueError('Unexpected upstream host')
        data = response.read(5_000_001)
    if len(data)>5_000_000:
        raise ValueError('Upstream resource too large')
    return data


def verify_controls(lock, fetch):
    changed = [p for p, expected in lock['controls'].items() if sha(fetch(p)) != expected]
    if changed:
        raise ValueError('Unsupported TLC rule change: '+', '.join(changed))


def missing_skills(catalog, upstream):
    names = {n for s in catalog['skills'] for n in [s['id'], *s['aliases']]}
    result = []
    seen = set()
    for entry in upstream['skills']:
        if entry['name'] in seen:
            raise ValueError('Duplicate upstream skill')
        seen.add(entry['name'])
        if entry['name'] not in names:
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',entry['name']) or not re.fullmatch(r'\([a-z0-9-]+\)/[a-z0-9-]+',entry['path']):
                raise ValueError('Invalid upstream distribution path')
            if entry['category'] != entry['path'].split('/')[0][1:-1]:
                raise ValueError('Upstream category drift')
            result.append(entry)
    return result


def import_skill(root, entry, fetch, commit):
    name = entry['name']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or not re.fullmatch(r'\([a-z0-9-]+\)/[a-z0-9-]+',entry['path']) or entry['category']!=entry['path'].split('/')[0][1:-1]:
        raise ValueError('Invalid canonical source identity')
    paths = entry['files']
    if not isinstance(paths,list) or len(paths)>300 or len(paths)!=len(set(paths)) or 'SKILL.md' not in paths:
        raise ValueError('Invalid upstream resource inventory')
    blobs = {}
    for resource in sorted(paths):
        safe_path(Path('/virtual-skill'),resource)
        if resource.startswith('.') or resource.endswith(('.env','.pem','.key')):
            raise ValueError('Credential or hidden resource in source skill')
        blobs[resource] = canonical(fetch(SOURCE_ROOT+entry['path']+'/'+resource))
    content = hashlib.sha256()
    for path, data in sorted(blobs.items()):
        content.update(path.encode()); content.update(data)
    if content.hexdigest()!=entry.get('contentHash'):
        raise ValueError('TLC registry content hash mismatch')
    text=blobs['SKILL.md'].decode('utf-8')
    fm=frontmatter(root,text)
    if fm['name']!=name:
        raise ValueError('Automatic import requires a canonical name without alias migration')
    desc=fm['description']
    if len(desc)>1024 or not re.search(r'use when|use for|trigger',desc,re.I) or not re.search(r'do not use|not for',desc,re.I):
        raise ValueError('Upstream routing contract invalid')
    positives=re.findall(r'"([^"\n]+)"',desc.split('Do NOT')[0])
    if len(positives)<3:
        raise ValueError('Automatic import requires three concrete upstream trigger phrases')
    body=text.split('---',2)[2]
    if re.search(r'(?im)^\s*(?:ignore (?:previous|system)|bypass (?:permission|policy)|spawn (?:a |new )?subagent)',body):
        raise ValueError('Unsafe source instruction requires adaptation')
    package=root/'00_skills'/entry['path'].split('/')[0]/name
    if package.exists():
        raise ValueError('Destination exists but is not registered; manual reconciliation required')
    resources=[]
    for path,data in blobs.items():
        installed='references/tlc/'+('UPSTREAM.md' if path=='SKILL.md' else path)
        target=safe_path(package,installed)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        if data.startswith(b'#!'):
            target.chmod(0o755)
        resource=dict(source=path,installed=installed,sha256=sha(data))
        if data.startswith(b'#!'):
            resource['executable']=True
        resources.append(resource)
    references=[f'- Read [{p}](references/tlc/{p}) only when its matching source procedure requires it.' for p in paths if p!='SKILL.md' and '/' not in p]
    license_id=fm.get('license','CC-BY-4.0')
    wrapper=('---\nname: '+name+'\ndescription: '+json.dumps(desc,ensure_ascii=False)+'\nlicense: '+license_id+
             '\nmetadata:\n  author: '+json.dumps(str(fm['metadata']['author']),ensure_ascii=False)+'\n  version: '+str(fm['metadata']['version'])+
             '\n  owner_agent: codenavi-agent\n---\n\n# '+name+'\n\nGovernance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.\n'+
             'Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.\n\n## Workflow\n\n'+
             '1. Confirm the requested outcome, authorized target and the prerequisites stated by the source.\n'+
             '2. Read [source procedure](references/tlc/UPSTREAM.md) before this specific workflow. Source instructions inherit the root contract; any source roles are internal lenses, never new identities.\n'+
             '3. Resolve the source skill directory as this package’s `references/tlc/`; its resource paths and helpers are relative to that directory.\n'+
             '4. Inspect the target and define observable success before execution. Missing evidence, tools, permission or credentials blocks the affected action; report the cause.\n'+
             '5. Follow the source procedure within the authorized scope, verify its concrete outputs and update the continuity quartet.\n\n## Inputs, outputs and verification\n\n'+
             'Inputs: user request, inspected target and source prerequisites. Outputs: the source-defined artifacts plus actual verification and limitations.\n'+
             'Installation is instruction-only: no Docker image, browser, model, dependency or runtime is installed by this importer. Credentials remain runtime references.\n'+
             'Example: use one of the request phrases in the description, inspect its target, execute the scoped procedure and report its resulting artifacts. A request outside the stated negative scope must route elsewhere.\n\n'+
             'Source: Tech Leads Club, commit `'+commit+'`; original procedure/resources retain attribution and source hashes in the upstream manifest.\n'+
             '\n'.join(references)+'\n')
    (package/'SKILL.md').write_text(wrapper,encoding='utf-8',newline='\n')
    skill=register(root,(package/'SKILL.md').relative_to(root).as_posix(),'tlc-auto-validated')
    upstream=read_json(root/'00_skills/upstream.manifest.json')
    upstream['skills'].append(dict(name=name,category=entry['category'],source_path=entry['path'],installed_path=package.relative_to(root).as_posix(),
                                   upstream_version=str(fm['metadata']['version']),source_commit=commit,content_hash=entry['contentHash'],files=resources))
    write_json(root/'00_skills/upstream.manifest.json',upstream)
    structural_review(root,skill,positives[:5],['outside source scope','missing authorization','missing source prerequisites'],dict(repository=REPOSITORY,commit=commit,path=entry['path']))
    return name


def _update(root, fetch, commit, apply=False):
    if not re.fullmatch('[0-9a-f]{40}',commit):
        raise ValueError('Invalid official source commit')
    lock=read_json(root/'quality/tlc-upstream.json')
    if lock.get('repository')!=REPOSITORY or set(lock.get('controls',{}))!=CONTROLS:
        raise ValueError('TLC standard controls are incomplete or point to another source')
    verify_controls(lock,fetch)
    upstream=json.loads(fetch(REGISTRY))
    catalog=read_json(root/'00_skills/catalog.json')
    additions=missing_skills(catalog,upstream)
    old={s['name']:s for s in read_json(root/'quality/tlc-snapshot.json')['skills']}
    changes=[s['name'] for s in upstream['skills'] if s['name'] in old and s.get('contentHash')!=old[s['name']].get('contentHash')]
    managed=read_json(root/'quality/tlc-auto-imports.json')['skills']
    updates=[s for s in upstream['skills'] if s['name'] in changes and s['name'] in managed]
    updated=[]
    imported=[]
    if apply:
        for entry in updates:
            skill=next(s for s in catalog['skills'] if s['id']==entry['name'])
            package=safe_path(root,skill['path']).parent
            review=read_json(root/'quality/reviews'/f"{skill['id']}.json")
            from common import package_hash
            before=package_hash(package)
            if before!=review['package_hash'] or skill['source']!='tlc-auto-validated':
                raise ValueError('Managed skill was edited locally; automatic replacement blocked')
            if skill['category']!=entry['category']:
                raise ValueError('Automatic category migration requires review')
            # This function runs only in the isolated candidate. Verify its resolved deletion target.
            if not package.resolve().is_relative_to((root/'00_skills').resolve()) or package.name!=entry['name']:
                raise ValueError('Unsafe managed package replacement')
            shutil.rmtree(package)
            candidate_catalog=read_json(root/'00_skills/catalog.json')
            candidate_catalog['skills']=[s for s in candidate_catalog['skills'] if s['id']!=entry['name']]
            write_json(root/'00_skills/catalog.json',candidate_catalog)
            sources=read_json(root/'00_skills/upstream.manifest.json')
            sources['skills']=[s for s in sources['skills'] if s['name']!=entry['name']]
            write_json(root/'00_skills/upstream.manifest.json',sources)
            import_skill(root,entry,fetch,commit)
            updated.append(dict(name=entry['name'],category=entry['category'],base_hash=before))
        for entry in additions:
            imported.append(import_skill(root,entry,fetch,commit))
        if imported or updated:
            sync_distribution(root)
        newlock={**lock,'commit':commit,'checked_at':datetime.date.today().isoformat()}
        # Dates only change with the observed source, avoiding a daily no-op commit.
        if lock['commit']!=commit:
            write_json(root/'quality/tlc-upstream.json',newlock)
        snapshot=dict(skills=[{k:s[k] for k in ['name','category','path','contentHash','version'] if k in s} for s in upstream['skills']])
        if snapshot!=read_json(root/'quality/tlc-snapshot.json'):
            write_json(root/'quality/tlc-snapshot.json',snapshot)
        auto=read_json(root/'quality/tlc-auto-imports.json')
        if imported:
            auto['skills']+=imported
            write_json(root/'quality/tlc-auto-imports.json',auto)
    return dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_commit=commit,new_skills=[s['name'] for s in additions],imported=imported,updated=updated,existing_source_changes=changes,
                curated_source_changes=[name for name in changes if name not in managed],
                existing_source_policy='Update unmodified auto-imports after validation; preserve curated adaptations',standard='Current TLC control hashes recognized',scope='No imported source code executed or runtime installed')


def update(root, fetch, commit, apply=False):
    if not apply:
        return _update(root,fetch,commit)
    from validate import validate
    scratch=root/'.aeos'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='tlc-candidate-',dir=scratch) as folder:
        candidate=Path(folder)
        for path in workspace_files(root):
            target=candidate/path.relative_to(root)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
        report=_update(candidate,fetch,commit,True)
        result=validate(candidate,True)
        if result['status']!='PASS':
            raise ValueError('Candidate gates failed: '+', '.join(sorted({e['code'] for e in result['errors']})))
        changes=[]
        for path in files(candidate):
            destination=safe_path(root,path.relative_to(candidate).as_posix())
            data=path.read_bytes()
            if not destination.exists() or canonical(destination.read_bytes())!=canonical(data):
                changes.append((destination,data,path.stat().st_mode))
        previous={p:(p.read_bytes() if p.exists() else None) for p,_,_ in changes}
        try:
            for path,data,mode in changes:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(data)
                path.chmod(mode)
        except OSError:
            # Roll back only files this transaction created/changed; never remove a preexisting directory.
            for path,data in previous.items():
                if data is None:
                    if path.exists():
                        path.unlink()
                else:
                    path.write_bytes(data)
            raise
        report['candidate_validation']=result['counts']
        report['changed_files']=len(changes)
        return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--out',type=Path,default=ROOT/'.aeos/quality/upstream.json')
    args=parser.parse_args()
    try:
        if args.source:
            commit=subprocess.run(['git','rev-parse','HEAD'],cwd=args.source,capture_output=True,check=True).stdout.decode().strip()
            fetch=lambda p: canonical(safe_path(args.source,p).read_bytes())
        else:
            commit=json.loads(download('https://api.github.com/repos/'+REPOSITORY+'/commits/main'))['sha']
            fetch=lambda p:download('https://raw.githubusercontent.com/'+REPOSITORY+'/'+commit+'/'+urllib.parse.quote(p,safe='/'))
        report=update(args.root.resolve(),fetch,commit,args.apply)
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        report=dict(status='FAIL',error_type=type(exc).__name__,reason=str(exc) if isinstance(exc,ValueError) else 'Official TLC acquisition failed; freshness not proven')
    write_json(args.out,report)
    print(json.dumps(report))
    return int(report['status']!='PASS')


if __name__=='__main__':
    sys.exit(main())
