"""Standard exclusion patterns for repository scanning."""

from __future__ import annotations

DEFAULT_EXCLUSIONS: list[str] = [
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "frontend/build",
    "dist",
    "build",
    "coverage",
    "htmlcov",
    "logs",
    "tmp",
    "temp",
    ".aeos/sandbox",
    "unsloth_compiled_cache",
    "src/training/unsloth_compiled_cache",
    "checkpoints",
    "*.safetensors",
    "*.pt",
    "*.pth",
    "*.bin",
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.db-wal",
    "*.db-shm",
    "*.db-journal",
]

BINARY_EXTENSIONS: set[str] = {
    ".safetensors", ".pt", ".pth", ".bin", ".ckpt",
    ".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm", ".db-journal",
    ".pyc", ".pyd", ".so", ".dll", ".dylib",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".whl", ".egg", ".jar",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".mp4", ".avi", ".mov", ".mkv",
    ".mp3", ".wav", ".ogg", ".flac",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".ttf", ".otf", ".woff", ".woff2",
    ".o", ".obj", ".lib", ".a",
}

EXECUTABLE_EXTENSIONS: set[str] = {
    ".exe", ".msi", ".bat", ".cmd", ".ps1", ".sh",
}


def build_ignore_patterns(extra: list[str] | None = None) -> list[str]:
    """Return the combined list of exclusion patterns."""
    patterns = list(DEFAULT_EXCLUSIONS)
    if extra:
        patterns.extend(extra)
    return patterns


def should_ignore(rel_path: str, patterns: list[str] | None = None) -> bool:
    """Check whether a relative path matches any exclusion pattern."""
    if patterns is None:
        patterns = DEFAULT_EXCLUSIONS
    from fnmatch import fnmatch
    for pat in patterns:
        if pat.startswith("*."):
            if fnmatch(rel_path, pat):
                return True
        elif pat in rel_path.replace("\\", "/").split("/"):
            return True
    return False
