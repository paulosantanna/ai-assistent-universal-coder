from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lsprotocol.types import Position, Range


@dataclass(frozen=True)
class DocumentSnapshot:
    uri: str
    version: int
    text: str
    lines: tuple[str, ...] = field(init=False)
    content_hash: str = field(init=False)
    parsed_ast: object = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "lines", tuple(self.text.splitlines(keepends=True)))
        object.__setattr__(self, "content_hash", hashlib.sha256(self.text.encode("utf-8")).hexdigest())

    def position_at_offset(self, offset: int) -> Position:
        if offset < 0:
            offset = 0
        if offset > len(self.text):
            offset = len(self.text)
        line = 0
        remaining = offset
        for line_text in self.lines:
            line_len = len(line_text)
            if remaining <= line_len:
                return Position(line=line, character=remaining)
            remaining -= line_len
            line += 1
        return Position(line=line, character=0)

    def offset_at_position(self, position: Position) -> int:
        if position.line < 0:
            return 0
        if position.line >= len(self.lines):
            return len(self.text)
        offset = 0
        for i in range(position.line):
            offset += len(self.lines[i])
        return offset + min(position.character, len(self.lines[position.line].rstrip("\n\r")))

    def get_line(self, line: int) -> str:
        if line < 0 or line >= len(self.lines):
            return ""
        return self.lines[line].rstrip("\n\r")

    def range_to_offsets(self, range: Range) -> tuple[int, int]:
        start = self.offset_at_position(range.start)
        end = self.offset_at_position(range.end)
        return (start, end)
