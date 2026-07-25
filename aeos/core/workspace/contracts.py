"""Contratos imutáveis do kernel de tarefas do AEOS Workspace OS."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class TaskState(str, Enum):
    """Estado operacional persistido de uma tarefa."""

    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class OutcomeStatus(str, Enum):
    """Resultado semântico, deliberadamente separado do estado operacional."""

    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    ABSTAINED = "ABSTAINED"


class KnowledgeKind(str, Enum):
    """Classificação epistêmica fechada para alegações de uma tarefa."""

    FACT = "FACT"
    INFERENCE = "INFERENCE"
    ASSUMPTION = "ASSUMPTION"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class EvidenceClaim:
    kind: KnowledgeKind
    statement: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("evidence statement must not be empty")
        if any(not reference.strip() for reference in self.evidence_refs):
            raise ValueError("evidence references must not be empty")
        if self.kind is KnowledgeKind.FACT and not self.evidence_refs:
            raise ValueError("FACT claims require evidence references")


@dataclass(frozen=True, slots=True)
class TaskOutcome:
    status: OutcomeStatus
    summary: str
    claims: tuple[EvidenceClaim, ...] = ()

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("outcome summary must not be empty")

    @property
    def fact_refs(self) -> frozenset[str]:
        return frozenset(
            reference
            for claim in self.claims
            if claim.kind is KnowledgeKind.FACT
            for reference in claim.evidence_refs
        )


@dataclass(frozen=True, slots=True)
class TaskSpec:
    task_id: str
    priority: int = 0
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if any(not dependency.strip() for dependency in self.dependencies):
            raise ValueError("dependency ids must not be empty")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ValueError(f"task {self.task_id!r} has duplicate dependencies")


@dataclass(frozen=True, slots=True)
class TaskSnapshot:
    """Snapshot CAS-friendly: cada transição produz uma nova revisão."""

    task_id: str
    state: TaskState = TaskState.PENDING
    revision: int = 0
    outcome: TaskOutcome | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if self.revision < 0:
            raise ValueError("revision must be non-negative")
        if self.state is TaskState.COMPLETED:
            if (
                self.outcome is None
                or self.outcome.status is not OutcomeStatus.SUCCEEDED
                or not self.outcome.fact_refs
            ):
                raise ValueError(
                    "a completed snapshot requires a successful, evidenced outcome"
                )
        elif self.state is TaskState.FAILED:
            if self.outcome is not None and self.outcome.status is not OutcomeStatus.FAILED:
                raise ValueError("a failed snapshot requires a FAILED outcome")
        elif self.state is TaskState.BLOCKED:
            if self.outcome is not None and self.outcome.status not in {
                OutcomeStatus.PARTIAL,
                OutcomeStatus.ABSTAINED,
            }:
                raise ValueError("a blocked snapshot requires PARTIAL or ABSTAINED")
        elif self.outcome is not None:
            raise ValueError("this task state may not contain an outcome")
