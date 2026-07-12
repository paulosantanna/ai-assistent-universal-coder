from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock

import pytest
from lsprotocol.types import Position, Range

from aeos_lsp.parsing.dispatcher import ParserDispatcher, detect_aeos_type, is_aeos_document, AEOSDocumentType
from aeos_lsp.parsing.yaml_parser import YamlParser, YamlDocument, AeoSDocumentType, YamlAstNode
from aeos_lsp.parsing.json_parser import JsonParser, JsonAstNode
from aeos_lsp.parsing.toml_parser import TomlParser, TomlAstNode, TomlDocument
from aeos_lsp.parsing.markdown_parser import (
    MarkdownParser,
    MarkdownDocument,
    FrontMatter,
    Heading,
    Directive,
    FencedCodeBlock,
    AeoSElement,
)
from aeos_lsp.parsing.expression_parser import ExprParser, ExprAstNode
from aeos_lsp.parsing.position_mapper import PositionMapper
from aeos_lsp.parsing.base import ParseResult, ParseError, ParseErrorSeverity
from aeos_lsp.semantic.symbols import SymbolTable, SymbolVisitor
from aeos_lsp.semantic.references import ReferenceTable, Reference, ReferenceKind, ReferenceRole
from aeos_lsp.semantic.resolver import CrossReferenceResolver, ResolutionResult
from aeos_lsp.semantic.dependency_graph import DependencyGraph, DependencyNode
from aeos_lsp.semantic.inheritance_graph import InheritanceGraph
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.models import (
    Agent, AgentLayer, Skill, Playbook, PlaybookStep, Tool, Command,
    Policy, Permission, Registry, ModelProfile, TokenBudget, QualityGate,
    JudgeRule, EvidenceRequirement, Artifact, Variable, Input, Output,
    Dependency, ExecutionTarget, ApprovalRequirement, RollbackDefinition,
    SymbolKind, Visibility, DeprecationStatus, Workspace, Repository,
)


SAMPLE_AGENT_YAML = """\
agent:
  name: test-agent
  description: A test agent
  skills:
    - test-skill
  parent: base-agent
  layers:
    - name: reasoning
      skills:
        - analysis-skill
  visibility: public
"""

SAMPLE_SKILL_YAML = """\
skill:
  name: test-skill
  description: A test skill
  tools:
    - file-reader
    - data-analyzer
  inputs:
    - query
  outputs:
    - result
  visibility: public
"""

SAMPLE_PLAYBOOK_YAML = """\
playbook:
  name: test-playbook
  description: A test playbook
  steps:
    - name: gather-data
      tool: data-collector
      inputs:
        source: "api"
      outputs:
        raw: data
    - name: analyze
      skill: analysis-skill
      inputs:
        data: "{{steps.gather-data.outputs.raw}}"
  variables:
    - threshold
  visibility: public
"""

SAMPLE_MARKDOWN_AGENT = """\
---
agent: test-agent
description: An agent defined in markdown
---

# Test Agent

This is a test agent with @agent:test-agent reference.

## Skills

The agent uses skill:analysis-skill for processing.

```yaml
name: embedded-config
value: test
```
"""

SAMPLE_MARKDOWN_PLAYBOOK = """\
---
playbook: test-playbook
---

# Test Playbook

@step:collect-data Runs data collection.

This playbook executes tool:data-collector and skill:analysis-skill.
"""


@pytest.fixture
def sample_agent_yaml() -> str:
    return SAMPLE_AGENT_YAML


@pytest.fixture
def sample_skill_yaml() -> str:
    return SAMPLE_SKILL_YAML


@pytest.fixture
def sample_playbook_yaml() -> str:
    return SAMPLE_PLAYBOOK_YAML


@pytest.fixture
def sample_markdown_agent() -> str:
    return SAMPLE_MARKDOWN_AGENT


@pytest.fixture
def sample_markdown_playbook() -> str:
    return SAMPLE_MARKDOWN_PLAYBOOK


@pytest.fixture
def temp_dir() -> Path:
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def parser_dispatcher() -> ParserDispatcher:
    return ParserDispatcher()


@pytest.fixture
def aeos_document_paths() -> list[str]:
    return [
        "AGENT.md",
        "AGENTS.md",
        "SKILL.md",
        "PLAYBOOK.md",
        "my.agent.md",
        "my.skill.md",
        "my.playbook.md",
        "config.aeos.yaml",
        "config.aeos.yml",
        "config.aeos.json",
        "config.aeos.jsonc",
        "config.aeos.toml",
        "aeos.config.yaml",
        "permissions.yaml",
        "policies.yaml",
        "agents.registry.yaml",
        "overlay.index",
        "overlay.registry.index.yaml",
    ]


@pytest.fixture
def mock_workspace_manager() -> WorkspaceManager:
    ws = WorkspaceManager()
    ws.add_folder(WorkspaceFolderInfo(uri="file:///workspace", name="workspace"))
    return ws


@pytest.fixture
def mock_semantic_model() -> SemanticModel:
    return SemanticModel()


@pytest.fixture
def yaml_parser() -> YamlParser:
    return YamlParser()


@pytest.fixture
def json_parser() -> JsonParser:
    return JsonParser()


@pytest.fixture
def toml_parser() -> TomlParser:
    return TomlParser()


@pytest.fixture
def markdown_parser() -> MarkdownParser:
    return MarkdownParser()


@pytest.fixture
def expr_parser() -> ExprParser:
    return ExprParser()


@pytest.fixture
def symbol_table() -> SymbolTable:
    return SymbolTable()


@pytest.fixture
def reference_table() -> ReferenceTable:
    return ReferenceTable()


@pytest.fixture
def dependency_graph() -> DependencyGraph:
    return DependencyGraph()


@pytest.fixture
def inheritance_graph() -> InheritanceGraph:
    return InheritanceGraph()


@pytest.fixture
def sample_agent_symbol() -> Agent:
    return Agent(
        stable_id="agent:test-agent",
        name="test-agent",
        source_uri="file:///workspace/agent.yaml",
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=10, character=0)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=10, character=0)),
        parent_id="base-agent",
        skills=["test-skill"],
        layers=[
            AgentLayer(
                stable_id="agent:test-agent/layer:reasoning",
                name="reasoning",
                skills=["analysis-skill"],
            ),
        ],
    )


@pytest.fixture
def sample_skill_symbol() -> Skill:
    return Skill(
        stable_id="skill:test-skill",
        name="test-skill",
        source_uri="file:///workspace/skill.yaml",
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=8, character=0)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=8, character=0)),
        tools=["file-reader", "data-analyzer"],
        inputs=["query"],
        outputs=["result"],
    )


@pytest.fixture
def sample_playbook_symbol() -> Playbook:
    return Playbook(
        stable_id="playbook:test-playbook",
        name="test-playbook",
        source_uri="file:///workspace/playbook.yaml",
        selection_range=Range(start=Position(line=0, character=0), end=Position(line=15, character=0)),
        full_range=Range(start=Position(line=0, character=0), end=Position(line=15, character=0)),
        steps=["step:gather-data", "step:analyze"],
        variables=["threshold"],
    )


@pytest.fixture
def resolver(symbol_table: SymbolTable) -> CrossReferenceResolver:
    return CrossReferenceResolver(symbol_table)
