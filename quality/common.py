"""CodENavi capability quality helpers. No runtime credentials or external execution."""
import hashlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '.tools', '.work', '.aeos', 'node_modules', '__pycache__', '.pytest_cache',
           '02_repositorios', 'chromatic-runs', 'reidoabc-image-fix'}


def canonical(data):
    if b'\0' not in data:
        try:
            data.decode('utf-8')
            return data.replace(b'\r\n', b'\n')
        except UnicodeDecodeError:
            pass
    return data


def sha(data):
    return hashlib.sha256(canonical(data)).hexdigest()


def artifact_sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def safe_path(root, value):
    p = PurePosixPath(value)
    if not value or '\\' in value or p.is_absolute() or '..' in p.parts or ':' in value:
        raise ValueError('Unsafe relative resource path')
    target = root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()) or target.is_symlink():
        raise ValueError('Resource escapes the declared root')
    return target


def files(root):
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED)
        for name in sorted(names):
            if name.endswith(('.pyc', '.pyo')) or name == '_read_image.py':
                continue
            yield Path(base)/name


def workspace_files(root):
    if (root/'.git').exists():
        result = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard', '-z'], cwd=root,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        for name in sorted(set(result.stdout.split(b'\0'))-{b''}):
            path = safe_path(root, name.decode('utf-8'))
            if path.is_file():
                yield path
    else:
        yield from files(root)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def architect(root):
    return module(root/'00_skills/(creation)/skill-architect/scripts/validate_skill.py', 'architect')


def package_hash(root):
    h = hashlib.sha256()
    for path in files(root):
        h.update(path.relative_to(root).as_posix().encode()+b'\0')
        h.update(sha(path.read_bytes()).encode()+b'\0')
    return h.hexdigest()
