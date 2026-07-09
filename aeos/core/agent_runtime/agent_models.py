from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

AgentStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


@dataclass
class AgentContract:
    id: str
    role: str
    responsibilities: list[str]
    allowed_actions: list[str]
    forbidden_actions: list[str]
    capabilities: list[str]
    delegation_policy: dict[str, Any]
    output_schema: dict[str, Any]
    stop_conditions: list[str]
    path: str = ""

    def is_valid(self) -> bool:
        return all([
            bool(self.id),
            bool(self.role),
            len(self.responsibilities) > 0,
            len(self.allowed_actions) > 0,
            isinstance(self.capabilities, list),
            isinstance(self.delegation_policy, dict),
        ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "responsibilities": self.responsibilities,
            "allowed_actions": self.allowed_actions,
            "forbidden_actions": self.forbidden_actions,
            "capabilities": self.capabilities,
            "delegation_policy": self.delegation_policy,
            "output_schema": self.output_schema,
            "stop_conditions": self.stop_conditions,
            "path": self.path,
        }


@dataclass
class AgentTask:
    execution_id: str
    task_id: str
    agent_id: str
    actor: str
    role: str
    objective: str
    scope: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    context_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    approval_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    status: str = "PENDING"

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "actor": self.actor,
            "role": self.role,
            "objective": self.objective,
            "scope": self.scope,
            "constraints": self.constraints,
            "context_refs": self.context_refs,
            "evidence_refs": self.evidence_refs,
            "approval_id": self.approval_id,
            "parent_task_id": self.parent_task_id,
            "status": self.status,
        }


@dataclass
class AgentResult:
    execution_id: str
    task_id: str
    agent_id: str
    status: AgentStatus
    messages: list[dict[str, Any]] = field(default_factory=list)
    delegations: list[dict[str, Any]] = field(default_factory=list)
    skill_results: list[dict[str, Any]] = field(default_factory=list)
    playbook_results: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    facts: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "status": self.status,
            "messages": self.messages,
            "delegations": self.delegations,
            "skill_results": self.skill_results,
            "playbook_results": self.playbook_results,
            "tool_results": self.tool_results,
            "facts": self.facts,
            "assumptions": self.assumptions,
            "risks": self.risks,
            "recommendations": self.recommendations,
            "evidence_refs": self.evidence_refs,
            "blocking_conditions": self.blocking_conditions,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


@dataclass(frozen=True)
class AgentMessage:
    execution_id: str
    task_id: str
    from_agent: str
    message_type: str
    payload: dict[str, Any]
    to_agent: Optional[str] = None
    parent_message_id: Optional[str] = None
    context_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    risk_level: str = "low"
    requires_ack: bool = True
    message_id: str = field(default_factory=lambda: f"msg-{uuid4().hex[:12]}")
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "from_agent": self.from_agent,
            "message_type": self.message_type,
            "payload": self.payload,
            "to_agent": self.to_agent,
            "parent_message_id": self.parent_message_id,
            "context_refs": self.context_refs,
            "evidence_refs": self.evidence_refs,
            "risk_level": self.risk_level,
            "requires_ack": self.requires_ack,
            "message_id": self.message_id,
            "created_at": self.created_at,
        }


def generate_task_id() -> str:
    return f"task-{uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
