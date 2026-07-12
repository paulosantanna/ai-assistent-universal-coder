from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar

from lsprotocol.types import Position, Range

TAst = TypeVar("TAst")


class ParseErrorSeverity(Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    HINT = 4


@dataclass(frozen=True)
class ParseError:
    message: str
    range: Range
    severity: ParseErrorSeverity = ParseErrorSeverity.ERROR
    code: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
            "severity": self.severity.value,
            "code": self.code,
        }

    @classmethod
    def single_line(
        cls,
        message: str,
        line: int,
        start_char: int,
        end_char: int,
        severity: ParseErrorSeverity = ParseErrorSeverity.ERROR,
        code: str = "",
    ) -> ParseError:
        return cls(
            message=message,
            range=Range(
                start=Position(line=line, character=start_char),
                end=Position(line=line, character=end_char),
            ),
            severity=severity,
            code=code,
        )


ParserRange = Range


@dataclass(frozen=True)
class ParseResult(Generic[TAst]):
    ast: TAst
    errors: list[ParseError] = field(default_factory=list)
    ranges: dict[str, Range] = field(default_factory=dict)

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, error: ParseError) -> ParseResult[TAst]:
        return ParseResult(
            ast=self.ast,
            errors=[*self.errors, error],
            ranges=self.ranges,
        )

    def merge(self, other: ParseResult[Any]) -> ParseResult[TAst]:
        return ParseResult(
            ast=self.ast,
            errors=[*self.errors, *other.errors],
            ranges={**self.ranges, **other.ranges},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "ast": self.ast,
            "errors": [e.to_dict() for e in self.errors],
            "ranges": {
                k: {
                    "start": {"line": v.start.line, "character": v.start.character},
                    "end": {"line": v.end.line, "character": v.end.character},
                }
                for k, v in self.ranges.items()
            },
        }


class PositionConverter:
    """Encoding-aware position conversion between byte offsets and line/character."""

    def __init__(self, text: str, encoding: str = "utf-16") -> None:
        self._text = text
        self._encoding = encoding.lower().replace("-", "")
        self._lines: list[tuple[int, int]] = []
        self._build_line_index()

    def _build_line_index(self) -> None:
        self._lines = []
        start = 0
        for line_text in self._text.splitlines(keepends=True):
            self._lines.append((start, start + len(line_text.encode("utf-8"))))
            start += len(line_text.encode("utf-8"))

    def offset_to_position(self, utf8_offset: int) -> Position:
        if utf8_offset < 0:
            return Position(line=0, character=0)
        byte_text = self._text.encode("utf-8")
        if utf8_offset > len(byte_text):
            utf8_offset = len(byte_text)

        line = 0
        remaining = utf8_offset
        for line_start_utf8, line_end_utf8 in self._lines:
            line_len_utf8 = line_end_utf8 - line_start_utf8
            if remaining <= line_len_utf8:
                line_utf8_bytes = byte_text[line_start_utf8:line_end_utf8]
                character = self._byte_offset_to_character(line_utf8_bytes, remaining)
                return Position(line=line, character=character)
            remaining -= line_len_utf8
            line += 1
        return Position(line=line, character=0)

    def _byte_offset_to_character(self, line_bytes: bytes, offset: int) -> int:
        if self._encoding in ("utf16", "utf-16"):
            char_count = 0
            i = 0
            while i < offset and i < len(line_bytes):
                b = line_bytes[i]
                if b < 0x80:
                    i += 1
                elif b < 0xC0:
                    i += 1
                elif b < 0xE0:
                    i += 2
                elif b < 0xF0:
                    i += 3
                else:
                    i += 4
                char_count += 1
            utf16_len = 0
            i2 = 0
            while i2 < i and i2 < len(line_bytes):
                cp = self._utf8_decode_codepoint(line_bytes, i2)
                if cp >= 0x10000:
                    utf16_len += 2
                else:
                    utf16_len += 1
                b2 = line_bytes[i2]
                if b2 < 0x80:
                    i2 += 1
                elif b2 < 0xC0:
                    i2 += 1
                elif b2 < 0xE0:
                    i2 += 2
                elif b2 < 0xF0:
                    i2 += 3
                else:
                    i2 += 4
            return utf16_len
        elif self._encoding in ("utf32", "utf-32"):
            char_count = 0
            i = 0
            while i < offset and i < len(line_bytes):
                b = line_bytes[i]
                if b < 0x80:
                    i += 1
                elif b < 0xC0:
                    i += 1
                elif b < 0xE0:
                    i += 2
                elif b < 0xF0:
                    i += 3
                else:
                    i += 4
                char_count += 1
            return char_count
        else:
            char_count = 0
            i = 0
            while i < offset and i < len(line_bytes):
                b = line_bytes[i]
                if b < 0x80:
                    i += 1
                elif b < 0xC0:
                    i += 1
                elif b < 0xE0:
                    i += 2
                elif b < 0xF0:
                    i += 3
                else:
                    i += 4
                char_count += 1
            return char_count

    def _utf8_decode_codepoint(self, buf: bytes, pos: int) -> int:
        b = buf[pos]
        if b < 0x80:
            return b
        elif b < 0xC0:
            return b
        elif b < 0xE0:
            return ((b & 0x1F) << 6) | (buf[pos + 1] & 0x3F) if pos + 1 < len(buf) else b
        elif b < 0xF0:
            return (
                ((b & 0x0F) << 12)
                | ((buf[pos + 1] & 0x3F) << 6)
                | (buf[pos + 2] & 0x3F)
                if pos + 2 < len(buf)
                else b
            )
        else:
            return (
                ((b & 0x07) << 18)
                | ((buf[pos + 1] & 0x3F) << 12)
                | ((buf[pos + 2] & 0x3F) << 6)
                | (buf[pos + 3] & 0x3F)
                if pos + 3 < len(buf)
                else b
            )

    def position_to_offset(self, position: Position) -> int:
        byte_text = self._text.encode("utf-8")
        line_start_utf8, _ = self._lines[position.line] if position.line < len(self._lines) else (len(byte_text), len(byte_text))
        line_end_utf8 = self._lines[position.line][1] if position.line < len(self._lines) else len(byte_text)
        line_bytes = byte_text[line_start_utf8:line_end_utf8]
        utf8_offset = self._character_to_byte_offset(line_bytes, position.character)
        return line_start_utf8 + utf8_offset

    def _character_to_byte_offset(self, line_bytes: bytes, character: int) -> int:
        if character <= 0:
            return 0
        byte_pos = 0
        char_index = 0
        while byte_pos < len(line_bytes) and char_index < character:
            b = line_bytes[byte_pos]
            if b < 0x80:
                byte_pos += 1
            elif b < 0xC0:
                byte_pos += 1
            elif b < 0xE0:
                byte_pos += 2
            elif b < 0xF0:
                byte_pos += 3
            else:
                byte_pos += 4
            if self._encoding in ("utf16", "utf-16"):
                cp = self._utf8_decode_codepoint_at(line_bytes, char_index, byte_pos)
                if cp >= 0x10000:
                    char_index += 2
                else:
                    char_index += 1
            else:
                char_index += 1
        return byte_pos

    def _utf8_decode_codepoint_at(self, buf: bytes, start_char: int, byte_pos: int) -> int:
        pos = 0
        for _ in range(start_char):
            if pos >= len(buf):
                return 0
            b = buf[pos]
            if b < 0x80:
                pos += 1
            elif b < 0xC0:
                pos += 1
            elif b < 0xE0:
                pos += 2
            elif b < 0xF0:
                pos += 3
            else:
                pos += 4
        return self._utf8_decode_codepoint(buf, pos)


