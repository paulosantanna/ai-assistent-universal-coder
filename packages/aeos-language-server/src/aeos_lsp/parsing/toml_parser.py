from __future__ import annotations

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

try:
    import tomli
except ImportError:
    tomli = None


@dataclass(frozen=True)
class TomlAstNode:
    key: str
    value: Any
    key_range: Range | None = None
    value_range: Range | None = None
    node_type: str = "string"
    table_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "key_range": self._range_to_dict(self.key_range),
            "value_range": self._range_to_dict(self.value_range),
            "node_type": self.node_type,
            "table_path": self.table_path,
        }

    @staticmethod
    def _range_to_dict(r: Range | None) -> dict[str, Any] | None:
        if r is None:
            return None
        return {
            "start": {"line": r.start.line, "character": r.start.character},
            "end": {"line": r.end.line, "character": r.end.character},
        }


@dataclass(frozen=True)
class TomlDocument:
    nodes: list[TomlAstNode] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)
    tables: dict[str, Range] = field(default_factory=dict)
    errors: list[ParseError] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "tables": {k: self._range_to_dict(v) for k, v in self.tables.items()},
        }

    @staticmethod
    def _range_to_dict(r: Range | None) -> dict[str, Any] | None:
        if r is None:
            return None
        return {
            "start": {"line": r.start.line, "character": r.start.character},
            "end": {"line": r.end.line, "character": r.end.character},
        }


