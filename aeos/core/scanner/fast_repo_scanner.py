from pathlib import Path

DEFAULT_SKIP_DIRS = {".git", "node_modules", "target", "build", "dist", ".venv", "venv", "__pycache__", ".gradle", ".m2"}

class FastRepoScanner:
    def __init__(self, root: str, skip_dirs=None, max_file_mb: int = 5):
        self.root = Path(root)
        self.skip_dirs = set(skip_dirs or DEFAULT_SKIP_DIRS)
        self.max_file_bytes = max_file_mb * 1024 * 1024

    def iter_files(self):
        for path in self.root.rglob("*"):
            if path.is_dir():
                continue
            rel_parts = set(path.relative_to(self.root).parts)
            if rel_parts.intersection(self.skip_dirs):
                continue
            try:
                if path.stat().st_size > self.max_file_bytes:
                    yield {"path": str(path), "mode": "metadata_only", "size": path.stat().st_size}
                else:
                    yield {"path": str(path), "mode": "readable", "size": path.stat().st_size}
            except OSError:
                yield {"path": str(path), "mode": "error", "size": None}
