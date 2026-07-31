from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def candidate_id() -> str:
    return f"dataset-{uuid4().hex[:12]}"


@dataclass(frozen=True)
class ContextFile:
    path: str
    sha256: str
    bytes: int
    estimated_tokens: int
    priority: str = "useful"
    cache_key: str = ""
    preview: str = ""
    redaction_findings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "estimated_tokens": self.estimated_tokens,
            "priority": self.priority,
            "cache_key": self.cache_key,
            "preview": self.preview,
            "redaction_findings": list(self.redaction_findings),
        }


@dataclass(frozen=True)
class ExcludedContextFile:
    path: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "reason": self.reason}


@dataclass
class ContextPack:
    execution_id: str
    objective: str
    target_path: str
    files: list[ContextFile] = field(default_factory=list)
    excluded_files: list[ExcludedContextFile] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    token_budget: dict[str, Any] = field(default_factory=dict)
    status: str = "PASS"
    blocking_conditions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=now_iso)

    @property
    def estimated_tokens(self) -> int:
        return sum(item.estimated_tokens for item in self.files)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "objective": self.objective,
            "target_path": self.target_path,
            "files": [item.to_dict() for item in self.files],
            "excluded_files": [item.to_dict() for item in self.excluded_files],
            "evidence_refs": list(self.evidence_refs),
            "token_budget": dict(self.token_budget),
            "status": self.status,
            "blocking_conditions": list(self.blocking_conditions),
            "estimated_tokens": self.estimated_tokens,
            "generated_at": self.generated_at,
        }


@dataclass
class ModelRoutingDecision:
    execution_id: str
    stage: str
    risk_level: str
    profile: str
    status: str
    paid: bool
    reason: str
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    max_context_tokens: int = 0
    approval_id: str | None = None
    blocking_conditions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "stage": self.stage,
            "risk_level": self.risk_level,
            "profile": self.profile,
            "status": self.status,
            "paid": self.paid,
            "reason": self.reason,
            "estimated_input_tokens": self.estimated_input_tokens,
            "estimated_output_tokens": self.estimated_output_tokens,
            "max_context_tokens": self.max_context_tokens,
            "approval_id": self.approval_id,
            "blocking_conditions": list(self.blocking_conditions),
            "generated_at": self.generated_at,
        }


@dataclass
class DatasetCandidate:
    candidate_id: str
    execution_id: str
    dataset_type: str
    status: str
    source_refs: list[str]
    prompt: str = ""
    completion: str = ""
    quality: dict[str, Any] = field(default_factory=dict)
    redaction_findings: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "execution_id": self.execution_id,
            "dataset_type": self.dataset_type,
            "status": self.status,
            "source_refs": list(self.source_refs),
            "prompt": self.prompt,
            "completion": self.completion,
            "quality": dict(self.quality),
            "redaction_findings": list(self.redaction_findings),
            "blocking_conditions": list(self.blocking_conditions),
            "generated_at": self.generated_at,
        }


@dataclass
class WorkflowPlan:
    execution_id: str
    workflow_id: str
    objective: str
    risk_level: str
    stages: list[str]
    model_stages: list[str]
    context_pack_ref: str = ""
    model_decision_refs: list[str] = field(default_factory=list)
    gates: dict[str, list[str]] = field(default_factory=dict)
    status: str = "PASS"
    blocking_conditions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "objective": self.objective,
            "risk_level": self.risk_level,
            "stages": list(self.stages),
            "model_stages": list(self.model_stages),
            "context_pack_ref": self.context_pack_ref,
            "model_decision_refs": list(self.model_decision_refs),
            "gates": {k: list(v) for k, v in self.gates.items()},
            "status": self.status,
            "blocking_conditions": list(self.blocking_conditions),
            "generated_at": self.generated_at,
        }


@dataclass
class WorkflowResult:
    execution_id: str
    workflow_id: str
    status: str
    plan: WorkflowPlan
    context_pack: ContextPack
    model_decisions: list[ModelRoutingDecision]
    dataset_candidates: list[DatasetCandidate] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "status": self.status,
            "plan": self.plan.to_dict(),
            "context_pack": self.context_pack.to_dict(),
            "model_decisions": [item.to_dict() for item in self.model_decisions],
            "dataset_candidates": [item.to_dict() for item in self.dataset_candidates],
            "evidence_refs": list(self.evidence_refs),
            "blocking_conditions": list(self.blocking_conditions),
        }
