from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import (
    BaseParser,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)


@dataclass(frozen=True)
class JsonComment:
    text: str
    range: Range
    comment_type: str = "line"

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
            "comment_type": self.comment_type,
        }


@dataclass(frozen=True)
class JsonAstNode:
    key: str
    value: Any
    key_range: Range | None = None
    value_range: Range | None = None
    node_type: str = "value"
    path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "key_range": {
                "start": {"line": self.key_range.start.line, "character": self.key_range.start.character},
                "end": {"line": self.key_range.end.line, "character": self.key_range.end.character},
            }
            if self.key_range
            else None,
            "value_range": {
                "start": {"line": self.value_range.start.line, "character": self.value_range.start.character},
                "end": {"line": self.value_range.end.line, "character": self.value_range.end.character},
            }
            if self.value_range
            else None,
            "node_type": self.node_type,
            "path": self.path,
        }


class PositionTrackingDecoder(json.JSONDecoder):
    """Custom JSON decoder that tracks positions of keys and values."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.nodes: list[JsonAstNode] = []
        self.comments: list[JsonComment] = []
        self.ranges: dict[str, Range] = {}
        self._path_stack: list[str] = []
        self._key_positions: dict[int, tuple[int, int, int, int]] = {}
        self._value_positions: dict[int, tuple[int, int, int, int]] = {}
        self._event_id: int = 0
        super().__init__(*args, **kwargs)

    def decode(self, s: str, _w: Any = None) -> Any:
        self._text = s
        self._lines = s.splitlines(keepends=True)
        self._line_offsets = self._build_line_offsets(s)
        self._parse_comments(s)
        return super().decode(s)

    def _build_line_offsets(self, text: str) -> list[int]:
        offsets = [0]
        for line in text.splitlines(keepends=True):
            offsets.append(offsets[-1] + len(line))
        return offsets

    def _parse_comments(self, text: str) -> None:
        lines = text.splitlines()
        in_block_comment = False
        block_start_line = 0
        block_start_col = 0
        block_text: list[str] = []

        for line_idx, line in enumerate(lines):
            stripped = line.strip()
            if in_block_comment:
                end_idx = stripped.find("*/")
                if end_idx != -1:
                    block_text.append(stripped[:end_idx])
                    self.comments.append(JsonComment(
                        text="\n".join(block_text),
                        range=Range(
                            start=Position(line=block_start_line, character=block_start_col),
                            end=Position(line=line_idx, character=end_idx + 2),
                        ),
                        comment_type="block",
                    ))
                    in_block_comment = False
                    block_text = []
                else:
                    block_text.append(stripped)
                continue
            if "//" in stripped:
                idx = stripped.index("//")
                comment_text = stripped[idx + 2:]
                start_char = line.index("//")
                self.comments.append(JsonComment(
                    text=comment_text,
                    range=Range(
                        start=Position(line=line_idx, character=start_char),
                        end=Position(line=line_idx, character=len(line.rstrip("\n\r"))),
                    ),
                    comment_type="line",
                ))
            if "/*" in stripped:
                idx = stripped.index("/*")
                end_idx = stripped.find("*/", idx + 2)
                if end_idx != -1:
                    self.comments.append(JsonComment(
                        text=stripped[idx + 2:end_idx],
                        range=Range(
                            start=Position(line=line_idx, character=line.index("/*")),
                            end=Position(line=line_idx, character=line.index("*/") + 2),
                        ),
                        comment_type="block",
                    ))
                else:
                    in_block_comment = True
                    block_start_line = line_idx
                    block_start_col = line.index("/*")
                    block_text = [stripped[idx + 2:]]

    def raw_decode(self, s: str, idx: int = 0) -> tuple[Any, int]:
        obj, end = super().raw_decode(s, idx)
        return obj, end


def strip_jsonc(text: str) -> str:
    result: list[str] = []
    lines = text.splitlines(keepends=True)
    in_block = False
    for line in lines:
        i = 0
        stripped = ""
        while i < len(line):
            if in_block:
                end_idx = line.find("*/", i)
                if end_idx != -1:
                    in_block = False
                    i = end_idx + 2
                else:
                    break
            elif line[i:i + 2] == "//":
                break
            elif line[i:i + 2] == "/*":
                in_block = True
                i += 2
            else:
                stripped += line[i]
                i += 1
        result.append(stripped)
    combined = "".join(result)
    combined = re.sub(r",\s*([}\]])", r"\1", combined)
    return combined


class JsonParser(BaseParser[list[JsonAstNode]]):
    file_extensions: set[str] = {".json", ".jsonc", ".aeos.json", ".aeos.jsonc"}

    def __init__(self) -> None:
        self._nodes: list[JsonAstNode] = []
        self._ranges: dict[str, Range] = {}
        self._comments: list[JsonComment] = []
        self._path_stack: list[str] = []
        self._text: str = ""
        self._lines: list[str] = []
        self._line_offsets: list[int] = []

    def parse(self, text: str, uri: str) -> ParseResult[list[JsonAstNode]]:
        self._nodes = []
        self._ranges = {}
        self._comments = []
        self._path_stack = []
        self._text = text
        self._lines = text.splitlines(keepends=True)
        self._line_offsets = self._build_line_offsets(text)
        errors: list[ParseError] = []

        if not text.strip():
            return ParseResult(ast=[], ranges={})

        is_jsonc = uri.endswith(".jsonc") or uri.endswith(".aeos.jsonc")
        clean_text = strip_jsonc(text) if is_jsonc else text

        try:
            raw_data = json.loads(clean_text)
            self._build_ast(raw_data, "", text, errors)
            self._detect_trailing_commas(text, errors)
            self._detect_comments_in_strict_json(text, is_jsonc, errors)

            return ParseResult(
                ast=self._nodes,
                errors=errors,
                ranges=self._ranges,
            )

        except json.JSONDecodeError as e:
            error_range = self._json_error_to_range(e, text)
            errors.append(ParseError(
                message=str(e),
                range=error_range,
                severity=ParseErrorSeverity.ERROR,
                code="JSON_PARSE_ERROR",
            ))
            partial = self._partial_parse(text)
            return ParseResult(ast=partial, errors=errors, ranges=self._ranges)

        except Exception as e:
            errors.append(ParseError(
                message=f"Unexpected JSON error: {e}",
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=0),
                ),
                severity=ParseErrorSeverity.ERROR,
                code="JSON_UNKNOWN_ERROR",
            ))
            return ParseResult(ast=self._nodes, errors=errors, ranges=self._ranges)

    def parse_file(self, path: str) -> ParseResult[list[JsonAstNode]]:
        text = Path(path).read_text(encoding="utf-8")
        return self.parse(text, path)

    def get_comments(self) -> list[JsonComment]:
        return list(self._comments)

    def _build_line_offsets(self, text: str) -> list[int]:
        offsets = [0]
        for line in text.splitlines(keepends=True):
            offsets.append(offsets[-1] + len(line))
        return offsets

    def _build_ast(
        self,
        data: Any,
        path: str,
        text: str,
        errors: list[ParseError],
    ) -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                child_path = f"{path}.{key}" if path else str(key)
                key_range = self._find_key_in_text(key, text)
                if key_range is not None:
                    self._ranges[f"key:{child_path}"] = key_range

                if isinstance(value, (dict, list)):
                    node_type = "object" if isinstance(value, dict) else "array"
                    value_range = self._find_value_range(key, value, text)
                    if value_range is not None:
                        self._ranges[child_path] = value_range
                    self._nodes.append(JsonAstNode(
                        key=str(key),
                        value=value,
                        key_range=key_range,
                        value_range=value_range,
                        node_type=node_type,
                        path=child_path,
                    ))
                    self._build_ast(value, child_path, text, errors)
                else:
                    value_range = self._find_value_range(key, value, text)
                    if value_range is not None:
                        self._ranges[child_path] = value_range
                    self._nodes.append(JsonAstNode(
                        key=str(key),
                        value=value,
                        key_range=key_range,
                        value_range=value_range,
                        node_type=self._json_type(value),
                        path=child_path,
                    ))
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                child_path = f"{path}[{idx}]"
                if isinstance(item, (dict, list)):
                    self._build_ast(item, child_path, text, errors)
                else:
                    value_range = self._find_array_item_range(text, idx, item)
                    if value_range is not None:
                        self._ranges[child_path] = value_range
                    self._nodes.append(JsonAstNode(
                        key=str(idx),
                        value=item,
                        value_range=value_range,
                        node_type=self._json_type(item),
                        path=child_path,
                    ))

    def _find_key_in_text(self, key: str, text: str) -> Range | None:
        pattern = re.compile(
            r'"' + re.escape(str(key)) + r'"\s*:',
            re.MULTILINE,
        )
        m = pattern.search(text)
        if m:
            key_start = m.start() + 1
            key_end = m.end() - 2
            start_pos = self._offset_to_position(key_start)
            end_pos = self._offset_to_position(key_end)
            return Range(start=start_pos, end=end_pos)
        return None

    def _find_value_range(self, key: str, value: Any, text: str) -> Range | None:
        pattern = re.compile(
            r'"' + re.escape(str(key)) + r'"\s*:\s*',
            re.MULTILINE,
        )
        m = pattern.search(text)
        if m:
            value_start = m.end()
            if isinstance(value, str):
                val_str = json.dumps(value)
                val_end = value_start + len(val_str)
                return Range(
                    start=self._offset_to_position(value_start),
                    end=self._offset_to_position(val_end),
                )
            elif value is None:
                end = value_start + 4
                return Range(
                    start=self._offset_to_position(value_start),
                    end=self._offset_to_position(end),
                )
            elif isinstance(value, bool):
                end = value_start + (4 if value else 5)
                return Range(
                    start=self._offset_to_position(value_start),
                    end=self._offset_to_position(end),
                )
            elif isinstance(value, (int, float)):
                val_str = str(value)
                end = value_start + len(val_str)
                return Range(
                    start=self._offset_to_position(value_start),
                    end=self._offset_to_position(end),
                )
            else:
                end = value_start
                depth = 1
                in_str = False
                while end < len(text) and depth > 0:
                    ch = text[end]
                    if in_str:
                        if ch == "\\":
                            end += 1
                        elif ch == '"':
                            in_str = False
                    else:
                        if ch == '"':
                            in_str = True
                        elif ch in ("{", "["):
                            depth += 1
                        elif ch in ("}", "]"):
                            depth -= 1
                    end += 1
                return Range(
                    start=self._offset_to_position(value_start),
                    end=self._offset_to_position(end),
                )
        return None

    def _find_array_item_range(self, text: str, idx: int, value: Any) -> Range | None:
        lines = text.splitlines()
        count = 0
        for line_idx, line in enumerate(lines):
            for ch_idx, ch in enumerate(line):
                if ch == "," or ch in ("[", "]"):
                    continue
                if ch in ("-", "+") or ch.isdigit() or ch == '"' or ch in ("t", "f", "n"):
                    if count == idx:
                        if isinstance(value, str):
                            quote_start = line.index('"', ch_idx) if '"' in line[ch_idx:] else ch_idx
                            return Range(
                                start=Position(line=line_idx, character=quote_start),
                                end=Position(line=line_idx, character=quote_start + len(value) + 2),
                            )
                    count += 1
        return None

    def _detect_trailing_commas(self, text: str, errors: list[ParseError]) -> None:
        for line_idx, line in enumerate(text.splitlines()):
            stripped = line.strip()
            if stripped.endswith(",]") or stripped.endswith(",}"):
                comma_idx = line.rindex(",")
                errors.append(ParseError(
                    message="Trailing comma",
                    range=Range(
                        start=Position(line=line_idx, character=comma_idx),
                        end=Position(line=line_idx, character=comma_idx + 1),
                    ),
                    severity=ParseErrorSeverity.WARNING,
                    code="JSON_TRAILING_COMMA",
                ))

    def _detect_comments_in_strict_json(self, text: str, is_jsonc: bool, errors: list[ParseError]) -> None:
        if is_jsonc:
            return
        for line_idx, line in enumerate(text.splitlines()):
            stripped = line.strip()
            if "//" in stripped:
                idx = stripped.index("//")
                errors.append(ParseError(
                    message="Comments are not allowed in strict JSON",
                    range=Range(
                        start=Position(line=line_idx, character=line.index("//")),
                        end=Position(line=line_idx, character=len(line.rstrip("\n\r"))),
                    ),
                    severity=ParseErrorSeverity.ERROR,
                    code="JSON_COMMENT_IN_STRICT",
                ))

    def _json_error_to_range(self, error: json.JSONDecodeError, text: str) -> Range:
        pos = error.pos
        if pos >= len(text):
            pos = len(text) - 1 if text else 0
        start = self._offset_to_position(pos)
        end = Position(line=start.line, character=start.character + 1)
        return Range(start=start, end=end)

    def _partial_parse(self, text: str) -> list[JsonAstNode]:
        nodes: list[JsonAstNode] = []
        try:
            cleaned = strip_jsonc(text)
            data = json.loads(cleaned)
            self._build_ast(data, "", text, [])
            nodes = self._nodes
        except Exception:
            pass
        return nodes

    def _json_type(self, value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        if isinstance(value, float):
            return "number"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "object"
        return "unknown"

    def _offset_to_position(self, offset: int) -> Position:
        if offset <= 0:
            return Position(line=0, character=0)
        if offset >= len(self._text):
            lines_count = len(self._lines)
            if lines_count == 0:
                return Position(line=0, character=0)
            last_line = self._lines[-1]
            char_count = 0
            for ch in last_line:
                char_count += 2 if ord(ch) >= 0x10000 else 1
            return Position(line=lines_count - 1, character=char_count)

        line = 0
        remaining = offset
        for line_text in self._lines:
            line_len = len(line_text)
            if remaining <= line_len:
                prefix = line_text[:remaining]
                char_count = 0
                for ch in prefix:
                    char_count += 2 if ord(ch) >= 0x10000 else 1
                return Position(line=line, character=char_count)
            remaining -= line_len
            line += 1
        return Position(line=line, character=0)
