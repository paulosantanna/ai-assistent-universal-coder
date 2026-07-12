from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExecutionRequest:
    agent_id: str | None = None
    skill_id: str | None = None
    playbook_id: str | None = None
    tool_id: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    timeout: float | None = None
    execution_mode: str = "dry-run"


@dataclass
class ExecutionResult:
    success: bool
    output: Any = None
    error: str | None = None
    elapsed_seconds: float = 0.0
    evidence_id: str | None = None
    token_usage: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PermissionCheck:
    allowed: bool
    reason: str = ""
    scope: str = ""
    capability: str = ""
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    compliant: bool
    policy_name: str = ""
    violations: list[str] = field(default_factory=list)
    remediation: str = ""


@dataclass
class JudgeVerdict:
    passed: bool
    score: float = 0.0
    checks: list[dict[str, Any]] = field(default_factory=list)
    summary: str = ""


@dataclass
class EvidenceRecord:
    evidence_id: str
    artifact_id: str = ""
    execution_id: str = ""
    content_hash: str = ""
    content: str = ""
    timestamp: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillDefinition:
    id: str
    name: str
    tools: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    model: str = ""
    instructions: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PlaybookDefinition:
    id: str
    name: str
    steps: list[dict[str, Any]] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenBudget:
    max_tokens: int = 4096
    used_tokens: int = 0
    remaining_tokens: int = 4096
    warnings: list[str] = field(default_factory=list)


class AeosRuntimePort(ABC):
    @abstractmethod
    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        ...

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        ...


class PermissionPort(ABC):
    @abstractmethod
    async def check_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
        resource: str = "",
    ) -> PermissionCheck:
        ...

    @abstractmethod
    async def grant_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
        ttl_seconds: int | None = None,
    ) -> bool:
        ...

    @abstractmethod
    async def revoke_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
    ) -> bool:
        ...

    @abstractmethod
    async def list_permissions(self, agent_id: str) -> list[PermissionCheck]:
        ...


class PolicyPort(ABC):
    @abstractmethod
    async def evaluate(
        self,
        action: str,
        resource: str,
        context: dict[str, Any],
    ) -> PolicyDecision:
        ...

    @abstractmethod
    async def list_policies(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def get_policy(self, policy_name: str) -> dict[str, Any] | None:
        ...


class JudgePort(ABC):
    @abstractmethod
    async def evaluate(
        self,
        artifact: str,
        rules: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeVerdict:
        ...

    @abstractmethod
    async def get_rules(self) -> list[dict[str, Any]]:
        ...


class EvidencePort(ABC):
    @abstractmethod
    async def store(self, record: EvidenceRecord) -> str:
        ...

    @abstractmethod
    async def retrieve(self, evidence_id: str) -> EvidenceRecord | None:
        ...

    @abstractmethod
    async def find(self, artifact_id: str) -> list[EvidenceRecord]:
        ...

    @abstractmethod
    async def verify(self, evidence_id: str) -> bool:
        ...


class SkillPort(ABC):
    @abstractmethod
    async def resolve(self, skill_ref: str) -> SkillDefinition | None:
        ...

    @abstractmethod
    async def execute(
        self,
        skill: SkillDefinition,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        ...

    @abstractmethod
    async def list_skills(self) -> list[SkillDefinition]:
        ...


class PlaybookPort(ABC):
    @abstractmethod
    async def resolve(self, playbook_ref: str) -> PlaybookDefinition | None:
        ...

    @abstractmethod
    async def execute(
        self,
        playbook: PlaybookDefinition,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        ...

    @abstractmethod
    async def list_playbooks(self) -> list[PlaybookDefinition]:
        ...


class TokenBudgetPort(ABC):
    @abstractmethod
    async def check_budget(self, agent_id: str, estimated_tokens: int) -> TokenBudget:
        ...

    @abstractmethod
    async def consume(self, agent_id: str, tokens: int) -> bool:
        ...

    @abstractmethod
    async def reset(self, agent_id: str) -> None:
        ...

    @abstractmethod
    async def get_budget(self, agent_id: str) -> TokenBudget:
        ...


class SandboxPort(ABC):
    @abstractmethod
    async def create(self, name: str, config: dict[str, Any] | None = None) -> str:
        ...

    @abstractmethod
    async def destroy(self, sandbox_id: str) -> bool:
        ...

    @abstractmethod
    async def execute_in_sandbox(
        self,
        sandbox_id: str,
        command: str,
        timeout: float | None = None,
    ) -> ExecutionResult:
        ...

    @abstractmethod
    async def list_sandboxes(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def sandbox_health(self, sandbox_id: str) -> dict[str, Any]:
        ...
