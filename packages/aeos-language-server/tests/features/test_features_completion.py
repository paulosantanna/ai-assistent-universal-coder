from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

import pytest
from lsprotocol.types import (
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    Position,
    TextDocumentIdentifier,
)

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.features.completion import CompletionFeature
from aeos_lsp.semantic.models import Agent, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def mock_server():
    server = MagicMock()
    ws = MagicMock()
    doc = MagicMock()
    doc.source = "agent:\n  name: test\n  skills:\n    - \n"
    ws.text_documents = {"file:///test.yaml": doc}
    server.workspace = ws
    type(server.workspace).get_config = MagicMock(return_value=LSPClientConfig())
    return server


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(mock_server, semantic_model):
    return CompletionFeature(mock_server, semantic_model)


class TestFeaturesCompletion:
    def test_completion_basic(self, feature, mock_server):
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_completions(params)
        assert isinstance(result, CompletionList)
        assert len(result.items) > 0

    def test_completion_resolve(self, feature):
        item = MagicMock()
        item.label = "test-skill"
        resolved = feature._completion_resolve_feature if hasattr(feature, "_completion_resolve_feature") else None
        if resolved:
            result = resolved.resolve_completion(item)
            assert result is not None

    def test_completion_context_aware(self, feature, mock_server):
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=1),
        )
        result = feature.provide_completions(params)
        labels = [item.label for item in result.items]
        assert any("agent" in l for l in labels)

    def test_completion_prefix_filtering(self, feature, mock_server):
        doc = mock_server.workspace.text_documents["file:///test.yaml"]
        doc.source = "skill:\n  name: s\n"
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=2),
        )
        result = feature.provide_completions(params)
        labels = [item.label for item in result.items]
        assert any(l.startswith("s") for l in labels)

    def test_completion_pagination(self, feature, mock_server):
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_completions(params)
        assert isinstance(result.is_incomplete, bool)

    def test_completion_directive(self, feature, mock_server):
        doc = mock_server.workspace.text_documents["file:///test.yaml"]
        doc.source = "@"
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=1),
        )
        result = feature.provide_completions(params)
        labels = [item.label for item in result.items]
        assert any(l.startswith("@") for l in labels)

    def test_completion_expression(self, feature, mock_server):
        doc = mock_server.workspace.text_documents["file:///test.yaml"]
        doc.source = "{{\n"
        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=2),
        )
        result = feature.provide_completions(params)
        assert isinstance(result, CompletionList)
