"""Stage exact Dark-videos changes, then optionally install with fingerprint checks."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stage(target, output):
    home = Path(__file__).resolve().parents[1]
    router = 'backend/app/api/router.py'
    nav = 'frontend/src/components/shell/nav.ts'
    config = 'backend/app/api/science_studio.json'
    existing_router = (target / router).read_bytes()
    existing_nav = (target / nav).read_bytes()
    router_newline = '\r\n' if b'\r\n' in existing_router else '\n'
    nav_newline = '\r\n' if b'\r\n' in existing_nav else '\n'
    r = existing_router.decode('utf-8').replace('\r\n', '\n')
    n = existing_nav.decode('utf-8').replace('\r\n', '\n')
    if 'science_studio.router' not in r:
        anchor = 'from app.api import accounts, auth, cookier, desktop_update, health, oauth, pipeline, settings'
        if anchor not in r or '    health.router,' not in r:
            raise ValueError('router_anchor_changed: inspect actual target')
        r = r.replace(anchor, anchor + '\nfrom app.api import science_studio', 1)
        r = r.replace('    health.router,', '    science_studio.router,\n    health.router,', 1)
    r = r.replace('from app.api import accounts, auth, cookier, desktop_update, health, oauth, pipeline, settings\nfrom app.api import science_studio',
                  'from app.api import (\n    accounts,\n    auth,\n    cookier,\n    desktop_update,\n    health,\n    oauth,\n    pipeline,\n    science_studio,\n    settings,\n)')
    if 'href: "/science-studio"' not in n:
        anchor = '      { href: "/schedule",'
        if anchor not in n:
            raise ValueError('navigation_anchor_changed')
        n = n.replace(anchor, '      { href: "/science-studio", label: "Science Studio", icon: "film", owner: "creative" },\n' + anchor, 1)
    mapping = {
        router: r.replace('\n', router_newline).encode('utf-8'),
        nav: n.replace('\n', nav_newline).encode('utf-8'),
        'backend/app/api/science_studio.py': (home / 'integration/dark_api.py').read_bytes(),
        'frontend/src/app/(app)/science-studio/page.tsx': (home / 'integration/page.tsx').read_bytes(),
        config: (target / config).read_bytes() if (target / config).is_file() else
            (json.dumps({'home': str(home), 'projects': str(home.parent / '.work/science-studio/projects'),
                         'config': None}, indent=2) + '\n').encode(),
    }
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    differences = []
    for name, data in mapping.items():
        path = target / name
        before = path.read_bytes() if path.is_file() else None
        if name not in (router, nav, config) and before is not None and before != data:
            installed = output / 'installed.json'
            prior = json.loads(installed.read_text(encoding='utf-8')) if installed.is_file() else {'files': []}
            known = next((item for item in prior['files'] if item['path'] == name), None)
            if not known or known['after'] != sha(before):
                raise ValueError('existing_artifact_has_unrecognized_content: ' + name)
        proposed = output / 'proposed' / name
        proposed.parent.mkdir(parents=True, exist_ok=True)
        proposed.write_bytes(data)
        if before is not None:
            backup = output / 'before' / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            # Preserve initial backup across reruns; never erase previous rollback evidence.
            if not backup.exists():
                backup.write_bytes(before)
        differences.extend(difflib.unified_diff((before or b'').decode().splitlines(True),
                                               data.decode().splitlines(True), fromfile=name, tofile=name))
        manifest.append({'path': name, 'before': sha(before) if before is not None else None,
                         'after': sha(data), 'changed': before != data})
    (output / 'changes.diff').write_text(''.join(differences), encoding='utf-8')
    (output / 'manifest.json').write_text(json.dumps({'target': str(target), 'files': manifest}, indent=2) + '\n', encoding='utf-8')
    return manifest


def apply(target, output):
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    if Path(manifest['target']).resolve() != target:
        raise ValueError('staged_target_mismatch')
    for item in manifest['files']:
        destination = (target / item['path']).resolve()
        if not destination.is_relative_to(target):
            raise ValueError('outside_install_target')
        before = sha(destination.read_bytes()) if destination.is_file() else None
        if before != item['before']:
            raise ValueError('target_changed_since_staging: ' + item['path'])
        source = output / 'proposed' / item['path']
        if sha(source.read_bytes()) != item['after']:
            raise ValueError('staged_file_changed: ' + item['path'])
    for item in manifest['files']:
        if item['changed']:
            destination = target / item['path']
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((output / 'proposed' / item['path']).read_bytes())
    (output / 'installed.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return {'status': 'installed_on_disk', 'activation': 'not_restarted', 'files': len(manifest['files'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    target, output = args.target.resolve(), args.stage.resolve()
    if args.apply:
        print(json.dumps(apply(target, output)))
    else:
        print(json.dumps({'status': 'staged', 'files': stage(target, output)}))
