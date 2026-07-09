from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

SkillStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


@dataclass
class SkillContract:
    id: str
    mission: str
    allowed_actions: list[str]
    forbidden_actions: list[str]
    required_inputs: list[str]
    output_schema: dict[str, Any]
    quality_gates: list[str]
    stop_conditions: list[str]
    owner_agent: str = ""
    capabilities: list[str] = field(default_factory=list)
    risk_level: str = "low"
    path: str = ""

    def is_valid(self) -> bool:
        return all([
            bool(self.id),
            bool(self.mission),
            len(self.allowed_actions) > 0,
            isinstance(self.required_inputs, list),
            isinstance(self.output_schema, dict),
            len(self.quality_gates) > 0,
            len(self.stop_conditions) > 0,
        ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "mission": self.mission,
            "allowed_actions": self.allowed_actions,
            "forbidden_actions": self.forbidden_actions,
            "required_inputs": self.required_inputs,
            "output_schema": self.output_schema,
            "quality_gates": self.quality_gates,
            "stop_conditions": self.stop_conditions,
            "owner_agent": self.owner_agent,
            "capabilities": self.capabilities,
            "risk_level": self.risk_level,
            "path": self.path,
        }


@dataclass
class SkillRequest:
    execution_id: str
    skill_id: str
    actor: str
    role: str
    input: dict[str, Any] = field(default_factory=dict)
    context_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    approval_id: Optional[str] = None
    request_id: str = field(default_factory=lambda: f"sr-{uuid4().hex[:12]}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "skill_id": self.skill_id,
            "actor": self.actor,
            "role": self.role,
            "input": self.input,
            "context_refs": self.context_refs,
            "evidence_refs": self.evidence_refs,
            "approval_id": self.approval_id,
            "request_id": self.request_id,
        }


@dataclass
class SkillResult:
    execution_id: str
    skill_id: str
    status: SkillStatus
    facts: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "facts": self.facts,
            "assumptions": self.assumptions,
            "risks": self.risks,
            "recommendations": self.recommendations,
            "tool_results": self.tool_results,
            "evidence_refs": self.evidence_refs,
            "blocking_conditions": self.blocking_conditions,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
