"""Verify coverage, source drift, evidence contracts and generated local links."""
import csv
import json
import re
import time
from pathlib import Path
from scan import ROOT, OUT, TARGET, digest, save, scan


def verify():
    start = time.monotonic()
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    model = json.loads((OUT / 'mapa.json').read_text(encoding='utf-8'))
    before = json.loads((OUT / 'inventory.json').read_text(encoding='utf-8'))
    evidence = json.loads((OUT / 'evidencias.json').read_text(encoding='utf-8'))['sources']
    after = scan(persist=False, collect_signals=False, verbose=False)
    repos = {r['name']: r for r in model['repositories']}
    old = {r['name']: r for r in before['repositories']}
    now = {r['name']: r for r in after['repositories']}
    check(set(repos) == set(now) == set(old), 'Directory coverage differs')
    check(len(repos) == 17, 'Expected 17 reviewed directories; review intake')
    for name in sorted(set(old) & set(now)):
        check(old[name]['source_fingerprint'] == now[name]['source_fingerprint'], 'Source drift: ' + name)
        check(old[name]['git'] == now[name]['git'], 'Git state drift: ' + name)
        check(not now[name]['errors'], 'Inventory errors: ' + name)
        check((OUT / 'repositorios' / (name + '.md')).is_file(), 'Missing repo note: ' + name)
    by_id = {e['id']: e for e in evidence}
    check(len(by_id) == len(evidence), 'Duplicate evidence ids')
    file_index = {f"02_repositorios/{r['name']}/{f['path']}": f for r in now.values() for f in r['files']}
    for e in evidence:
        f = file_index.get(e['path'])
        check(f is not None, 'Evidence outside inventory: ' + e['id'])
        if f:
            check(f['sha256'] == e['sha256'], 'Evidence hash differs: ' + e['id'])
            check(1 <= e['line'] <= f['lines'], 'Evidence line out of range: ' + e['id'])
    for r in repos.values():
        for key in ('purpose', 'architecture', 'flow'):
            check(bool(r['dimensions'][key]['evidence']), 'Missing core fact evidence: ' + r['name'] + '/' + key)
        for dim in r['dimensions'].values():
            for key in dim['evidence']:
                check(key in by_id, 'Unresolved evidence id: ' + key)
    with (OUT / 'matriz-conhecimento.csv').open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    pairs = {(r['repositorio'], r['dimensao']) for r in rows}
    wanted = {(r['name'], d) for r in repos.values() for d in r['dimensions']}
    check(pairs == wanted and len(pairs) == len(rows), 'Matrix incomplete/duplicate')
    links = 0
    for path in OUT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', '#')):
                continue
            links += 1
            resolved = (path.parent / target.split('#')[0]).resolve()
            check(resolved.is_relative_to(ROOT), 'Link escapes workspace: ' + str(path))
            check(resolved.exists(), 'Broken link: ' + str(path.relative_to(OUT)) + ' -> ' + target)
    # Artifacts intentionally contain no copied source excerpts or secret values.
    secret_patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'AKIA[A-Z0-9]{16}',
                       r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                       r'https?://[^\s/"<>]+:[^\s/"<>]+@']
    for path in OUT.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.name in {'checksums.json', 'verificacao.json'}:
            continue
        text = path.read_text(encoding='utf-8-sig')
        for pattern in secret_patterns:
            check(re.search(pattern, text) is None, 'Potential secret in artifact: ' + path.relative_to(OUT).as_posix())
    result = {'status': 'PASS' if not errors else 'FAIL', 'mapping_version': '3.0.0-beta',
              'checked_at': after['captured_at'], 'repositories': len(repos),
              'source_files_rehashed': len(file_index), 'evidence_locators': len(evidence),
              'matrix_rows': len(rows), 'local_links_checked': links,
              'source_and_git_preserved': not any('drift' in s for s in errors),
              'duration_seconds': round(time.monotonic() - start, 3),
              'verification_scope': 'Static source hashes, Git state, coverage, locators, matrix and links. No target tests/runtime executed. Sequential self-verification.',
              'limitations': ['Known-pattern artifact secret scan is not a comprehensive secrets audit.',
                              'Excluded source trees are outside the preservation/hash claim.'],
              'errors': errors}
    save('verificacao.json', result)
    checksums = {p.relative_to(OUT).as_posix(): digest(p.read_bytes()) for p in sorted(OUT.rglob('*'))
                 if p.is_file() and '__pycache__' not in p.parts and p.name != 'checksums.json'}
    save('checksums.json', checksums)
    print(json.dumps(result, ensure_ascii=True))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    verify()
