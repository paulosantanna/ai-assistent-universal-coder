from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

RuntimeStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


@dataclass
class RuntimeRequest:
    execution_id: str
    run_type: str  # "skill" | "playbook" | "agent"
    entity_id: str
    actor: str
    role: str
    input: dict[str, Any] = field(default_factory=dict)
    target_path: str = "."
    dry_run: bool = True
    approval_id: Optional[str] = None

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
class RuntimeResult:
    execution_id: str
    run_type: str
    entity_id: str
    status: RuntimeStatus
    result: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "run_type": self.run_type,
            "entity_id": self.entity_id,
            "status": self.status,
            "result": self.result,
            "evidence_refs": self.evidence_refs,
            "blocking_conditions": self.blocking_conditions,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


@dataclass
class EvidenceManifest:
    execution_id: str
    generated_at: str = ""
    files: list[dict[str, Any]] = field(default_factory=list)
    total_records: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "generated_at": self.generated_at,
            "files": self.files,
            "total_records": self.total_records,
        }


def generate_execution_id() -> str:
    return f"exec-{uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
