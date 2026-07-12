from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lsprotocol.types import Diagnostic, Position, Range

_SUPPRESSION_RE = re.compile(
    r"#\s*aeos-lsp:ignore\s+"
    r"(?P<codes>[A-Za-z0-9,;_\-#\s]+)"
    r"(?:\s+\((?P<justification>.+)\))?"
    r"\s*$"
)

_SUPPRESS_ALL_RE = re.compile(
    r"#\s*aeos-lsp:ignore-all\s*(?:\((?P<justification>.+)\))?\s*$"
)


@dataclass(frozen=True)
class SuppressionEntry:
    line: int
    codes: frozenset[str]
    suppress_all: bool = False
    justification: str | None = None


@dataclass
class SuppressionManager:
    cache: dict[str, list[SuppressionEntry]] = field(default_factory=dict)
    workspace_suppressions: dict[str, set[str]] = field(default_factory=dict)
    _lock: threading.RLock = field(default_factory=threading.RLock)
    require_justification: bool = False

    def parse_suppression_comments(self, uri: str, text: str) -> list[SuppressionEntry]:
        with self._lock:
            parsed = self._parse_lines(text)
            self.cache[uri] = parsed
            return parsed

    def is_suppressed(self, uri: str, diagnostic: Diagnostic, text: str | None = None) -> bool:
        with self._lock:
            entries = self.cache.get(uri)
            if entries is None:
                if text is not None:
                    entries = self.parse_suppression_comments(uri, text)
                else:
                    return False

            code: str = ""
            if isinstance(diagnostic.code, str):
                code = diagnostic.code
            elif hasattr(diagnostic.code, "value"):
                code = diagnostic.code.value

            for entry in entries:
                if entry.line == diagnostic.range.start.line:
                    if entry.suppress_all:
                        if self.require_justification and not entry.justification:
                            continue
                        return True
                    if code in entry.codes:
                        if self.require_justification and not entry.justification:
                            continue
                        return True

            for entry in entries:
                if entry.line == diagnostic.range.start.line and not entry.suppress_all:
                    if any(code.startswith(c) for c in entry.codes if c.endswith("*")):
                        if self.require_justification and not entry.justification:
                            continue
                        return True

            return False

    def is_suppressed_by_workspace(self, uri: str, diagnostic: Diagnostic) -> bool:
        with self._lock:
            for pattern, codes in self.workspace_suppressions.items():
                if PatternMatcher.match(pattern, uri):
                    code: str = ""
                    if isinstance(diagnostic.code, str):
                        code = diagnostic.code
                    elif hasattr(diagnostic.code, "value"):
                        code = diagnostic.code.value
                    if not codes or code in codes:
                        return True
            return False

    def is_suppressed_any(self, uri: str, diagnostic: Diagnostic, text: str | None = None) -> bool:
        return self.is_suppressed(uri, diagnostic, text) or self.is_suppressed_by_workspace(uri, diagnostic)

    def update_workspace_suppressions(self, suppressions: dict[str, set[str]]) -> None:
        with self._lock:
            self.workspace_suppressions.clear()
            self.workspace_suppressions.update(suppressions)

    def invalidate(self, uri: str) -> None:
        with self._lock:
            self.cache.pop(uri, None)

    def clear(self) -> None:
        with self._lock:
            self.cache.clear()
            self.workspace_suppressions.clear()

    def _parse_lines(self, text: str) -> list[SuppressionEntry]:
        entries: list[SuppressionEntry] = []
        for line_idx, line_text in enumerate(text.splitlines()):
            # Check for aeos-lsp:ignore-all
            m_all = _SUPPRESS_ALL_RE.search(line_text)
            if m_all:
                entries.append(SuppressionEntry(
                    line=line_idx,
                    codes=frozenset(),
                    suppress_all=True,
                    justification=m_all.group("justification"),
                ))
                continue

            # Check for aeos-lsp:ignore CODE,CODE2
            m = _SUPPRESSION_RE.search(line_text)
            if m:
                raw_codes = m.group("codes").strip()
                codes: set[str] = set()
                for part in re.split(r"[,;\s]+", raw_codes):
                    part = part.strip()
                    if part:
                        codes.add(part)
                entries.append(SuppressionEntry(
                    line=line_idx,
                    codes=frozenset(codes),
                    suppress_all=False,
                    justification=m.group("justification"),
                ))

        return entries


class PatternMatcher:
    @staticmethod
    def match(pattern: str, value: str) -> bool:
        if pattern == value:
            return True
        if pattern.endswith("*"):
            return value.lower().startswith(pattern[:-1].lower())
        if pattern.startswith("*"):
            return value.lower().endswith(pattern[1:].lower())
        if "*" in pattern:
            import fnmatch
            return fnmatch.fnmatch(value, pattern)
        return False
