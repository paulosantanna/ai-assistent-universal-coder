from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    CodeLens,
    CodeLensParams,
    Command,
    Position,
    Range,
    TextDocumentIdentifier,
)

from aeos_lsp.features.code_lens import CodeLensFeature
from aeos_lsp.semantic.models import Agent, Skill, Playbook, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return CodeLensFeature(server, semantic_model)


class TestFeaturesCodeLens:
    def test_code_lens_on_agent(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:lens-agent",
            name="lens-agent",
            source_uri="file:///agent.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        params = CodeLensParams(
            text_document=TextDocumentIdentifier(uri="file:///agent.yaml"),
        )
        result = feature.provide_code_lenses(params)
        assert result is not None
        commands = [lens.command.command for lens in result if lens.command]
        assert "aeos.validateDocument" in commands
        assert "aeos.showReferences" in commands

    def test_code_lens_on_skill(self, semantic_model, feature):
        skill = Skill(
            stable_id="skill:lens-skill",
            name="lens-skill",
            source_uri="file:///skill.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        )
        semantic_model.symbol_table.add(skill)
        params = CodeLensParams(
            text_document=TextDocumentIdentifier(uri="file:///skill.yaml"),
        )
        result = feature.provide_code_lenses(params)
        assert result is not None
        commands = [lens.command.command for lens in result if lens.command]
        assert "aeos.validateDocument" in commands
        assert "aeos.dryRunSkill" in commands

    def test_code_lens_on_playbook(self, semantic_model, feature):
        pb = Playbook(
            stable_id="playbook:lens-pb",
            name="lens-pb",
            source_uri="file:///playbook.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        )
        semantic_model.symbol_table.add(pb)
        params = CodeLensParams(
            text_document=TextDocumentIdentifier(uri="file:///playbook.yaml"),
        )
        result = feature.provide_code_lenses(params)
        assert result is not None
        commands = [lens.command.command for lens in result if lens.command]
        assert "aeos.dryRunPlaybook" in commands

    def test_code_lens_not_on_non_aeos(self, semantic_model, feature):
        params = CodeLensParams(
            text_document=TextDocumentIdentifier(uri="file:///readme.txt"),
        )
        result = feature.provide_code_lenses(params)
        assert result is None

    def test_code_lens_validate_workspace(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:ws-agent",
            name="ws-agent",
            source_uri="file:///ws.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=1, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=1, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        params = CodeLensParams(
            text_document=TextDocumentIdentifier(uri="file:///ws.yaml"),
        )
        result = feature.provide_code_lenses(params)
        commands = [lens.command.command for lens in result if lens.command]
        assert "aeos.validateWorkspace" in commands
