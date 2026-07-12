from __future__ import annotations

import logging
import re
from collections import Counter
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity

logger = logging.getLogger(__name__)


class OutputCompactor:
    def __init__(self, max_repeated_lines: int = 3) -> None:
        self._max_repeated = max_repeated_lines

    def compact_text(self, text: str) -> str:
        if not text:
            return text

        text = self._compress_repeated_lines(text)
        text = self._compress_repeated_patterns(text)
        text = self._compress_whitespace(text)

        return text

    def compact_diagnostics(self, diagnostics: list[Diagnostic]) -> list[dict[str, Any]]:
        if not diagnostics:
            return []

        grouped: dict[str, list[Diagnostic]] = {}
        for d in diagnostics:
            key = f"{d.code}:{d.message[:100]}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(d)

        compacted: list[dict[str, Any]] = []
        for key, group in grouped.items():
            first = group[0]
            count = len(group)
            entry = {
                "code": first.code,
                "message": first.message,
                "severity": first.severity.value if hasattr(first.severity, "value") else first.severity,
                "count": count,
                "source": first.source,
            }

            if count > 1:
                entry["duplicates"] = count
                entry["note"] = f"Repeated {count} times"

            compacted.append(entry)

        compacted.sort(key=lambda x: (
            x.get("severity", DiagnosticSeverity.Hint.value),
            x.get("code", "") or "",
        ))

        return compacted

    def deduplicate(self, items: list[Any], key_fn=None) -> list[Any]:
        if key_fn is None:
            key_fn = lambda x: str(x)

        seen: set[str] = set()
        result: list[Any] = []
        for item in items:
            key = key_fn(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    def compact_json(self, data: Any, max_depth: int = 10) -> Any:
        if max_depth <= 0:
            if isinstance(data, (str, int, float, bool)):
                return data
            return "... (truncated)"

        if isinstance(data, dict):
            compacted: dict[str, Any] = {}
            for key, value in data.items():
                compacted[key] = self.compact_json(value, max_depth - 1)
            return compacted

        if isinstance(data, list):
            if len(data) > 10:
                compacted_list = [self.compact_json(item, max_depth - 1) for item in data[:10]]
                compacted_list.append(f"... ({len(data) - 10} more items)")
                return compacted_list
            return [self.compact_json(item, max_depth - 1) for item in data]

        return data

    def summarize_diagnostics(self, diagnostics: list[Diagnostic]) -> dict[str, Any]:
        if not diagnostics:
            return {"total": 0}

        severity_counts: dict[str, int] = Counter()
        code_counts: dict[str, int] = Counter()
        source_counts: dict[str, int] = Counter()

        for d in diagnostics:
            sev = d.severity.value if hasattr(d.severity, "value") else str(d.severity)
            severity_counts[sev] += 1
            code_counts[str(d.code or "unknown")] += 1
            source_counts[str(d.source or "unknown")] += 1

        return {
            "total": len(diagnostics),
            "by_severity": dict(severity_counts),
            "top_codes": code_counts.most_common(10),
            "top_sources": source_counts.most_common(10),
        }

    def _compress_repeated_lines(self, text: str) -> str:
        lines = text.split("\n")
        compressed: list[str] = []
        i = 0
        while i < len(lines):
            current = lines[i]
            count = 1
            while i + count < len(lines) and lines[i + count] == current:
                count += 1
            if count > self._max_repeated:
                compressed.append(current)
                compressed.append(f"... ({count - self._max_repeated} repeated lines)")
                i += count
            else:
                for _ in range(count):
                    compressed.append(current)
                i += count
        return "\n".join(compressed)

    def _compress_repeated_patterns(self, text: str) -> str:
        pattern = re.compile(r"(.{10,}?)\1{2,}", re.DOTALL)
        return pattern.sub(r"\1(... repeated)", text)

    def _compress_whitespace(self, text: str) -> str:
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        text = re.sub(r"[ \t]{4,}", " ", text)
        return text.strip()

    def __repr__(self) -> str:
        return f"OutputCompactor(max_repeated_lines={self._max_repeated})"
