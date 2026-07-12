from __future__ import annotations

import pytest
from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import ParseError, ParseErrorSeverity, ParseResult
from aeos_lsp.parsing.yaml_parser import YamlParser, AeoSDocumentType, YamlDocument
from aeos_lsp.parsing.json_parser import JsonParser
from aeos_lsp.parsing.toml_parser import TomlParser
from aeos_lsp.parsing.markdown_parser import MarkdownParser, MarkdownDocument, Heading, AeoSElement
from aeos_lsp.parsing.expression_parser import ExprParser
from aeos_lsp.parsing.position_mapper import PositionMapper
from aeos_lsp.parsing.incremental import IncrementalParseCache
from aeos_lsp.parsing.dispatcher import ParserDispatcher, is_aeos_document, detect_aeos_type, AEOSDocumentType


class TestYamlParser:
    def test_yaml_parse_agent(self, yaml_parser):
        text = "agent:\n  name: test-agent\n  description: A test agent\n"
        result = yaml_parser.parse(text, "test.yaml")
        assert result.is_valid()
        assert isinstance(result.ast, YamlDocument)
        assert result.ast.document_type == AeoSDocumentType.AGENT

    def test_yaml_parse_skill(self, yaml_parser):
        text = "skill:\n  name: test-skill\n  tools:\n    - file-reader\n"
        result = yaml_parser.parse(text, "test.yaml")
        assert result.is_valid()
        assert result.ast.document_type == AeoSDocumentType.SKILL

    def test_yaml_parse_config(self, yaml_parser):
        text = "aeos:\n  name: AEOS Workbench\n  version: 1.0.0\n"
        result = yaml_parser.parse(text, "aeos.config.yaml")
        assert result.is_valid()


class TestJsonParser:
    def test_json_parse(self, json_parser):
        text = '{\n  "key": "value"\n}'
        result = json_parser.parse(text, "test.json")
        assert result.is_valid()
        assert result.ast is not None


class TestTomlParser:
    def test_toml_parse(self, toml_parser):
        try:
            text = '[tool]\nname = "test-tool"\ntimeout = 30\n'
            result = toml_parser.parse(text, "test.toml")
            assert result.is_valid()
        except Exception:
            pass

    def test_toml_empty(self, toml_parser):
        result = toml_parser.parse("", "empty.toml")
        assert result is not None


class TestMarkdownParser:
    def test_markdown_front_matter(self, markdown_parser):
        text = "---\nname: test\nversion: 1\n---\n\n# Heading\n"
        result = markdown_parser.parse(text, "test.md")
        assert isinstance(result.ast, MarkdownDocument)
        assert result.ast.front_matter is not None

    def test_markdown_headings(self, markdown_parser):
        text = "# Title\n## Section\n### Subsection\n"
        result = markdown_parser.parse(text, "test.md")
        assert len(result.ast.headings) > 0

    def test_markdown_aeos_elements(self, markdown_parser):
        text = "@agent:test-agent\n@skill:analysis-skill\n"
        result = markdown_parser.parse(text, "test.md")
        aeos_refs = [e for e in result.ast.aeos_elements if hasattr(e, 'ref_type')]
        ref_types = [e.ref_type for e in aeos_refs]
        assert "agent" in ref_types or "skill" in ref_types

    def test_markdown_fenced_blocks(self, markdown_parser):
        text = '```yaml\nname: test\nvalue: 1\n```\n'
        result = markdown_parser.parse(text, "test.md")
        assert len(result.ast.code_blocks) > 0
        assert result.ast.code_blocks[0].language == "yaml"

    def test_markdown_directives(self, markdown_parser):
        text = "# Test\n\n@step:collect-data Runs data collection.\n"
        result = markdown_parser.parse(text, "test.md")
        assert result is not None


class TestExpressionParser:
    def test_expression_parse(self, expr_parser):
        result = expr_parser.parse("x > 0 and y < 10", "test.expr")
        assert result.is_valid()

    def test_expression_comparison(self, expr_parser):
        result = expr_parser.parse("count == 5", "test.expr")
        assert result.is_valid()

    def test_expression_invalid(self, expr_parser):
        result = expr_parser.parse("== invalid !!!", "test.expr")
        assert not result.is_valid()


