from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from aeos.core.registries.registry_models import SkillEntry
from aeos.core.skill_engine.skill_models import SkillContract


ExecutionStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


def generate_execution_id() -> str:
    return f"exec-{uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExecutionRequest:
    run_type: str
    entity_id: str
    actor: str = "cli-user"
    role: str = "operator"
    input: dict[str, Any] = field(default_factory=dict)
    target_path: str = "."
    dry_run: bool = True
    approval_id: Optional[str] = None
    execution_id: str = field(default_factory=generate_execution_id)

    def __post_init__(self) -> None:
        if not self.execution_id:
            self.execution_id = generate_execution_id()

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "run_type": self.run_type,
            "entity_id": self.entity_id,
            "actor": self.actor,
            "role": self.role,
            "input": self.input,
            "target_path": self.target_path,
            "dry_run": self.dry_run,
            "approval_id": self.approval_id,
        }


@dataclass
class ResolvedSkill:
    skill_id: str
    entry: SkillEntry
    contract: SkillContract
    path: str
    validation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "entry": self.entry.to_dict(),
            "contract": self.contract.to_dict(),
            "path": self.path,
            "validation": self.validation,
        }


@dataclass
class ExecutionResult:
    execution_id: str
    run_type: str
    entity_id: str
    status: ExecutionStatus
    mode: str = "dry-run"
    result: dict[str, Any] = field(default_factory=dict)
    facts: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)
    duration_ms: int = 0
    error: Optional[str] = None
    generated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "run_type": self.run_type,
            "entity_id": self.entity_id,
            "status": self.status,
            "mode": self.mode,
            "result": self.result,
            "facts": self.facts,
            "risks": self.risks,
            "evidence_refs": self.evidence_refs,
            "blocking_conditions": self.blocking_conditions,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "generated_at": self.generated_at,
        }