class BaseParser(ABC, Generic[TAst]):
    """Abstract base for all AEOS parsers."""

    file_extensions: set[str] = set()

    @abstractmethod
    def parse(self, text: str, uri: str) -> ParseResult[TAst]:
        ...

    @abstractmethod
    def parse_file(self, path: str) -> ParseResult[TAst]:
        ...

    def supports_extension(self, ext: str) -> bool:
        return ext.lower() in self.file_extensions

    def _text_to_lines(self, text: str) -> list[str]:
        return text.splitlines(keepends=True)

    def _make_range(self, text: str, start_offset: int, end_offset: int) -> Range:
        start = self._offset_to_position(text, start_offset)
        end = self._offset_to_position(text, end_offset)
        return Range(start=start, end=end)

    def _offset_to_position(self, text: str, offset: int) -> Position:
        if offset <= 0:
            return Position(line=0, character=0)
        if offset >= len(text):
            text_end = len(text)
            lines = text.splitlines(keepends=True)
            last_line_idx = len(lines) - 1
            if last_line_idx < 0:
                return Position(line=0, character=0)
            last_line = lines[last_line_idx]
            char_count = 0
            for ch in last_line:
                if ord(ch) >= 0x10000:
                    char_count += 2
                else:
                    char_count += 1
            return Position(line=last_line_idx, character=char_count)

        line = 0
        remaining = offset
        lines = text.splitlines(keepends=True)
        for line_text in lines:
            line_len = len(line_text)
            if remaining <= line_len:
                prefix = line_text[:remaining]
                char_count = 0
                for ch in prefix:
                    if ord(ch) >= 0x10000:
                        char_count += 2
                    else:
                        char_count += 1
                return Position(line=line, character=char_count)
            remaining -= line_len
            line += 1
        return Position(line=line, character=0)

    def _position_to_offset(self, text: str, position: Position) -> int:
        lines = text.splitlines(keepends=True)
        if position.line < 0 or position.line >= len(lines):
            return len(text)
        offset = 0
        for i in range(position.line):
            offset += len(lines[i])
        line_text = lines[position.line]
        char_count = 0
        byte_idx = 0
        while char_count < position.character and byte_idx < len(line_text):
            ch = line_text[byte_idx]
            if ord(ch) >= 0x10000:
                char_count += 2
            else:
                char_count += 1
            byte_idx += 1
        return offset + byte_idx
