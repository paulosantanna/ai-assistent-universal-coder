from pathlib import Path
from typing import Optional


class PackagePolicy:

    FORBIDDEN_DIRS = {".git", "__pycache__", "node_modules", ".venv", ".env"}
    FORBIDDEN_EXTENSIONS = {".pyc", ".exe", ".dll", ".so", ".dylib"}
    FORBIDDEN_PREFIXES = {"/", "\\", ".."}
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    MAX_TOTAL_SIZE = 1024 * 1024 * 1024  # 1 GB

    @staticmethod
    def is_path_allowed(rel_path: str) -> tuple[bool, Optional[str]]:
        for prefix in PackagePolicy.FORBIDDEN_PREFIXES:
            if rel_path.startswith(prefix):
                return False, f"Path starts with forbidden prefix: {prefix}"
        if ".." in rel_path:
            return False, "Path traversal detected"
        parts = rel_path.replace("\\", "/").split("/")
        for part in parts:
            if part in PackagePolicy.FORBIDDEN_DIRS:
                return False, f"Forbidden directory: {part}"
        ext = Path(rel_path).suffix
        if ext in PackagePolicy.FORBIDDEN_EXTENSIONS:
            return False, f"Forbidden extension: {ext}"
        return True, None

    @staticmethod
    def is_size_allowed(file_size: int, total_size: int) -> tuple[bool, Optional[str]]:
        if file_size > PackagePolicy.MAX_FILE_SIZE:
            return False, f"File exceeds max size: {file_size} > {PackagePolicy.MAX_FILE_SIZE}"
        if total_size > PackagePolicy.MAX_TOTAL_SIZE:
            return False, f"Total exceeds max size: {total_size} > {PackagePolicy.MAX_TOTAL_SIZE}"
        return True, None