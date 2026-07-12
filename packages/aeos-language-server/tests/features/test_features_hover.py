from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    HoverParams,
    MarkupKind,
    Position,
    Range,
    TextDocumentIdentifier,
)

from aeos_lsp.features.hover import HoverFeature
from aeos_lsp.semantic.models import Agent, Skill, DeprecationStatus, Visibility
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return HoverFeature(server, semantic_model)


def _add_agent_symbol(model, uri="file:///test.yaml"):
    agent = Agent(
        stable_id="agent:test-agent",
        name="test-agent",
        source_uri=uri,
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            documentation="A test agent for hover",
        visibility=Visibility.PUBLIC,
    )
    model.symbol_table.add(agent)
    return agent


def _add_skill_symbol(model, uri="file:///skill.yaml"):
    skill = Skill(
        stable_id="skill:test-skill",
        name="test-skill",
        source_uri=uri,
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=3, character=0)),
            documentation="A test skill",
        tools=["file-reader", "data-analyzer"],
        inputs=["query"],
        outputs=["result"],
    )
    model.symbol_table.add(skill)
    return skill


class TestFeaturesHover:
    def test_hover_basic(self, semantic_model, feature):
        _add_agent_symbol(semantic_model)
        params = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_hover(params)
        assert result is not None
        assert result.contents.kind == MarkupKind.Markdown
        assert "test-agent" in result.contents.value

    def test_hover_markdown_format(self, semantic_model, feature):
        _add_agent_symbol(semantic_model)
        params = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///test.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_hover(params)
        assert result is not None
        assert "**" in result.contents.value
        assert "`test-agent`" in result.contents.value
        assert "A test agent" in result.contents.value

    def test_hover_on_different_symbols(self, semantic_model, feature):
        _add_agent_symbol(semantic_model, "file:///agent.yaml")
        _add_skill_symbol(semantic_model, "file:///skill.yaml")
        params_agent = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///agent.yaml"),
            position=Position(line=0, character=0),
        )
        result_agent = feature.provide_hover(params_agent)
        assert result_agent is not None
        assert "Agent" in result_agent.contents.value or "agent" in result_agent.contents.value

        params_skill = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///skill.yaml"),
            position=Position(line=0, character=0),
        )
        result_skill = feature.provide_hover(params_skill)
        assert result_skill is not None
        assert "Skill" in result_skill.contents.value or "skill" in result_skill.contents.value

    def test_hover_none_for_missing(self, semantic_model, feature):
        params = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_hover(params)
        assert result is None

    def test_hover_deprecated_shows_warning(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:old-agent",
            name="old-agent",
            source_uri="file:///deprecated.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            deprecation=DeprecationStatus.DEPRECATED,
        )
        semantic_model.symbol_table.add(agent)
        params = HoverParams(
            text_document=TextDocumentIdentifier(uri="file:///deprecated.yaml"),
            position=Position(line=0, character=0),
        )
        result = feature.provide_hover(params)
        assert result is not None
        assert "deprecated" in result.contents.value.lower()
