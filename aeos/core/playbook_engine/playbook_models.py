from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

PlaybookStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


@dataclass
class PlaybookStep:
    id: str
    skill: Optional[str] = None
    description: str = ""
    depends_on: list[str] = field(default_factory=list)
    status: str = "PENDING"
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "skill": self.skill,
            "description": self.description,
            "depends_on": self.depends_on,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }


@dataclass
class PlaybookContract:
    id: str
    objective: str
    required_agents: list[str]
    required_skills: list[str]
    required_lcps: list[str]
    allowed_mcps: list[str]
    steps: list[PlaybookStep]
    blocking_conditions: list[str]
    outputs: list[str]
    final_report_sections: list[str]
    risk_level: str = "low"
    required_capabilities: list[str] = field(default_factory=list)
    path: str = ""

    def is_valid(self) -> bool:
        return all([
            bool(self.id),
            bool(self.objective),
            len(self.required_skills) > 0 or len(self.steps) > 0,
            isinstance(self.blocking_conditions, list),
            isinstance(self.steps, list),
        ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "objective": self.objective,
            "required_agents": self.required_agents,
            "required_skills": self.required_skills,
            "required_lcps": self.required_lcps,
            "allowed_mcps": self.allowed_mcps,
            "steps": [s.to_dict() for s in self.steps],
            "blocking_conditions": self.blocking_conditions,
            "outputs": self.outputs,
            "final_report_sections": self.final_report_sections,
            "risk_level": self.risk_level,
            "required_capabilities": self.required_capabilities,
            "path": self.path,
        }


@dataclass
class PlaybookRequest:
    execution_id: str
    playbook_id: str
    actor: str
    role: str
    target_path: str = "."
    input: dict[str, Any] = field(default_factory=dict)
    approval_id: Optional[str] = None
    dry_run: bool = True
    request_id: str = field(default_factory=lambda: f"pr-{uuid4().hex[:12]}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "playbook_id": self.playbook_id,
            "actor": self.actor,
            "role": self.role,
            "target_path": self.target_path,
            "input": self.input,
            "approval_id": self.approval_id,
            "dry_run": self.dry_run,
            "request_id": self.request_id,
        }


@dataclass
class PlaybookResult:
    execution_id: str
    playbook_id: str
    status: PlaybookStatus
    steps: list[dict[str, Any]] = field(default_factory=list)
    skill_results: list[dict[str, Any]] = field(default_factory=list)
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
            "playbook_id": self.playbook_id,
            "status": self.status,
            "steps": self.steps,
            "skill_results": self.skill_results,
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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
