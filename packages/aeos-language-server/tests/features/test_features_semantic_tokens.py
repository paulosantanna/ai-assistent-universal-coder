from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    Position,
    Range,
    SemanticTokensDeltaParams,
    SemanticTokensParams,
    SemanticTokensRangeParams,
    TextDocumentIdentifier,
)

from aeos_lsp.features.semantic_tokens import SemanticTokensFeature
from aeos_lsp.semantic.models import Agent, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return SemanticTokensFeature(server, semantic_model)


def _add_symbols(semantic_model):
    agent = Agent(
        stable_id="agent:sem-agent",
        name="sem-agent",
        source_uri="file:///test.yaml",
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=0, character=9)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
    )
    skill = Skill(
        stable_id="skill:sem-skill",
        name="sem-skill",
        source_uri="file:///test.yaml",
        selection_range=Range(start=Position(line=3, character=0), end=Position(line=3, character=9)),
        full_range=Range(start=Position(line=3, character=0), end=Position(line=5, character=0)),
    )
    semantic_model.symbol_table.add(agent)
    semantic_model.symbol_table.add(skill)


class TestFeaturesSemanticTokens:
    def test_semantic_tokens_full(self, semantic_model, feature):
        _add_symbols(semantic_model)
        params = SemanticTokensParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
        )
        result = feature.provide_semantic_tokens(params)
        assert result is not None
        assert len(result.data) > 0
        assert len(result.data) % 5 == 0

    def test_semantic_tokens_delta(self, semantic_model, feature):
        _add_symbols(semantic_model)
        params = SemanticTokensDeltaParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            previous_result_id="",
        )
        result = feature.provide_semantic_tokens_delta(params)
        assert result is not None
        if hasattr(result, "edits"):
            assert len(result.edits) > 0

    def test_semantic_tokens_range(self, semantic_model, feature):
        _add_symbols(semantic_model)
        params = SemanticTokensRangeParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=4, character=0),
            ),
        )
        result = feature.provide_semantic_tokens_range(params)
        assert result is not None
        assert len(result.data) > 0

    def test_semantic_tokens_range_empty(self, semantic_model, feature):
        params = SemanticTokensRangeParams(
            text_document=TextDocumentIdentifier(uri="file:///empty.yaml"),
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
        )
        result = feature.provide_semantic_tokens_range(params)
        assert result is None

    def test_semantic_tokens_empty(self, semantic_model, feature):
        params = SemanticTokensParams(
            text_document=TextDocumentIdentifier(uri="file:///empty.yaml"),
        )
        result = feature.provide_semantic_tokens(params)
        assert result is None

    def test_semantic_tokens_legend(self, feature):
        types = feature.token_types
        assert len(types) > 0
        assert "agent" in types
        assert "skill" in types
        assert "playbook" in types
        mods = feature.token_modifiers
        assert "declaration" in mods
        assert "deprecated" in mods
