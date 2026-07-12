from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    DocumentFormattingParams,
    DocumentRangeFormattingParams,
    FormattingOptions,
    Position,
    Range,
    TextDocumentIdentifier,
)

from aeos_lsp.features.formatting import FormattingFeature
from aeos_lsp.features.range_formatting import RangeFormattingFeature


@pytest.fixture
def server():
    s = MagicMock()
    ws = MagicMock()
    ws.text_documents = {}
    s.workspace = ws
    return s


@pytest.fixture
def formatting_feature(server):
    return FormattingFeature(server)


@pytest.fixture
def range_formatting_feature(server):
    return RangeFormattingFeature(server)


def _add_document(server, uri, content):
    doc = MagicMock()
    doc.source = content
    server.workspace.text_documents[uri] = doc


class TestFeaturesFormatting:
    def test_format_document(self, server, formatting_feature):
        uri = "file:///format.yaml"
        content = "  agent:\n  name:    formatted\n  description:   test\n"
        _add_document(server, uri, content)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = formatting_feature.provide_formatting(params)
        assert result is not None
        assert len(result) == 1
        edit = result[0]
        new_text = edit.new_text
        assert "name: formatted" in new_text
        assert "description: test" in new_text

    def test_format_range(self, server, range_formatting_feature):
        uri = "file:///range-format.yaml"
        content = "  key1: val1\n  key2:     val2\n  key3: val3\n"
        _add_document(server, uri, content)
        params = DocumentRangeFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            range=Range(
                start=Position(line=1, character=0),
                end=Position(line=2, character=0),
            ),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = range_formatting_feature.provide_range_formatting(params)
        assert result is not None
        assert len(result) == 1

    def test_format_identical(self, server, formatting_feature):
        uri = "file:///identical.yaml"
        content = "name: test\n"
        _add_document(server, uri, content)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = formatting_feature.provide_formatting(params)
        assert result is None

    def test_format_missing_document(self, server, formatting_feature):
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = formatting_feature.provide_formatting(params)
        assert result is None

    def test_format_comments_and_strings(self, server, formatting_feature):
        uri = "file:///comments.yaml"
        content = "#acomment\n\tkey:val\n"
        _add_document(server, uri, content)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = formatting_feature.provide_formatting(params)
        assert result is not None

    def test_format_preserves_front_matter(self, server, range_formatting_feature):
        uri = "file:///front-matter.yaml"
        content = "---\ntitle: test\n---\n\nname:abc\n"
        _add_document(server, uri, content)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = range_formatting_feature.provide_range_formatting(
            DocumentRangeFormattingParams(
                text_document=TextDocumentIdentifier(uri=uri),
                range=Range(
                    start=Position(0, 0),
                    end=Position(4, 0),
                ),
                options=FormattingOptions(tab_size=2, insert_spaces=True),
            )
        )
        assert result is not None

    def test_range_formatting_none_for_invalid(self, server, range_formatting_feature):
        params = DocumentRangeFormattingParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
            range=Range(
                start=Position(0, 0),
                end=Position(1, 0),
            ),
            options=FormattingOptions(tab_size=2, insert_spaces=True),
        )
        result = range_formatting_feature.provide_range_formatting(params)
        assert result is None
