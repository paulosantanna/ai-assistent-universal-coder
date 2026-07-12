from __future__ import annotations

import re
import threading
from typing import Any

from lsprotocol.types import (
    FoldingRange,
    FoldingRangeKind,
    FoldingRangeParams,
)
from pygls.lsp.server import LanguageServer


class FoldingFeature:
    def __init__(self, server: LanguageServer) -> None:
        self._server = server
        self._lock = threading.RLock()

    def provide_folding_ranges(self, params: FoldingRangeParams) -> list[FoldingRange] | None:
        uri = params.text_document.uri
        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return None

        text = doc.source
        lines = text.splitlines(keepends=False)
        ranges: list[FoldingRange] = []

        ranges.extend(self._yaml_folding(lines))
        ranges.extend(self._markdown_folding(lines))
        ranges.extend(self._region_folding(lines))
        ranges.extend(self._comment_folding(lines))
        ranges.extend(self._front_matter_folding(lines))

        merged = self._merge_overlapping(ranges)
        return merged if merged else None

    def _yaml_folding(self, lines: list[str]) -> list[FoldingRange]:
        ranges: list[FoldingRange] = []
        indent_stack: list[tuple[int, int]] = []

        for i, line in enumerate(lines):
            if not line.strip() or line.strip().startswith("#") or line.strip().startswith("---"):
                continue

            stripped = line.rstrip()
            if stripped.endswith(":") or stripped.endswith(": |") or stripped.endswith(": >"):
                indent = len(line) - len(line.lstrip())
                indent_stack.append((indent, i))
            elif stripped.endswith(":") is False and indent_stack:
                pass
            elif stripped.endswith(":") and indent_stack:
                current_indent = len(line) - len(line.lstrip())
                while indent_stack and indent_stack[-1][0] >= current_indent:
                    start_indent, start_line = indent_stack.pop()
                    if i - start_line > 1:
                        ranges.append(FoldingRange(
                            start_line=start_line,
                            end_line=i - 1,
                            kind=FoldingRangeKind.Region,
                        ))

        while len(indent_stack) > 1:
            start_indent, start_line = indent_stack.pop()
            if indent_stack:
                parent_start = indent_stack[-1][1]
                if start_line > parent_start + 1:
                    ranges.append(FoldingRange(
                        start_line=start_line,
                        end_line=len(lines) - 1,
                        kind=FoldingRangeKind.Region,
                    ))

        return ranges

    def _markdown_folding(self, lines: list[str]) -> list[FoldingRange]:
        ranges: list[FoldingRange] = []
        heading_stack: list[tuple[int, int, int]] = []

        for i, line in enumerate(lines):
            m = re.match(r"^(#{1,6})\s", line)
            if m:
                level = len(m.group(1))
                while heading_stack and heading_stack[-1][0] >= level:
                    h_level, h_line, _ = heading_stack.pop()
                    if i - h_line > 1:
                        ranges.append(FoldingRange(
                            start_line=h_line,
                            end_line=i - 1,
                            kind=FoldingRangeKind.Region,
                        ))
                heading_stack.append((level, i, i))

        while heading_stack:
            level, h_line, _ = heading_stack.pop()
            if len(lines) - 1 - h_line > 1:
                ranges.append(FoldingRange(
                    start_line=h_line,
                    end_line=len(lines) - 1,
                    kind=FoldingRangeKind.Region,
                ))

        return ranges

    def _region_folding(self, lines: list[str]) -> list[FoldingRange]:
        ranges: list[FoldingRange] = []
        region_stack: list[int] = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r"^#\s*region\b", stripped, re.IGNORECASE):
                region_stack.append(i)
            elif re.match(r"^#\s*endregion\b", stripped, re.IGNORECASE):
                if region_stack:
                    start = region_stack.pop()
                    if i - start > 1:
                        ranges.append(FoldingRange(
                            start_line=start,
                            end_line=i,
                            kind=FoldingRangeKind.Region,
                        ))

        return ranges

    def _comment_folding(self, lines: list[str]) -> list[FoldingRange]:
        ranges: list[FoldingRange] = []
        in_block = False
        block_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            is_comment = stripped.startswith("#") or stripped.startswith("//")
            if is_comment and not in_block:
                in_block = True
                block_start = i
            elif not is_comment and in_block:
                if i - block_start > 2:
                    ranges.append(FoldingRange(
                        start_line=block_start,
                        end_line=i - 1,
                        kind=FoldingRangeKind.Comment,
                    ))
                in_block = False

        if in_block and len(lines) - 1 - block_start > 2:
            ranges.append(FoldingRange(
                start_line=block_start,
                end_line=len(lines) - 1,
                kind=FoldingRangeKind.Comment,
            ))

        return ranges

    def _front_matter_folding(self, lines: list[str]) -> list[FoldingRange]:
        if len(lines) < 3:
            return []
        if lines[0].strip() == "---":
            for i in range(1, min(len(lines), 50)):
                if lines[i].strip() == "---":
                    if i > 1:
                        return [FoldingRange(
                            start_line=0,
                            end_line=i,
                            kind=FoldingRangeKind.Region,
                        )]
                    break
        return []

    def _merge_overlapping(self, ranges: list[FoldingRange]) -> list[FoldingRange]:
        if not ranges:
            return []

        sorted_ranges = sorted(ranges, key=lambda r: (r.start_line, -r.end_line))
        merged: list[FoldingRange] = []

        for r in sorted_ranges:
            if merged and merged[-1].start_line <= r.start_line <= merged[-1].end_line:
                if r.end_line > merged[-1].end_line:
                    merged[-1].end_line = r.end_line
            else:
                merged.append(r)

        return merged