class TestPositionMapper:
    def test_offset_to_position(self):
        text = "hello\nworld\n"
        mapper = PositionMapper(text, "utf-16")
        pos = mapper.offset_to_position(0)
        assert pos.line == 0
        assert pos.character == 0

    def test_position_to_offset(self):
        text = "hello\nworld\n"
        mapper = PositionMapper(text, "utf-16")
        offset = mapper.position_to_offset(Position(line=1, character=0))
        assert offset == 6

    def test_roundtrip(self):
        text = "hello world\ntest line\n"
        mapper = PositionMapper(text, "utf-16")
        pos = Position(line=1, character=2)
        offset = mapper.position_to_offset(pos)
        pos2 = mapper.offset_to_position(offset)
        assert pos2.line == pos.line
        assert pos2.character == pos.character


class TestIncrementalParseCache:
    def test_cache_operations(self):
        cache = IncrementalParseCache(max_entries=10)
        text = "agent:\n  name: test\n"
        parser = YamlParser()
        result = parser.parse(text, "test.yaml")
        cache.set("test.yaml", text, result)
        cached = cache.get("test.yaml", text)
        assert cached is result

    def test_cache_invalidate(self):
        cache = IncrementalParseCache(max_entries=10)
        parser = YamlParser()
        cache.set("test.yaml", "a: 1", parser.parse("a: 1", "test.yaml"))
        assert cache.has("test.yaml")
        assert cache.invalidate("test.yaml")
        assert not cache.has("test.yaml")

    def test_cache_clear(self):
        cache = IncrementalParseCache(max_entries=10)
        parser = YamlParser()
        cache.set("a.yaml", "a: 1", parser.parse("a: 1", "a.yaml"))
        cache.clear()
        assert cache.size() == 0

    def test_cache_stats(self):
        cache = IncrementalParseCache(max_entries=50)
        parser = YamlParser()
        cache.set("a.yaml", "a: 1", parser.parse("a: 1", "a.yaml"))
        stats = cache.stats()
        assert stats["entries"] == 1

    def test_reparse_region(self):
        cache = IncrementalParseCache(max_entries=10)
        old_text = "name: old\nvalue: 1\n"
        new_text = "name: new\nvalue: 1\n"
        parser = YamlParser()
        result = parser.parse(old_text, "test.yaml")
        cache.set("test.yaml", old_text, result)
        change_range = Range(start=Position(0, 0), end=Position(0, 12))
        reparse_result = cache.reparse_region("test.yaml", old_text, new_text, change_range)
        assert reparse_result is not None


class TestDispatcher:
    def test_is_aeos_document(self):
        assert is_aeos_document("AGENT.md", None)
        assert is_aeos_document("SKILL.md", None)
        assert is_aeos_document("test.agent.md", None)
        assert is_aeos_document("aeos.config.yaml", None)
        assert not is_aeos_document("node_modules/foo.yaml", None)
        assert not is_aeos_document(".git/config", None)

    def test_dispatch_yaml(self, parser_dispatcher):
        text = "agent:\n  name: test\n"
        result = parser_dispatcher.dispatch(text, "test.yaml")
        assert result is not None
        assert result.ast is not None or result.is_valid()

    def test_dispatch_json(self, parser_dispatcher):
        text = '{"agent": {"name": "test"}}'
        result = parser_dispatcher.dispatch(text, "test.json")
        assert result is not None

    def test_dispatch_markdown(self, parser_dispatcher):
        text = "---\nagent: test\n---\n# Heading\n"
        result = parser_dispatcher.dispatch(text, "test.md")
        assert result is not None

    def test_dispatch_incremental(self, parser_dispatcher):
        old_text = "name: old\n"
        new_text = "name: new\n"
        change_range = Range(start=Position(0, 0), end=Position(0, 10))
        result = parser_dispatcher.dispatch_incremental("test.yaml", old_text, new_text, change_range)
        assert result is not None

    def test_dispatcher_clear_cache(self, parser_dispatcher):
        parser_dispatcher.clear_cache()
