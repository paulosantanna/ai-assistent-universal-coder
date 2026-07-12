from __future__ import annotations

import fnmatch
from pathlib import Path

from aeos_lsp.constants import DEFAULT_EXCLUSIONS


class Exclusions:
    def __init__(self, custom_patterns: set[str] | None = None) -> None:
        self._patterns: set[str] = set(DEFAULT_EXCLUSIONS)
        if custom_patterns:
            self._patterns.update(custom_patterns)

    @property
    def patterns(self) -> frozenset[str]:
        return frozenset(self._patterns)

    def add_pattern(self, pattern: str) -> None:
        self._patterns.add(pattern)

    def remove_pattern(self, pattern: str) -> None:
        self._patterns.discard(pattern)

    def matches_exclusion(self, path: Path) -> bool:
        resolved = path.resolve()
        for pattern in self._patterns:
            if _match_glob(resolved, pattern):
                return True
        return False

    def is_aeos_cache(self, path: Path) -> bool:
        resolved = path.resolve()
        parts = resolved.parts
        return ".aeos" in parts

    def update_custom_patterns(self, patterns: set[str]) -> None:
        self._patterns = set(DEFAULT_EXCLUSIONS) | patterns


def _match_glob(path: Path, pattern: str) -> bool:
    resolved = path.resolve()
    name = resolved.name
    if fnmatch.fnmatch(name, pattern):
        return True
    if pattern.startswith("*."):
        if resolved.suffix == pattern[1:]:
            return True
    for part in resolved.parts:
        if fnmatch.fnmatch(part, pattern):
            return True
    return False
