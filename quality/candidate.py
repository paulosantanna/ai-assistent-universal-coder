"""Prepare a bounded diff and provenance manifest after successful upstream gates."""
import argparse
from pathlib import Path
import subprocess
import sys

from common import ROOT, artifact_sha, read_json, write_json
from publish import allowed


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'.aeos/tlc-candidate')
    args=parser.parse_args()
    report=read_json(ROOT/'.aeos/quality/upstream.json')
    if report['status']!='PASS' or not report.get('candidate_validation'):
        raise ValueError('Candidate is missing successful full validation')
    snapshot=read_json(ROOT/'quality/tlc-snapshot.json')
    additions=[dict(name=s['name'],category=s['category']) for s in snapshot['skills'] if s['name'] in report['imported']]
    changes=subprocess.run(['git','status','--porcelain','-z','--untracked-files=all'],cwd=ROOT,capture_output=True,check=True).stdout.split(b'\0')
    paths=[row[3:].decode() for row in changes if row]
    updates=report.get('updated',[])
    if any(not allowed(path,additions+updates) for path in paths):
        raise ValueError('Candidate checkout has unrelated changes')
    if paths:
        subprocess.run(['git','add','--',*paths],cwd=ROOT,check=True)
    patch=subprocess.run(['git','diff','--cached','--binary','--full-index'],cwd=ROOT,capture_output=True,check=True).stdout
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'update.patch').write_bytes(patch)
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip()
    write_json(args.out/'manifest.json',dict(base_sha=head,source_commit=report['source_commit'],additions=additions,updates=updates,patch_sha256=artifact_sha(patch),validation='PASS'))
    print('Validated update artifact prepared; changed files: '+str(len(paths)))
    return 0


if __name__=='__main__':
    sys.exit(main())
