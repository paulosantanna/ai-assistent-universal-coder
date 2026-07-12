from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

import pytest
from lsprotocol.types import (
    CodeAction,
    CodeActionContext,
    CodeActionKind,
    CodeActionParams,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
    TextDocumentIdentifier,
)

from aeos_lsp.features.code_actions import CodeActionsFeature
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def mock_server():
    server = MagicMock()
    ws = MagicMock()
    doc = MagicMock()
    doc.source = "agent:\n  name: test\n  skills:\n    - unresolved-skill\n"
    ws.text_documents = {"file:///test.yaml": doc}
    server.workspace = ws
    return server


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(mock_server, semantic_model):
    return CodeActionsFeature(mock_server, semantic_model)


class TestFeaturesCodeActions:
    def test_code_action_add_timeout(self, mock_server, semantic_model, feature):
        diagnostic = Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=5)),
            message="Missing timeout configuration",
            severity=DiagnosticSeverity.Warning,
            code="missing_timeout",
            source="aeos",
        )
        params = CodeActionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            context=CodeActionContext(diagnostics=[diagnostic]),
        )
        result = feature.provide_code_actions(params)
        assert result is not None
        titles = [a.title if isinstance(a, CodeAction) else a.title for a in result]
        assert any("timeout" in t.lower() for t in titles)

    def test_code_action_fix_reference(self, mock_server, semantic_model, feature):
        diagnostic = Diagnostic(
            range=Range(start=Position(line=2, character=4), end=Position(line=2, character=20)),
            message="Unresolved reference: unresolved-skill",
            severity=DiagnosticSeverity.Error,
            code="unresolved_reference",
            source="aeos",
        )
        params = CodeActionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            context=CodeActionContext(diagnostics=[diagnostic]),
        )
        result = feature.provide_code_actions(params)
        assert result is not None
        titles = [a.title if isinstance(a, CodeAction) else a.title for a in result]
        assert any("reference" in t.lower() for t in titles)

    def test_code_action_deterministic(self, mock_server, semantic_model, feature):
        diagnostic = Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=5)),
            message="Test diagnostic",
            severity=DiagnosticSeverity.Warning,
            code="test_diag",
            source="aeos",
        )
        params = CodeActionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            context=CodeActionContext(diagnostics=[diagnostic]),
        )
        result1 = feature.provide_code_actions(params)
        result2 = feature.provide_code_actions(params)
        if result1 is not None and result2 is not None:
            titles1 = [a.title for a in result1]
            titles2 = [a.title for a in result2]
            assert titles1 == titles2

    def test_code_action_suppress(self, mock_server, semantic_model, feature):
        diagnostic = Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=5)),
            message="Some warning",
            severity=DiagnosticSeverity.Warning,
            code="some_warning",
            source="aeos",
        )
        params = CodeActionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            context=CodeActionContext(diagnostics=[diagnostic]),
        )
        result = feature.provide_code_actions(params)
        if result:
            titles = [a.title for a in result]
            assert any("suppress" in t.lower() for t in titles)

    def test_code_action_generic(self, mock_server, semantic_model, feature):
        params = CodeActionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            context=CodeActionContext(diagnostics=[]),
        )
        result = feature.provide_code_actions(params)
        assert result is not None
        titles = [a.title for a in result]
        assert any("stub" in t.lower() for t in titles)
