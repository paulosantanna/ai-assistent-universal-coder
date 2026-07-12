from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PathTraversalError(Exception):
    def __init__(self, path: str, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Path security violation: {path} ({reason})")


class PathPolicy:
    def __init__(
        self,
        workspace_roots: list[str | Path] | None = None,
        follow_symlinks: bool = False,
        allow_absolute_paths: bool = False,
        allow_path_traversal: bool = False,
        allowed_extensions: set[str] | None = None,
        blocked_extensions: set[str] | None = None,
        max_path_depth: int = 50,
    ) -> None:
        self._workspace_roots = [Path(p).resolve() for p in (workspace_roots or [])]
        self._follow_symlinks = follow_symlinks
        self._allow_absolute_paths = allow_absolute_paths
        self._allow_path_traversal = allow_path_traversal
        self._allowed_extensions = allowed_extensions
        self._blocked_extensions = blocked_extensions or {
            ".exe", ".dll", ".so", ".dylib", ".bin", ".pdb",
            ".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm",
            ".safetensors", ".pt", ".pth", ".bin", ".npy",
            ".pyc", ".pyo", ".pyd",
        }
        self._max_path_depth = max_path_depth

    def add_workspace_root(self, root: str | Path) -> None:
        resolved = Path(root).resolve()
        if resolved not in self._workspace_roots:
            self._workspace_roots.append(resolved)
            logger.debug("Added workspace root: %s", resolved)

    def remove_workspace_root(self, root: str | Path) -> None:
        resolved = Path(root).resolve()
        self._workspace_roots = [r for r in self._workspace_roots if r != resolved]

    def canonicalize(self, path: str | Path) -> Path:
        p = Path(path)

        if sys.platform == "win32":
            p = Path(os.path.normpath(str(p)))
        else:
            p = Path(os.path.normpath(str(p)))

        if not self._follow_symlinks:
            try:
                p = p.resolve()
            except (OSError, RuntimeError):
                p = p.absolute()

        return p

    def check_path(self, path: str | Path, operation: str = "read") -> Path:
        canonical = self.canonicalize(path)

        parts = canonical.parts
        if len(parts) > self._max_path_depth:
            raise PathTraversalError(
                str(canonical),
                f"Path depth {len(parts)} exceeds maximum {self._max_path_depth}",
            )

        suffix = canonical.suffix.lower()
        if self._blocked_extensions and suffix in self._blocked_extensions:
            raise PathTraversalError(
                str(canonical),
                f"File extension '{suffix}' is blocked",
            )

        if self._allowed_extensions and suffix not in self._allowed_extensions:
            raise PathTraversalError(
                str(canonical),
                f"File extension '{suffix}' is not in the allowed set",
            )

        if not self._allow_absolute_paths and canonical.is_absolute():
            raise PathTraversalError(
                str(canonical),
                "Absolute paths are not allowed",
            )

        if not self._allow_path_traversal:
            path_str = str(canonical)
            if ".." in path_str.split(os.sep):
                raise PathTraversalError(
                    str(canonical),
                    "Path traversal via '..' is not allowed",
                )

        if self._workspace_roots:
            if not self._is_within_workspace(canonical):
                raise PathTraversalError(
                    str(canonical),
                    f"Path is outside workspace roots: {self._workspace_roots}",
                )

        return canonical

    def is_path_allowed(self, path: str | Path, operation: str = "read") -> bool:
        try:
            self.check_path(path, operation)
            return True
        except PathTraversalError:
            return False

    def enforce_workspace_boundary(self, path: str | Path) -> Path:
        canonical = self.canonicalize(path)
        if self._workspace_roots:
            if not self._is_within_workspace(canonical):
                raise PathTraversalError(
                    str(canonical),
                    f"Path is outside workspace roots",
                )
        return canonical

    def safe_relative_to(self, path: str | Path, base: str | Path | None = None) -> Path:
        canonical = self.canonicalize(path)
        if base is None:
            if not self._workspace_roots:
                return canonical
            base = self._workspace_roots[0]
        else:
            base = self.canonicalize(base)

        try:
            return canonical.relative_to(base)
        except ValueError:
            raise PathTraversalError(
                str(canonical),
                f"Path is not relative to {base}",
            )

    def _is_within_workspace(self, path: Path) -> bool:
        try:
            resolved = path.resolve() if not path.is_absolute() else path
            for root in self._workspace_roots:
                try:
                    resolved.relative_to(root)
                    return True
                except ValueError:
                    continue
            return False
        except (OSError, RuntimeError):
            return False

    def to_stable_path(self, path: str | Path) -> str:
        canonical = self.canonicalize(path)
        if self._workspace_roots:
            for root in self._workspace_roots:
                try:
                    relative = canonical.relative_to(root)
                    return str(relative).replace(os.sep, "/")
                except ValueError:
                    continue
        return str(canonical).replace(os.sep, "/")

    def __repr__(self) -> str:
        return (
            f"PathPolicy(roots={len(self._workspace_roots)}, "
            f"follow_symlinks={self._follow_symlinks}, "
            f"allow_absolute={self._allow_absolute_paths}, "
            f"allow_traversal={self._allow_path_traversal})"
        )
