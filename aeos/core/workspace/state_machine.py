"""Máquina de estados fechada e otimista para tarefas."""

from __future__ import annotations

from dataclasses import replace

from aeos.core.workspace.contracts import (
    OutcomeStatus,
    TaskOutcome,
    TaskSnapshot,
    TaskState,
)


from .exceptions import RevisionConflictError

class TaskTransitionError(Exception):
    """Erro base tipado de transição."""



class InvalidTransition(TaskTransitionError):
    def __init__(self, source: TaskState, target: TaskState) -> None:
        self.source = source
        self.target = target
        super().__init__(f"invalid task transition: {source.value} -> {target.value}")


class CompletionEvidenceRequired(TaskTransitionError):
    """Conclusão recusada por resultado ou evidência insuficiente."""


_ALLOWED_TRANSITIONS: dict[TaskState, frozenset[TaskState]] = {
    TaskState.PENDING: frozenset({TaskState.READY, TaskState.CANCELLED}),
    TaskState.READY: frozenset(
        {TaskState.RUNNING, TaskState.BLOCKED, TaskState.CANCELLED}
    ),
    TaskState.RUNNING: frozenset(
        {
            TaskState.WAITING,
            TaskState.BLOCKED,
            TaskState.COMPLETED,
            TaskState.FAILED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.WAITING: frozenset(
        {TaskState.RUNNING, TaskState.BLOCKED, TaskState.CANCELLED}
    ),
    TaskState.BLOCKED: frozenset({TaskState.READY, TaskState.CANCELLED}),
    TaskState.FAILED: frozenset({TaskState.READY, TaskState.CANCELLED}),
    TaskState.COMPLETED: frozenset(),
    TaskState.CANCELLED: frozenset(),
}


def allowed_targets(state: TaskState) -> frozenset[TaskState]:
    return _ALLOWED_TRANSITIONS[state]


def transition(
    snapshot: TaskSnapshot,
    target: TaskState,
    *,
    expected_revision: int,
    outcome: TaskOutcome | None = None,
    verified_evidence_refs: frozenset[str] = frozenset(),
) -> TaskSnapshot:
    """Aplica uma transição atômica sobre um snapshot imutável."""

    if expected_revision != snapshot.revision:
        raise RevisionConflictError(
            f"stale task revision: expected {expected_revision}, actual {snapshot.revision}",
            expected_revision=expected_revision,
            actual_revision=snapshot.revision,
        )
    if target not in _ALLOWED_TRANSITIONS[snapshot.state]:
        raise InvalidTransition(snapshot.state, target)
    if target is TaskState.COMPLETED:
        if (
            outcome is None
            or outcome.status is not OutcomeStatus.SUCCEEDED
            or not outcome.fact_refs
            or not outcome.fact_refs.issubset(verified_evidence_refs)
        ):
            raise CompletionEvidenceRequired(
                "completion requires a SUCCEEDED outcome whose FACT references "
                "were independently verified"
            )
    elif target is TaskState.FAILED:
        if outcome is not None and outcome.status is not OutcomeStatus.FAILED:
            raise TaskTransitionError("FAILED state only accepts a FAILED outcome")
    elif target is TaskState.BLOCKED:
        if outcome is not None and outcome.status not in {
            OutcomeStatus.PARTIAL,
            OutcomeStatus.ABSTAINED,
        }:
            raise TaskTransitionError(
                "BLOCKED state only accepts PARTIAL or ABSTAINED outcomes"
            )
    elif outcome is not None:
        raise TaskTransitionError("outcome is not valid for the target state")

    return replace(
        snapshot,
        state=target,
        revision=snapshot.revision + 1,
        outcome=outcome,
    )
