"""Read-only bounded inventory. Never execute repository content or read secrets."""
import collections
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build',
        '.cache', '.mypy_cache', '.pytest_cache', '.ruff_cache', '__pycache__',
        '.next', '.turbo', '.dart_tool', '.idea', '.postgres', '.redis',
        'vendor', 'third_party', '.aeos', 'data', 'logs', 'backups', 'before',
        'evidence', 'artifacts', 'output', 'outputs', 'models', 'plan',
        '.local', '.gradle', '.husky', 'img', 'assets', 'contributors'}
SENSITIVE = {'.env', '.env.example', 'cookier', 'cookies.json', 'cookies.txt',
             'auth.json', 'credentials.json', 'settings.json'}
MANIFESTS = {'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod',
             'pubspec.yaml', 'docker-compose.yml', 'compose.yml', 'Dockerfile',
             'rust-toolchain.toml', '.nvmrc', 'requirements.txt'}
TEXT = {'.py', '.ts', '.tsx', '.js', '.mjs', '.cjs', '.rs', '.go', '.dart',
        '.ps1', '.md', '.toml', '.yaml', '.yml', '.sql', '.graphql', '.json'}


def inventory():
    result = []
    for repo in sorted((ROOT / '02_repositorios').iterdir(), key=lambda p: p.name.lower()):
        if not repo.is_dir():
            continue
        files, excluded, errors, candidates = [], [], [], []
        def onerror(error):
            errors.append({'path': str(Path(error.filename).relative_to(ROOT)), 'error': type(error).__name__})
        for directory, dirs, names in os.walk(repo, followlinks=False, onerror=onerror):
            parent = Path(directory)
            for name in sorted(dirs):
                path = parent / name
                if name in SKIP or path.is_symlink() or path.is_junction():
                    dirs.remove(name)
                    excluded.append({'path': path.relative_to(repo).as_posix(), 'reason': 'dependency/cache/runtime/data/asset/third-party/link tree'})
            dirs.sort()
            for name in sorted(names):
                path = parent / name
                relative = path.relative_to(repo).as_posix()
                if name in SENSITIVE or name.lower().startswith(('.env', 'cookie', 'secret', 'credential')) or path.is_symlink():
                    excluded.append({'path': relative, 'reason': 'potential credential or link; content not read'})
                    continue
                try:
                    stat = path.stat()
                    files.append({'path': relative, 'bytes': stat.st_size, 'mtime_ns': stat.st_mtime_ns})
                    if path.suffix in TEXT or name in MANIFESTS or name == '.nvmrc':
                        candidates.append(relative)
                except OSError as error:
                    errors.append({'path': relative, 'error': type(error).__name__})
        result.append({'name': repo.name, 'own_git': (repo / '.git').exists(),
                       'files': files, 'excluded': excluded, 'errors': errors,
                       'extensions': dict(collections.Counter(Path(f['path']).suffix for f in files)),
                       'manifests': [p for p in candidates if Path(p).name in MANIFESTS],
                       'sources': [p for p in candidates if Path(p).suffix in {'.py','.ts','.tsx','.rs','.go','.dart','.ps1'}],
                       'docs': [p for p in candidates if Path(p).suffix == '.md'],
                       'ci': [p for p in candidates if p.startswith('.github/workflows/')],
                       'tests': [p for p in candidates if any(s in p.lower() for s in ('test', 'spec.', '/specs/'))]})
    return result


if __name__ == '__main__':
    repos = inventory()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'inventory.json').write_text(json.dumps(repos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for r in repos:
        print(json.dumps({k: (v if k in {'name','own_git','extensions','manifests','ci'} else len(v)) for k,v in r.items()}, ensure_ascii=False))
