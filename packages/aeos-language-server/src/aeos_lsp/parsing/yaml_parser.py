from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from yaml.parser import ParserError as YamlParserError
from yaml.scanner import ScannerError as YamlScannerError

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import (
    BaseParser,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)


class AeoSDocumentType(Enum):
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"
    REGISTRY = "registry"
    CONFIG = "config"
    PERMISSIONS = "permissions"
    POLICIES = "policies"
    OVERLAY = "overlay"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class YamlAstNode:
    key: str
    value: Any
    key_range: Range | None = None
    value_range: Range | None = None
    parent_key: str | None = None
    node_type: str = "scalar"

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "key_range": self._range_to_dict(self.key_range),
            "value_range": self._range_to_dict(self.value_range),
            "node_type": self.node_type,
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
class YamlDocument:
    nodes: list[YamlAstNode] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)
    document_type: AeoSDocumentType = AeoSDocumentType.UNKNOWN
    multi_doc_index: int = 0
    tags: set[str] = field(default_factory=set)
    anchors: dict[str, Any] = field(default_factory=dict)


class YamlParser(BaseParser[YamlDocument]):
    file_extensions: set[str] = {".yaml", ".yml", ".aeos.yaml", ".aeos.yml"}

    def parse(self, text: str, uri: str) -> ParseResult[YamlDocument]:
        errors: list[ParseError] = []
        ranges: dict[str, Range] = {}
        docs: list[YamlDocument] = []

        if not text.strip():
            doc = YamlDocument(document_type=AeoSDocumentType.UNKNOWN)
            return ParseResult(ast=doc, ranges=ranges)

        try:
            loaded = list(yaml.compose_all(text))
            for doc_idx, node in enumerate(loaded):
                raw_data: dict[str, Any] = {}
                nodes: list[YamlAstNode] = []
                doc_ranges: dict[str, Range] = {}
                anchor_map: dict[str, Any] = {}
                if isinstance(node, yaml.MappingNode):
                    self._process_mapping_node(node, raw_data, nodes, doc_ranges, [], anchor_map)
                elif isinstance(node, yaml.SequenceNode):
                    raw_data = self._sequence_to_list(node)
                elif isinstance(node, yaml.ScalarNode):
                    raw_data = self._scalar_value(node)

                doc = YamlDocument(
                    nodes=nodes,
                    raw_data=raw_data,
                    document_type=self._detect_aeos_type(raw_data),
                    multi_doc_index=doc_idx,
                    anchors=anchor_map,
                )
                docs.append(doc)
                ranges.update(doc_ranges)

            merged = self._merge_documents(docs)
            return ParseResult(ast=merged, errors=errors, ranges=ranges)

        except YamlParserError as e:
            error_range = self._yaml_error_to_range(e, text)
            errors.append(ParseError(
                message=str(e),
                range=error_range,
                severity=ParseErrorSeverity.ERROR,
                code="YAML_PARSE_ERROR",
            ))
            return ParseResult(
                ast=YamlDocument(document_type=AeoSDocumentType.UNKNOWN),
                errors=errors,
            )

        except YamlScannerError as e:
            error_range = self._yaml_error_to_range(e, text)
            errors.append(ParseError(
                message=str(e),
                range=error_range,
                severity=ParseErrorSeverity.ERROR,
                code="YAML_SCAN_ERROR",
            ))
            return ParseResult(
                ast=YamlDocument(document_type=AeoSDocumentType.UNKNOWN),
                errors=errors,
            )

        except Exception as e:
            errors.append(ParseError(
                message=f"YAML error: {e}",
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
                severity=ParseErrorSeverity.ERROR,
                code="YAML_UNKNOWN_ERROR",
            ))
            return ParseResult(
                ast=YamlDocument(document_type=AeoSDocumentType.UNKNOWN),
                errors=errors,
            )

    def parse_file(self, path: str) -> ParseResult[YamlDocument]:
        text = Path(path).read_text(encoding="utf-8")
        return self.parse(text, path)

    def _process_mapping_node(
        self,
        node: yaml.MappingNode,
        raw_data: dict[str, Any],
        nodes: list[YamlAstNode],
        ranges: dict[str, Range],
        path: list[str],
        anchor_map: dict[str, Any],
    ) -> None:
        for key_node, value_node in node.value:
            key = self._scalar_value(key_node)
            current_path = ".".join(path + [str(key)]) if path else str(key)

            key_range = self._node_to_range(key_node)
            if key_range is not None:
                ranges[f"key:{current_path}"] = key_range

            if isinstance(value_node, yaml.MappingNode):
                child_data: dict[str, Any] = {}
                raw_data[key] = child_data
                value_range = self._node_to_range(value_node)
                if value_range is not None:
                    ranges[current_path] = value_range
                    nodes.append(YamlAstNode(
                        key=str(key),
                        value=child_data,
                        key_range=key_range,
                        value_range=value_range,
                        node_type="mapping",
                    ))
                self._process_mapping_node(value_node, child_data, nodes, ranges, path + [str(key)], anchor_map)

            elif isinstance(value_node, yaml.SequenceNode):
                seq_data = self._sequence_to_list(value_node)
                raw_data[key] = seq_data
                value_range = self._node_to_range(value_node)
                if value_range is not None:
                    ranges[current_path] = value_range
                    nodes.append(YamlAstNode(
                        key=str(key),
                        value=seq_data,
                        key_range=key_range,
                        value_range=value_range,
                        node_type="sequence",
                    ))

            elif isinstance(value_node, yaml.ScalarNode):
                scalar_val = self._scalar_value(value_node)
                raw_data[key] = scalar_val
                value_range = self._node_to_range(value_node)
                if value_range is not None:
                    ranges[current_path] = value_range
                    nodes.append(YamlAstNode(
                        key=str(key),
                        value=scalar_val,
                        key_range=key_range,
                        value_range=value_range,
                        node_type="scalar",
                    ))

                if value_node.tag:
                    anchor_map[key] = scalar_val

            elif isinstance(value_node, yaml.AliasNode):
                alias_val = f"<<:{value_node.anchor}"
                raw_data[key] = alias_val
                value_range = self._node_to_range(value_node)
                if value_range is not None:
                    ranges[current_path] = value_range
                    nodes.append(YamlAstNode(
                        key=str(key),
                        value=alias_val,
                        key_range=key_range,
                        value_range=value_range,
                        node_type="alias",
                    ))

    def _sequence_to_list(self, node: yaml.SequenceNode) -> list[Any]:
        result: list[Any] = []
        for item in node.value:
            if isinstance(item, yaml.ScalarNode):
                result.append(self._scalar_value(item))
            elif isinstance(item, yaml.MappingNode):
                child: dict[str, Any] = {}
                for k, v in item.value:
                    child[self._scalar_value(k)] = self._scalar_value(v) if isinstance(v, yaml.ScalarNode) else {}
                result.append(child)
            elif isinstance(item, yaml.SequenceNode):
                result.append(self._sequence_to_list(item))
            elif isinstance(item, yaml.AliasNode):
                result.append(f"<<:{item.anchor}")
        return result

    def _scalar_value(self, node: yaml.ScalarNode) -> Any:
        value = node.value
        if node.tag == "tag:yaml.org,2002:null" or value.lower() in ("null", "~") if isinstance(value, str) else False:
            return None
        if node.tag == "tag:yaml.org,2002:bool" or value.lower() in ("true", "false", "yes", "no", "on", "off") if isinstance(value, str) else False:
            return value.lower() in ("true", "yes", "on")
        if node.tag == "tag:yaml.org,2002:int":
            try:
                return int(value)
            except (ValueError, TypeError):
                return value
        if node.tag == "tag:yaml.org,2002:float":
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        if node.tag and node.tag.startswith("tag:yaml.org,2002:"):
            return value
        return value

    def _node_to_range(self, node: yaml.Node) -> Range | None:
        start_mark = getattr(node, "start_mark", None)
        end_mark = getattr(node, "end_mark", None)
        if start_mark is not None and end_mark is not None:
            return Range(
                start=Position(line=start_mark.line, character=start_mark.column),
                end=Position(line=end_mark.line, character=end_mark.column),
            )
        return None

    def _yaml_error_to_range(self, error: Exception, text: str) -> Range:
        problem_mark = getattr(error, "problem_mark", None)
        context_mark = getattr(error, "context_mark", None)
        mark = problem_mark or context_mark
        if mark is not None:
            return Range(
                start=Position(line=mark.line, character=mark.column),
                end=Position(line=mark.line, character=mark.column + 1),
            )
        note = getattr(error, "note", None)
        if note:
            m = re.search(r"line (\d+), column (\d+)", str(note))
            if m:
                line = int(m.group(1)) - 1
                col = int(m.group(2)) - 1
                return Range(
                    start=Position(line=line, character=col),
                    end=Position(line=line, character=col + 1),
                )
        return Range(start=Position(line=0, character=0), end=Position(line=0, character=0))

    def _detect_duplicate_keys(self, text: str, errors: list[ParseError]) -> None:
        scope_stack: list[dict[str, int]] = [{}]
        prev_indent: int | None = None
        for line_idx, line in enumerate(text.splitlines()):
            stripped = line.rstrip()
            if not stripped or stripped.startswith("#"):
                continue
            m = re.match(r"^(\s*)([\w_-]+)\s*:", line)
            if not m:
                continue
            key = m.group(2)
            indent = len(m.group(1))

            if prev_indent is None:
                pass
            elif indent > prev_indent:
                pass
            elif indent < prev_indent:
                levels_up = (prev_indent - indent) // 2
                for _ in range(levels_up):
                    if len(scope_stack) > 1:
                        scope_stack.pop()

            if key in scope_stack[-1]:
                errors.append(ParseError(
                    message=f"Duplicate key '{key}'",
                    range=Range(
                        start=Position(line=line_idx, character=indent),
                        end=Position(line=line_idx, character=indent + len(key)),
                    ),
                    severity=ParseErrorSeverity.ERROR,
                    code="YAML_DUPLICATE_KEY",
                ))
            else:
                scope_stack[-1][key] = line_idx

            prev_indent = indent

    def _detect_aeos_type(self, data: dict[str, Any]) -> AeoSDocumentType:
        if not isinstance(data, dict):
            return AeoSDocumentType.UNKNOWN
        keys = set(data.keys())
        if "aeos" in keys and "runtime" in keys:
            return AeoSDocumentType.CONFIG
        if "agent" in keys or "agents" in keys:
            return AeoSDocumentType.AGENT
        if "skill" in keys or "skills" in keys:
            return AeoSDocumentType.SKILL
        if "playbook" in keys or "playbooks" in keys:
            return AeoSDocumentType.PLAYBOOK
        if "registry" in keys or any(k.endswith(".registry") for k in keys):
            return AeoSDocumentType.REGISTRY
        if "permissions" in keys or "permission" in keys:
            return AeoSDocumentType.PERMISSIONS
        if "policies" in keys or "policy" in keys:
            return AeoSDocumentType.POLICIES
        if "overlay" in keys or data.get("kind") == "overlay":
            return AeoSDocumentType.OVERLAY
        return AeoSDocumentType.UNKNOWN

    def _merge_documents(self, docs: list[YamlDocument]) -> YamlDocument:
        if not docs:
            return YamlDocument(document_type=AeoSDocumentType.UNKNOWN)
        if len(docs) == 1:
            return docs[0]
        merged_nodes: list[YamlAstNode] = []
        merged_data: dict[str, Any] = {}
        merged_tags: set[str] = set()
        merged_anchors: dict[str, Any] = {}
        for doc in docs:
            merged_nodes.extend(doc.nodes)
            merged_data.update(doc.raw_data)
            merged_tags.update(doc.tags)
            merged_anchors.update(doc.anchors)
        return YamlDocument(
            nodes=merged_nodes,
            raw_data=merged_data,
            document_type=self._detect_aeos_type(merged_data),
            tags=merged_tags,
            anchors=merged_anchors,
        )
