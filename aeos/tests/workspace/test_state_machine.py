import pytest

from aeos.core.workspace.contracts import (
    EvidenceClaim,
    KnowledgeKind,
    OutcomeStatus,
    TaskOutcome,
    TaskSnapshot,
    TaskState,
)
from aeos.core.workspace.state_machine import (
    CompletionEvidenceRequired,
    InvalidTransition,
    RevisionConflict,
    allowed_targets,
    transition,
)


def successful_outcome() -> TaskOutcome:
    return TaskOutcome(
        status=OutcomeStatus.SUCCEEDED,
        summary="verified",
        claims=(
            EvidenceClaim(
                kind=KnowledgeKind.FACT,
                statement="focused tests passed",
                evidence_refs=("pytest:workspace",),
            ),
        ),
    )


def snapshot_in(state: TaskState, *, revision: int = 0) -> TaskSnapshot:
    outcome = successful_outcome() if state is TaskState.COMPLETED else None
    return TaskSnapshot("task", state=state, revision=revision, outcome=outcome)


VALID_TRANSITIONS = {
    TaskState.PENDING: {TaskState.READY, TaskState.CANCELLED},
    TaskState.READY: {TaskState.RUNNING, TaskState.BLOCKED, TaskState.CANCELLED},
    TaskState.RUNNING: {
        TaskState.WAITING,
        TaskState.BLOCKED,
        TaskState.COMPLETED,
        TaskState.FAILED,
        TaskState.CANCELLED,
    },
    TaskState.WAITING: {
        TaskState.RUNNING,
        TaskState.BLOCKED,
        TaskState.CANCELLED,
    },
    TaskState.BLOCKED: {TaskState.READY, TaskState.CANCELLED},
    TaskState.FAILED: {TaskState.READY, TaskState.CANCELLED},
    TaskState.COMPLETED: set(),
    TaskState.CANCELLED: set(),
}


@pytest.mark.parametrize(
    ("source", "target"),
    [
        (source, target)
        for source, targets in VALID_TRANSITIONS.items()
        for target in targets
    ],
)
def test_every_declared_transition_is_valid(source: TaskState, target: TaskState):
    snapshot = snapshot_in(source, revision=3)
    outcome = successful_outcome() if target is TaskState.COMPLETED else None

    changed = transition(
        snapshot,
        target,
        expected_revision=3,
        outcome=outcome,
        verified_evidence_refs=frozenset({"pytest:workspace"}),
    )

    assert changed.state is target
    assert changed.revision == 4
    assert snapshot.state is source


@pytest.mark.parametrize(
    ("source", "target"),
    [
        (source, target)
        for source in TaskState
        for target in TaskState
        if target not in VALID_TRANSITIONS[source]
    ],
)
def test_every_undeclared_transition_is_rejected(
    source: TaskState, target: TaskState
):
    with pytest.raises(InvalidTransition):
        transition(
            snapshot_in(source),
            target,
            expected_revision=0,
        )


def test_transition_table_and_public_query_remain_in_sync():
    for state, targets in VALID_TRANSITIONS.items():
        assert allowed_targets(state) == targets


def test_stale_revision_has_typed_conflict_and_does_not_mutate():
    snapshot = TaskSnapshot("task", state=TaskState.READY, revision=4)

    with pytest.raises(RevisionConflict) as error:
        transition(snapshot, TaskState.RUNNING, expected_revision=3)

    assert error.value.expected_revision == 3
    assert error.value.actual_revision == 4
    assert snapshot == TaskSnapshot("task", state=TaskState.READY, revision=4)


@pytest.mark.parametrize(
    "outcome",
    [
        None,
        TaskOutcome(OutcomeStatus.SUCCEEDED, "no claims"),
        TaskOutcome(
            OutcomeStatus.SUCCEEDED,
            "inference only",
            (EvidenceClaim(KnowledgeKind.INFERENCE, "likely"),),
        ),
        TaskOutcome(
            OutcomeStatus.SUCCEEDED,
            "unverified fact",
            (
                EvidenceClaim(
                    KnowledgeKind.FACT,
                    "observed",
                    ("log:1",),
                ),
            ),
        ),
        TaskOutcome(
            OutcomeStatus.PARTIAL,
            "not successful",
            (
                EvidenceClaim(
                    KnowledgeKind.FACT,
                    "observed",
                    ("log:1",),
                ),
            ),
        ),
    ],
)
def test_completion_without_validated_fact_is_blocked(outcome):
    with pytest.raises(CompletionEvidenceRequired):
        transition(
            TaskSnapshot("task", state=TaskState.RUNNING),
            TaskState.COMPLETED,
            expected_revision=0,
            outcome=outcome,
        )


def test_fact_claim_requires_reference():
    with pytest.raises(ValueError):
        EvidenceClaim(KnowledgeKind.FACT, "claim", ())


def test_completed_snapshot_cannot_be_forged_without_evidence():
    with pytest.raises(ValueError):
        TaskSnapshot("task", state=TaskState.COMPLETED)


def test_negative_and_abstained_outcomes_are_persistable():
    failed = transition(
        TaskSnapshot("task", state=TaskState.RUNNING),
        TaskState.FAILED,
        expected_revision=0,
        outcome=TaskOutcome(OutcomeStatus.FAILED, "deterministic failure"),
    )
    assert failed.outcome is not None
    assert failed.outcome.status is OutcomeStatus.FAILED

    blocked = transition(
        TaskSnapshot("task", state=TaskState.READY),
        TaskState.BLOCKED,
        expected_revision=0,
        outcome=TaskOutcome(OutcomeStatus.ABSTAINED, "insufficient evidence"),
    )
    assert blocked.outcome is not None
    assert blocked.outcome.status is OutcomeStatus.ABSTAINED
