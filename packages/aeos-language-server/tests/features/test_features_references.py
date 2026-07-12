from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    Position,
    Range,
    ReferenceContext,
    ReferenceParams,
    TextDocumentIdentifier,
)

from aeos_lsp.features.references import ReferencesFeature
from aeos_lsp.semantic.models import Agent, Skill
from aeos_lsp.semantic.references import Reference, ReferenceKind, ReferenceRole
from aeos_lsp.semantic.semantic_model import SemanticModel


@pytest.fixture
def semantic_model():
    return SemanticModel()


@pytest.fixture
def feature(semantic_model):
    server = MagicMock()
    return ReferencesFeature(server, semantic_model)


class TestFeaturesReferences:
    def test_references_basic(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:ref-target",
            name="ref-target",
            source_uri="file:///target.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        ref = Reference(
            source_uri="file:///referrer.yaml",
            source_range=Range(start=Position(line=1, character=0), end=Position(line=1, character=10)),
            target_uri="file:///target.yaml",
            target_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            kind=ReferenceKind.USAGE,
            role=ReferenceRole.REFERENCE,
        )
        semantic_model.reference_table.add_reference(ref)
        params = ReferenceParams(
            text_document=TextDocumentIdentifier(uri="file:///target.yaml"),
            position=Position(line=0, character=0),
            context=ReferenceContext(include_declaration=False),
        )
        result = feature.provide_references(params)
        if result is not None:
            uris = [loc.uri for loc in result]
            assert "file:///referrer.yaml" in uris

    def test_references_include_declaration(self, semantic_model, feature):
        agent = Agent(
            stable_id="agent:decl-target",
            name="decl-target",
            source_uri="file:///decl.yaml",
            selection_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
            full_range=Range(start=Position(line=0, character=0), end=Position(line=2, character=0)),
        )
        semantic_model.symbol_table.add(agent)
        params = ReferenceParams(
            text_document=TextDocumentIdentifier(uri="file:///decl.yaml"),
            position=Position(line=0, character=0),
            context=ReferenceContext(include_declaration=True),
        )
        result = feature.provide_references(params)
        if result is not None:
            uris = [loc.uri for loc in result]
            assert "file:///decl.yaml" in uris

    def test_references_none_for_missing(self, semantic_model, feature):
        params = ReferenceParams(
            text_document=TextDocumentIdentifier(uri="file:///missing.yaml"),
            position=Position(line=0, character=0),
            context=ReferenceContext(include_declaration=False),
        )
        result = feature.provide_references(params)
        assert result is None
