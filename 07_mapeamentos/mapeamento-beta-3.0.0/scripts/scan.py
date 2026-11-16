"""Bounded local source inventory. Never import or execute target repository code."""
import collections
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
TARGET = ROOT / '02_repositorios'
SKIP = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build',
        '.cache', '.mypy_cache', '.pytest_cache', '.ruff_cache', '__pycache__',
        '.next', '.turbo', '.dart_tool', '.idea', '.postgres', '.redis',
        'vendor', 'third_party', '.aeos', 'data', 'datasets', 'logs', 'backups',
        'before', 'evidence', 'artifacts', 'output', 'outputs', 'plan',
        '.local', '.gradle', 'assets', 'img', 'checkpoints', '.work', '.tools'}
TEXT = {'.py', '.ts', '.tsx', '.js', '.mjs', '.cjs', '.rs', '.go', '.dart',
        '.java', '.swift', '.cpp', '.c', '.cc', '.h', '.hpp', '.cs', '.kt',
        '.ps1', '.sh', '.bat', '.md', '.toml', '.yaml', '.yml', '.sql',
        '.graphql', '.json', '.txt', '.ipynb', '.html', '.css', '.svelte'}
MANIFESTS = {'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod',
             'pubspec.yaml', 'Dockerfile', 'rust-toolchain.toml',
             'requirements.txt', 'compose.yml', 'docker-compose.yml'}
LOCKS = {'uv.lock', 'Cargo.lock', 'package-lock.json', 'pnpm-lock.yaml',
         'yarn.lock', 'poetry.lock', 'pubspec.lock', 'go.sum'}
PATTERNS = {
    'sft': r'\b(?:SFTTrainer|SFTConfig)\b',
    'peft': r'\b(?:LoraConfig|PeftModel|prepare_model_for_kbit_training|get_peft_model)\b',
    'dpo': r'\b(?:DPOTrainer|DPOConfig|DpoTrainer)\b',
    'ppo': r'\b(?:PPOTrainer|PPOConfig|PPOTrainerAdapter)\b',
    'grpo': r'\b(?:GRPOTrainer|GRPOConfig)\b',
    'retrieval': r'\b(?:HybridRetriever|BM25Okapi|BM25Retriever|IndexFlatIP|FAISS|Chroma|ChromaDB|chromadb|Milvus|milvus|FTS5|fts5)\b',
    'graph': r'\b(?:GraphRAG|Neo4j|neo4j|graph_expand|extract_graph)\b',
    'ncm': r'\b(?:VQVAE|VQ_VAE|fine_drop|block_diagonal|Next.Concept)\b',
    'serving': r'\b(?:FastAPI|APIRouter|Ollama|vllm|onnxruntime)\b',
    'mcp': r'\b(?:McpServer|FastMCP|startMcpTransport|Model.Context.Protocol)\b',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save(name, obj):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sensitive(name):
    low = name.lower()
    return (low.startswith(('.env', 'cookie', 'secret', 'credential'))
            or low in {'auth.json', 'settings.json', '.npmrc', '.pypirc', '.netrc'}
            or low.endswith(('.pem', '.key', '.p12', '.pfx', '.sqlite', '.db')))


def git(repo, *args):
    proc = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                          capture_output=True, timeout=30)
    if proc.returncode:
        return {'error': 'git_exit_' + str(proc.returncode)}
    return proc.stdout.decode('utf-8', errors='replace').strip()


def scan(persist=True, collect_signals=True, verbose=True):
    start = time.monotonic()
    result = []
    for repo in sorted(TARGET.iterdir(), key=lambda p: p.name.lower()):
        if not repo.is_dir():
            continue
        if repo.is_symlink() or repo.is_junction():
            raise ValueError('Repository root is a link: ' + repo.name)
        files, excluded, errors = [], [], []
        own_git = (repo / '.git').exists()
        git_state = {'own_git': own_git}
        if own_git:
            git_state.update(head=git(repo, 'rev-parse', 'HEAD'),
                             branch=git(repo, 'symbolic-ref', '--short', '-q', 'HEAD'),
                             status=git(repo, 'status', '--porcelain=v1', '--untracked-files=normal'),
                             commits_since_beta2=git(repo, 'log', '--since=2026-10-20T23:59:59-03:00', '--format=%H %cs', '-30'))
        def onerror(err):
            errors.append({'type': type(err).__name__})
        for directory, dirs, names in os.walk(repo, followlinks=False, onerror=onerror):
            parent = Path(directory)
            for name in sorted(dirs):
                path = parent / name
                if name in SKIP or sensitive(name) or path.is_symlink() or path.is_junction():
                    dirs.remove(name)
                    excluded.append({'path': path.relative_to(repo).as_posix(), 'reason': 'excluded_tree_or_link'})
            dirs.sort()
            for name in sorted(names):
                path = parent / name
                rel = path.relative_to(repo).as_posix()
                if sensitive(name) or path.is_symlink():
                    excluded.append({'path': rel, 'reason': 'sensitive_name_or_link; content not read'})
                    continue
                try:
                    size = path.stat().st_size
                    if size > 2_000_000 or (path.suffix.lower() not in TEXT and name not in MANIFESTS | LOCKS):
                        excluded.append({'path': rel, 'reason': 'binary_or_unsupported_or_over_2MB; content not read'})
                        continue
                    raw = path.read_bytes()
                    if b'\x00' in raw[:4000] and not raw.startswith((b'\xff\xfe', b'\xfe\xff')):
                        excluded.append({'path': rel, 'reason': 'binary_content'})
                        continue
                    encoding = 'utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig'
                    try:
                        text = raw.decode(encoding)
                    except UnicodeDecodeError:
                        text = raw.decode('cp1252', errors='replace')
                    signals = {}
                    for label, pattern in (PATTERNS.items() if collect_signals else []):
                        hits = [i for i, line in enumerate(text.splitlines(), 1) if re.search(pattern, line)]
                        if hits:
                            signals[label] = hits[:12]
                    files.append({'path': rel, 'bytes': len(raw), 'sha256': digest(raw),
                                  'lines': len(text.splitlines()), 'signals': signals,
                                  'manifest': name in MANIFESTS, 'lockfile': name in LOCKS,
                                  'ci': rel.startswith('.github/workflows/'),
                                  'test_candidate': bool(re.search(r'(^|/)(tests?|__tests__)/|test_|_test\.|\.test\.|\.spec\.', rel))})
                except OSError as err:
                    errors.append({'path': rel, 'type': type(err).__name__})
        result.append({'name': repo.name, 'git': git_state, 'files': files,
                       'excluded': excluded, 'errors': errors,
                       'source_fingerprint': digest('\n'.join(f['path'] + ':' + f['sha256'] for f in files).encode()),
                       'extensions': dict(collections.Counter(Path(f['path']).suffix for f in files))})
        if verbose:
            print(repo.name, len(files), 'files;', len(excluded), 'excluded;', len(errors), 'errors')
    snapshot = {'version': '3.0.0-beta', 'captured_at': datetime.now(timezone.utc).isoformat(),
                            'scope': '02_repositorios immediate directories; local only',
                            'duration_seconds': round(time.monotonic()-start, 3), 'repositories': result}
    if persist:
        save('inventory.json', snapshot)
    return snapshot


if __name__ == '__main__':
    scan()
