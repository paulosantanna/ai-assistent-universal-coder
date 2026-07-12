from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    DocumentSymbol,
    DocumentSymbolParams,
    Position,
    Range,
    SymbolKind as LspSymbolKind,
    SymbolTag,
    TextDocumentIdentifier,
)

from aeos_lsp.features.document_symbols import DocumentSymbolsFeature
from aeos_lsp.semantic.models import Agent, Skill, Playbook, PlaybookStep
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return DocumentSymbolsFeature(server, semantic_model)


class TestFeaturesDocumentSymbols:
    def test_document_symbols_agent(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:sym-agent",
            name="sym-agent",
            source_uri="file:///agent.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=0, character=9)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=4, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///agent.yaml"),
        )
        result = feature.provide_symbols(params)
        assert result is not None
        assert len(result) >= 1
        assert result[0].name == "sym-agent"
        assert result[0].kind == LspSymbolKind.Class

    def test_document_symbols_hierarchical(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:hier-agent",
            name="hier-agent",
            source_uri="file:///hier.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=0, character=10)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=5, character=0)),
        )
        skill = Skill(
            stable_id="skill:hier-skill",
            name="hier-skill",
            source_uri="file:///hier.yaml",
            selection_range=Range(start=Position(line=2, character=0), end=Position(line=2, character=10)),
            full_range=Range(start=Position(line=2, character=0), end=Position(line=4, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        semantic_model.symbol_table.add(skill)
        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///hier.yaml"),
        )
        result = feature.provide_symbols(params)
        assert result is not None
        assert len(result) >= 2

    def test_document_symbols_none_for_missing(self, semantic_model, feature):
        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
        )
        result = feature.provide_symbols(params)
        assert result is None

    def test_document_symbols_detail(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:detail-agent",
            name="detail-agent",
            source_uri="file:///detail.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=0, character=12)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            parent_id="agent:base",
            skills=["skill:s1"],
        )
        semantic_model.symbol_table.add(agent)
        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///detail.yaml"),
        )
        result = feature.provide_symbols(params)
        assert result is not None
        assert "agent:" in (result[0].detail or "")
