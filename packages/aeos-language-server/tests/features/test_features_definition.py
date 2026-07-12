from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    DefinitionParams,
    Location,
    Position,
    Range,
    TextDocumentIdentifier,
)

from aeos_lsp.features.definition import DefinitionFeature
from aeos_lsp.semantic.models import Agent, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return DefinitionFeature(server, semantic_model)


class TestFeaturesDefinition:
    def test_definition_basic(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:test-agent",
            name="test-agent",
            source_uri="file:///agent.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=5, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=5, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        params = DefinitionParams(
            text_document=TextDocumentIdentifier(uri="file:///agent.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_definition(params)
        assert result is not None
        if isinstance(result, list):
            assert len(result) >= 1
            loc = result[0]
        else:
            loc = result
        assert loc.uri == "file:///agent.yaml"

    def test_definition_multiple(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:parent-agent",
            name="parent-agent",
            source_uri="file:///parent.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            skills=["skill:child-skill"],
        )
        skill = Skill(
            stable_id="skill:child-skill",
            name="child-skill",
            source_uri="file:///skill.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        semantic_model.symbol_table.add(skill)

        params = DefinitionParams(
            text_document=TextDocumentIdentifier(uri="file:///parent.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_definition(params)
        assert result is not None
        if isinstance(result, list):
            assert len(result) >= 1

    def test_definition_none_for_missing(self, semantic_model, feature):
        params = DefinitionParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_definition(params)
        assert result is None