class TomlParser(BaseParser[TomlDocument]):
    file_extensions: set[str] = {".toml", ".aeos.toml"}

    def __init__(self) -> None:
        self._text: str = ""
        self._lines: list[str] = []

    def parse(self, text: str, uri: str) -> ParseResult[TomlDocument]:
        self._text = text
        self._lines = text.splitlines(keepends=True)
        errors: list[ParseError] = []
        nodes: list[TomlAstNode] = []
        tables: dict[str, Range] = {}
        ranges: dict[str, Range] = {}

        if not text.strip():
            return ParseResult(ast=TomlDocument(), ranges=ranges)

        if tomli is None:
            errors.append(ParseError(
                message="tomli module is required for TOML parsing",
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
                severity=ParseErrorSeverity.ERROR,
                code="TOML_MISSING_MODULE",
            ))
            return ParseResult(ast=TomlDocument(), errors=errors, ranges=ranges)

        try:
            raw_data = tomli.loads(text)
            current_table_path = ""

            for line_idx, line in enumerate(self._lines):
                stripped = line.strip()

                if not stripped or stripped.startswith("#"):
                    continue

                table_match = re.match(r"^\[{1,2}(.+?)\]{1,2}\s*(?:#.*)?$", stripped)
                if table_match:
                    table_name = table_match.group(1).strip()
                    current_table_path = table_name
                    tables[table_name] = Range(
                        start=Position(line=line_idx, character=line.index("[")),
                        end=Position(line=line_idx, character=line.rindex("]") + 1),
                    )
                    continue

                kv_match = re.match(
                    r"^([a-zA-Z_][a-zA-Z0-9_\-\.]*)\s*=\s*(.+?)\s*(?:#.*)?$",
                    stripped,
                )
                if kv_match:
                    full_key = kv_match.group(1).strip()
                    value_str = kv_match.group(2).strip()
                    eq_idx = line.index("=")
                    key_start_char = line.index(full_key.split(".")[0])
                    key_end_char = eq_idx

                    resolved_value = self._resolve_value(raw_data, current_table_path, full_key)

                    node_type = self._detect_type(value_str)

                    key_range = Range(
                        start=Position(line=line_idx, character=key_start_char),
                        end=Position(line=line_idx, character=key_end_char),
                    )
                    value_end_char = key_end_char + 1 + len(value_str)
                    value_range = Range(
                        start=Position(line=line_idx, character=key_end_char + 1),
                        end=Position(line=line_idx, character=value_end_char),
                    )

                    full_path = f"{current_table_path}.{full_key}" if current_table_path else full_key
                    ranges[f"key:{full_path}"] = key_range
                    ranges[full_path] = value_range

                    node = TomlAstNode(
                        key=full_key,
                        value=resolved_value,
                        key_range=key_range,
                        value_range=value_range,
                        node_type=node_type,
                        table_path=current_table_path,
                    )
                    nodes.append(node)

            doc = TomlDocument(
                nodes=nodes,
                raw_data=raw_data,
                tables=tables,
            )
            return ParseResult(ast=doc, errors=errors, ranges=ranges)

        except tomli.TOMLDecodeError as e:
            error_range = self._toml_error_to_range(e, text)
            errors.append(ParseError(
                message=str(e),
                range=error_range,
                severity=ParseErrorSeverity.ERROR,
                code="TOML_PARSE_ERROR",
            ))
            partial_nodes = self._partial_parse(text)
            doc = TomlDocument(nodes=partial_nodes, raw_data={}, tables=tables)
            return ParseResult(ast=doc, errors=errors, ranges=ranges)

        except Exception as e:
            errors.append(ParseError(
                message=f"Unexpected TOML error: {e}",
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
                severity=ParseErrorSeverity.ERROR,
                code="TOML_UNKNOWN_ERROR",
            ))
            doc = TomlDocument(nodes=nodes, raw_data={}, tables=tables)
            return ParseResult(ast=doc, errors=errors, ranges=ranges)

    def parse_file(self, path: str) -> ParseResult[TomlDocument]:
        text = Path(path).read_text(encoding="utf-8")
        return self.parse(text, path)

    def _resolve_value(self, data: dict[str, Any], table_path: str, key: str) -> Any:
        parts = table_path.split(".") if table_path else []
        current: Any = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part, {})
            else:
                return None
        key_parts = key.split(".")
        for part in key_parts:
            if isinstance(current, dict):
                current = current.get(part, None)
            else:
                return None
        return current

    def _detect_type(self, value_str: str) -> str:
        stripped = value_str.strip()
        if stripped.startswith('"') or stripped.startswith("'"):
            return "string"
        if stripped.startswith("["):
            return "array"
        if stripped.startswith("{"):
            return "inline_table"
        if stripped in ("true", "false"):
            return "boolean"
        if stripped.startswith(("+", "-")) or stripped[0].isdigit():
            if "." in stripped or "e" in stripped or "E" in stripped:
                return "float"
            return "integer"
        if stripped.startswith("@"):
            return "datetime"
        return "unknown"

    def _toml_error_to_range(self, error: tomli.TOMLDecodeError, text: str) -> Range:
        msg = str(error)
        line_match = re.search(r"line (\d+)", msg)
        col_match = re.search(r"column (\d+)", msg)
        pos_match = re.search(r"at position (\d+)", msg)

        if pos_match:
            pos = int(pos_match.group(1))
            return self._make_range_from_offset(pos)

        if line_match:
            line = int(line_match.group(1)) - 1
            col = int(col_match.group(1)) - 1 if col_match else 0
            return Range(
                start=Position(line=line, character=col),
                end=Position(line=line, character=col + 1),
            )

        return Range(start=Position(line=0, character=0), end=Position(line=0, character=0))

    def _make_range_from_offset(self, offset: int) -> Range:
        line = 0
        remaining = offset
        for line_text in self._lines:
            line_len = len(line_text)
            if remaining <= line_len:
                char_count = 0
                for ch in line_text[:remaining]:
                    char_count += 2 if ord(ch) >= 0x10000 else 1
                return Range(
                    start=Position(line=line, character=char_count),
                    end=Position(line=line, character=char_count + 1),
                )
            remaining -= line_len
            line += 1
        return Range(start=Position(line=0, character=0), end=Position(line=0, character=0))

    def _partial_parse(self, text: str) -> list[TomlAstNode]:
        nodes: list[TomlAstNode] = []
        current_table = ""

        for line_idx, line in enumerate(text.splitlines()):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            table_match = re.match(r"^\[{1,2}(.+?)\]{1,2}\s*(?:#.*)?$", stripped)
            if table_match:
                current_table = table_match.group(1).strip()
                continue

            kv_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_\-\.]*)\s*=\s*(.+?)\s*(?:#.*)?$", stripped)
            if kv_match:
                key = kv_match.group(1).strip()
                value_str = kv_match.group(2).strip()
                eq_idx = line.index("=")
                key_range = Range(
                    start=Position(line=line_idx, character=line.index(key.split(".")[0])),
                    end=Position(line=line_idx, character=eq_idx),
                )
                value_range = Range(
                    start=Position(line=line_idx, character=eq_idx + 1),
                    end=Position(line=line_idx, character=eq_idx + 1 + len(value_str)),
                )
                node = TomlAstNode(
                    key=key,
                    value=value_str,
                    key_range=key_range,
                    value_range=value_range,
                    node_type=self._detect_type(value_str),
                    table_path=current_table,
                )
                nodes.append(node)

        return nodes
