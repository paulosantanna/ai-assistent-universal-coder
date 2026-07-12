from __future__ import annotations

import re
from typing import Literal

from lsprotocol.types import Position

Encoding = Literal["utf-8", "utf-16", "utf-32"]


class PositionMapper:
    """Handles encoding-aware position mapping for LSP compatibility.

    Supports UTF-8, UTF-16, and UTF-32 position encodings.
    UTF-16 is the default (and most common) for LSP clients.
    """

    def __init__(self, text: str, encoding: Encoding = "utf-16") -> None:
        self._text = text
        self._encoding = encoding
        self._text_bytes = text.encode("utf-8")
        self._byte_lines: list[tuple[int, int]] = []
        self._build_byte_line_index()

    def _build_byte_line_index(self) -> None:
        start = 0
        for line_text in self._text.splitlines(keepends=True):
            line_utf8_len = len(line_text.encode("utf-8"))
            self._byte_lines.append((start, start + line_utf8_len))
            start += line_utf8_len

    @property
    def encoding(self) -> str:
        return self._encoding

    @property
    def line_count(self) -> int:
        return len(self._byte_lines)

    def offset_to_position(self, utf8_offset: int) -> Position:
        if utf8_offset <= 0:
            return Position(line=0, character=0)
        if utf8_offset >= len(self._text_bytes):
            return self._eof_position()

        line = 0
        remaining = utf8_offset
        for line_start, line_end in self._byte_lines:
            line_len = line_end - line_start
            if remaining <= line_len or line == len(self._byte_lines) - 1:
                char_count = self._count_characters_in_range(
                    self._text_bytes[line_start:line_end], 0, remaining
                )
                return Position(line=line, character=char_count)
            remaining -= line_len
            line += 1
        return self._eof_position()

    def position_to_offset(self, position: Position) -> int:
        if position.line < 0:
            return 0
        if position.line >= len(self._byte_lines):
            return len(self._text_bytes)

        line_start, line_end = self._byte_lines[position.line]
        line_bytes = self._text_bytes[line_start:line_end]
        utf8_offset = self._character_to_byte_offset(line_bytes, position.character)
        return line_start + utf8_offset

    def get_line_range(self, line: int) -> tuple[int, int]:
        if line < 0 or line >= len(self._byte_lines):
            return (0, 0)
        return self._byte_lines[line]

    def _count_characters_in_range(self, buf: bytes, start_byte: int, end_byte: int) -> int:
        count = 0
        i = start_byte
        while i < end_byte and i < len(buf):
            b = buf[i]
            if b < 0x80:
                i += 1
                count += 1
            elif b < 0xC0:
                i += 1
                count += 1
            elif b < 0xE0:
                i += 2
                count += 1
            elif b < 0xF0:
                i += 3
                count += 1
            else:
                i += 4
                count += 1
        return count

    def _character_to_byte_offset(self, line_bytes: bytes, character: int) -> int:
        if character <= 0:
            return 0
        byte_pos = 0
        char_index = 0
        while byte_pos < len(line_bytes) and char_index < character:
            b = line_bytes[byte_pos]
            cp = self._decode_utf8_codepoint(line_bytes, byte_pos)
            if self._encoding == "utf-16" and cp >= 0x10000:
                char_index += 2
            else:
                char_index += 1
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
        return byte_pos

    def _decode_utf8_codepoint(self, buf: bytes, pos: int) -> int:
        b = buf[pos]
        if b < 0x80:
            return b
        elif b < 0xC0:
            return b
        elif b < 0xE0:
            if pos + 1 >= len(buf):
                return b
            return ((b & 0x1F) << 6) | (buf[pos + 1] & 0x3F)
        elif b < 0xF0:
            if pos + 2 >= len(buf):
                return b
            return (
                ((b & 0x0F) << 12)
                | ((buf[pos + 1] & 0x3F) << 6)
                | (buf[pos + 2] & 0x3F)
            )
        else:
            if pos + 3 >= len(buf):
                return b
            return (
                ((b & 0x07) << 18)
                | ((buf[pos + 1] & 0x3F) << 12)
                | ((buf[pos + 2] & 0x3F) << 6)
                | (buf[pos + 3] & 0x3F)
            )

    def _eof_position(self) -> Position:
        if not self._byte_lines:
            return Position(line=0, character=0)
        last_line_idx = len(self._byte_lines) - 1
        last_line_start, last_line_end = self._byte_lines[last_line_idx]
        last_line_bytes = self._text_bytes[last_line_start:last_line_end]
        char_count = self._count_characters_in_range(last_line_bytes, 0, len(last_line_bytes))
        return Position(line=last_line_idx, character=char_count)

    def offset_to_position_utf8(self, utf8_offset: int) -> Position:
        return self.offset_to_position(utf8_offset)

    def position_to_offset_utf8(self, position: Position) -> int:
        return self.position_to_offset(position)

    def offset_to_position_utf16(self, utf8_offset: int) -> Position:
        saved = self._encoding
        self._encoding = "utf-16"
        try:
            return self.offset_to_position(utf8_offset)
        finally:
            self._encoding = saved

    def position_to_offset_utf16(self, position: Position) -> int:
        saved = self._encoding
        self._encoding = "utf-16"
        try:
            return self.position_to_offset(position)
        finally:
            self._encoding = saved

    def offset_to_position_utf32(self, utf8_offset: int) -> Position:
        saved = self._encoding
        self._encoding = "utf-32"
        try:
            return self.offset_to_position(utf8_offset)
        finally:
            self._encoding = saved

    def position_to_offset_utf32(self, position: Position) -> int:
        saved = self._encoding
        self._encoding = "utf-32"
        try:
            return self.position_to_offset(position)
        finally:
            self._encoding = saved


def offset_to_position(text: str, offset: int, encoding: Encoding = "utf-16") -> Position:
    mapper = PositionMapper(text, encoding)
    return mapper.offset_to_position(offset)


def position_to_offset(text: str, line: int, character: int, encoding: Encoding = "utf-16") -> int:
    mapper = PositionMapper(text, encoding)
    return mapper.position_to_offset(Position(line=line, character=character))


def get_line_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 0
    for line_text in text.splitlines(keepends=True):
        end = start + len(line_text.encode("utf-8"))
        ranges.append((start, end))
        start = end
    if not text.endswith("\n") and text:
        last_line = text.splitlines(keepends=True)[-1]
        ranges.append((start, start + len(last_line.encode("utf-8"))))
    elif not text:
        ranges.append((0, 0))
    return ranges


_ENCODING_RE = re.compile(r"^(.+?)(?:\s*;\s*charset=)?([\w-]+)?", re.IGNORECASE)
_UTF_BOMS = {
    b"\xef\xbb\xbf": "utf-8",
    b"\xff\xfe": "utf-16-le",
    b"\xfe\xff": "utf-16-be",
    b"\xff\xfe\x00\x00": "utf-32-le",
    b"\x00\x00\xfe\xff": "utf-32-be",
}


def guess_encoding(text: str, declared: str | None = None) -> str:
    if declared:
        declared = declared.lower().replace("-", "").replace("_", "")
        if declared in ("utf8", "utf16", "utf32", "utf16le", "utf16be", "utf32le", "utf32be"):
            return declared
    raw = text.encode("utf-8") if isinstance(text, str) else text
    for bom, enc in _UTF_BOMS.items():
        if raw.startswith(bom):
            return enc
    if isinstance(raw, bytes):
        try:
            raw.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            try:
                raw.decode("latin-1")
                return "latin-1"
            except UnicodeDecodeError:
                return "utf-8"
    return "utf-8"
