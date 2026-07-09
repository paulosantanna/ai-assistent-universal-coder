"""Scan exclusion patterns and gitignore support."""

from pathlib import Path
from fnmatch import fnmatch

DEFAULT_EXCLUDE_PATTERNS = [
    ".aeos-runtime",
    ".aeos/tmp",
    ".cache",
    ".git",
    ".hypothesis",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "checkpoints",
    "chroma",
    "chromadb",
    "chroma_db",
    "data/cache",
    "data/chunks",
    "data/normalized",
    "data/raw",
    "dist",
    "env",
    "logs",
    "models",
    "node_modules",
    "outputs",
    "site-packages",
    "target",
    "unsloth_compiled_cache",
    "venv",
]


def normalize_patterns(patterns: list[str]) -> list[str]:
    result = []
    for p in patterns:
        p = p.strip("/\\").replace("\\", "/")
        if p not in result:
            result.append(p)
    return result


def load_gitignore(gitignore_path: Path) -> list[str]:
    if not gitignore_path.exists():
        return []
    patterns = []
    for line in gitignore_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def collect_gitignore_patterns(root: Path) -> list[str]:
    patterns = []
    gitignore = root / ".gitignore"
    if gitignore.exists():
        patterns.extend(load_gitignore(gitignore))
    for sub in root.iterdir():
        if sub.is_dir() and not sub.name.startswith("."):
            nested = sub / ".gitignore"
            if nested.exists():
                patterns.extend(load_gitignore(nested))
    return normalize_patterns(patterns)


def is_excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    for pattern in patterns:
        pat = pattern.strip("/")
        if "/" in pat:
            if fnmatch(rel, pat) or rel.startswith(pat + "/") or rel == pat:
                return True
        else:
            for part in parts:
                if fnmatch(part, pat):
                    return True
    return False
