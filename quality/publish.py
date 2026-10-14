"""Apply only the bounded, validated TLC update artifact in a separate publisher job."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

from common import ROOT, artifact_sha, package_hash, read_json, safe_path

METADATA = {'00_skills/catalog.json','00_skills/INDEX.md','00_skills/skills.registry.yaml','00_skills/upstream.manifest.json',
            'quality/tlc-upstream.json','quality/tlc-snapshot.json','quality/tlc-auto-imports.json'}


def allowed(path, additions):
    if path in METADATA:
        return True
    for item in additions:
        name=item['name']
        package='00_skills/('+item['category']+')/'+name+'/'
        if path.startswith(package) or path=='.agents/skills/'+name+'/SKILL.md' or path=='quality/reviews/'+name+'.json':
            return '..' not in path.split('/') and '\\' not in path
    return False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact',type=Path)
    args=parser.parse_args()
    manifest=read_json(args.artifact/'manifest.json')
    patch=(args.artifact/'update.patch').read_bytes()
    if artifact_sha(patch)!=manifest['patch_sha256'] or manifest.get('validation')!='PASS':
        raise ValueError('Update artifact hash or validation mismatch')
    current=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip()
    if current!=manifest['base_sha']:
        raise ValueError('Master advanced after candidate validation; regenerate candidate')
    if not patch:
        print('No upstream changes to publish')
        return 0
    if re.search(rb'(?m)^(?:new file mode|old mode|new mode) (?:120000|160000)$',patch):
        raise ValueError('Automatic artifact cannot introduce symlinks or submodules')
    stats=subprocess.run(['git','apply','--numstat','-z','-'],cwd=ROOT,input=patch,capture_output=True,check=True).stdout
    updates=manifest.get('updates',[])
    managed=read_json(ROOT/'quality/tlc-auto-imports.json')['skills'] if updates else []
    catalog={s['id']:s for s in read_json(ROOT/'00_skills/catalog.json')['skills']} if updates else {}
    for item in updates:
        if item['name'] not in managed:
            raise ValueError('Publisher cannot update a curated existing skill')
        if item['name'] not in catalog or catalog[item['name']].get('source')!='tlc-auto-validated' or catalog[item['name']]['category']!=item['category']:
            raise ValueError('Managed update does not match the published canonical catalog')
        package=safe_path(ROOT,'00_skills/('+item['category']+')/'+item['name'])
        if package_hash(package)!=item['base_hash']:
            raise ValueError('Managed skill changed after candidate preparation')
    paths=[]
    for row in stats.split(b'\0'):
        if not row:
            continue
        added,deleted,path=row.decode().split('\t',2)
        if path not in METADATA and deleted not in {'0','-'} and not allowed(path,updates):
            raise ValueError('Automatic update cannot remove existing package resources')
        safe_path(ROOT,path)
        if not allowed(path,manifest['additions']+updates):
            raise ValueError('Artifact path outside automatic update scope')
        paths.append(path)
    for item in manifest['additions']:
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',item['name']) or not re.fullmatch('[a-z0-9-]+',item['category']):
            raise ValueError('Invalid addition identity')
        if (ROOT/'00_skills'/('('+item['category']+')')/item['name']).exists():
            raise ValueError('Automatic publisher cannot replace an existing skill')
    subprocess.run(['git','apply','--check','-'],cwd=ROOT,input=patch,check=True)
    subprocess.run(['git','apply','-'],cwd=ROOT,input=patch,check=True)
    subprocess.run(['git','add','--',*paths],cwd=ROOT,check=True)
    # Never import or execute code from the update artifact in this write-enabled job.
    subprocess.run(['git','commit','-m','chore(skills): incorporate validated TLC updates'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['git','push','origin','HEAD:master'],cwd=ROOT,check=True)
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip()
    remote=subprocess.run(['git','ls-remote','origin','refs/heads/master'],cwd=ROOT,capture_output=True,check=True).stdout.decode().split()[0]
    if head!=remote:
        raise ValueError('Remote publication SHA differs from the validated update')
    print('Published verified TLC update: '+head)
    return 0


if __name__=='__main__':
    sys.exit(main())
