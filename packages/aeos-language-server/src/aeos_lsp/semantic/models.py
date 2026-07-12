from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lsprotocol.types import Position, Range


class SymbolKind(Enum):
    WORKSPACE = "workspace"
    REPOSITORY = "repository"
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"
    PLAYBOOK_STEP = "playbook_step"
    TOOL = "tool"
    COMMAND = "command"
    POLICY = "policy"
    PERMISSION = "permission"
    REGISTRY = "registry"
    MODEL_PROFILE = "model_profile"
    TOKEN_BUDGET = "token_budget"
    QUALITY_GATE = "quality_gate"
    JUDGE_RULE = "judge_rule"
    EVIDENCE_REQUIREMENT = "evidence_requirement"
    ARTIFACT = "artifact"
    VARIABLE = "variable"
    INPUT = "input"
    OUTPUT = "output"
    DEPENDENCY = "dependency"
    EXECUTION_TARGET = "execution_target"
    APPROVAL_REQUIREMENT = "approval_requirement"
    ROLLBACK_DEFINITION = "rollback_definition"
    LAYER = "layer"
    UNKNOWN = "unknown"


class Visibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    RESTRICTED = "restricted"


class DeprecationStatus(Enum):
    CURRENT = "current"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
    EXPERIMENTAL = "experimental"
    SUPERSEDED = "superseded"


@dataclass(frozen=True)
class Workspace:
    stable_id: str
    name: str
    folders: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)
    index_ref: str | None = None
    kind: SymbolKind = SymbolKind.WORKSPACE

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Repository:
    stable_id: str
    uri: str
    name: str
    root_config: dict[str, Any] = field(default_factory=dict)
    kind: SymbolKind = SymbolKind.REPOSITORY

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class AgentLayer:
    stable_id: str
    name: str
    skills: list[str] = field(default_factory=list)
    description: str = ""
    kind: SymbolKind = SymbolKind.LAYER

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Agent:
    stable_id: str
    name: str
    source_uri: str
    selection_range: Range
    full_range: Range
    declaration: Range | None = None
    documentation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    visibility: Visibility = Visibility.PUBLIC
    deprecation: DeprecationStatus = DeprecationStatus.CURRENT
    references: list[str] = field(default_factory=list)
    content_hash: str = ""
    parent_id: str | None = None
    skills: list[str] = field(default_factory=list)
    layers: list[AgentLayer] = field(default_factory=list)
    description: str = ""
    kind: SymbolKind = SymbolKind.AGENT

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Skill:
    stable_id: str
    name: str
    source_uri: str
    selection_range: Range
    full_range: Range
    declaration: Range | None = None
    documentation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    visibility: Visibility = Visibility.PUBLIC
    deprecation: DeprecationStatus = DeprecationStatus.CURRENT
    references: list[str] = field(default_factory=list)
    content_hash: str = ""
    tools: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    kind: SymbolKind = SymbolKind.SKILL

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Playbook:
    stable_id: str
    name: str
    source_uri: str
    selection_range: Range
    full_range: Range
    declaration: Range | None = None
    documentation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    visibility: Visibility = Visibility.PUBLIC
    deprecation: DeprecationStatus = DeprecationStatus.CURRENT
    references: list[str] = field(default_factory=list)
    content_hash: str = ""
    steps: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    kind: SymbolKind = SymbolKind.PLAYBOOK

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class PlaybookStep:
    stable_id: str
    name: str
    step_type: str = ""
    tool: str | None = None
    skill: str | None = None
    playbook: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    conditions: list[str] = field(default_factory=list)
    timeout: int | None = None
    retry: int | None = None
    approval: bool = False
    rollback: str | None = None
    executor: str | None = None
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.PLAYBOOK_STEP

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Tool:
    stable_id: str
    name: str
    command: str = ""
    inputs: list[dict[str, Any]] = field(default_factory=list)
    outputs: list[dict[str, Any]] = field(default_factory=list)
    mutating: bool = False
    timeout: int | None = None
    description: str = ""
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.TOOL

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Command:
    stable_id: str
    name: str
    args: list[str] = field(default_factory=list)
    mutating: bool = False
    shell: bool = False
    description: str = ""
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.COMMAND

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Policy:
    stable_id: str
    name: str
    rules: dict[str, Any] = field(default_factory=dict)
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.POLICY

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Permission:
    stable_id: str
    name: str
    scopes: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.PERMISSION

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Registry:
    stable_id: str
    name: str
    entries: dict[str, Any] = field(default_factory=dict)
    registry_type: str = ""
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.REGISTRY

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class ModelProfile:
    stable_id: str
    name: str
    provider: str = ""
    context_window: int = 0
    max_tokens: int = 0
    cost: float = 0.0
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.MODEL_PROFILE

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class TokenBudget:
    stable_id: str
    name: str
    max_input_tokens: int = 0
    max_output_tokens: int = 0
    max_total_tokens: int = 0
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.TOKEN_BUDGET

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class QualityGate:
    stable_id: str
    name: str
    rules: list[dict[str, Any]] = field(default_factory=list)
    min_score: float = 0.0
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.QUALITY_GATE

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class JudgeRule:
    stable_id: str
    name: str
    condition: str = ""
    action: str = ""
    min_score: float = 0.0
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.JUDGE_RULE

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class EvidenceRequirement:
    stable_id: str
    name: str
    required_evidence: list[str] = field(default_factory=list)
    hash_required: bool = False
    source_uri: str = ""
    kind: SymbolKind = SymbolKind.EVIDENCE_REQUIREMENT

    @property
    def symbol_kind(self) -> SymbolKind:
        return self.kind


@dataclass(frozen=True)
class Artifact:
    stable_id: str
    name: str
    kind: str = ""
    source_uri: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    symbol_kind: SymbolKind = SymbolKind.ARTIFACT


@dataclass(frozen=True)
class Variable:
    stable_id: str
    name: str
    kind: str = ""
    type_ref: str = ""
    default: Any = None
    source_uri: str = ""
    range: Range | None = None
    symbol_kind: SymbolKind = SymbolKind.VARIABLE


@dataclass(frozen=True)
class Input:
    stable_id: str
    name: str
    type_ref: str = ""
    required: bool = False
    default: Any = None
    source_uri: str = ""
    range: Range | None = None
    symbol_kind: SymbolKind = SymbolKind.INPUT


@dataclass(frozen=True)
class Output:
    stable_id: str
    name: str
    type_ref: str = ""
    description: str = ""
    source_uri: str = ""
    range: Range | None = None
    symbol_kind: SymbolKind = SymbolKind.OUTPUT


@dataclass(frozen=True)
class Dependency:
    stable_id: str
    source_id: str
    target_id: str
    kind: str = ""
    source_uri: str = ""
    symbol_kind: SymbolKind = SymbolKind.DEPENDENCY


@dataclass(frozen=True)
class ExecutionTarget:
    stable_id: str
    name: str
    kind: str = ""
    executor: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    source_uri: str = ""
    symbol_kind: SymbolKind = SymbolKind.EXECUTION_TARGET


@dataclass(frozen=True)
class ApprovalRequirement:
    stable_id: str
    name: str
    required_approvals: int = 1
    scope: str = ""
    source_uri: str = ""
    symbol_kind: SymbolKind = SymbolKind.APPROVAL_REQUIREMENT


@dataclass(frozen=True)
class RollbackDefinition:
    stable_id: str
    name: str
    steps: list[str] = field(default_factory=list)
    strategy: str = ""
    source_uri: str = ""
    symbol_kind: SymbolKind = SymbolKind.ROLLBACK_DEFINITION
