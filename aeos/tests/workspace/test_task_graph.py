import pytest

from aeos.core.workspace.contracts import TaskSnapshot, TaskSpec, TaskState
from aeos.core.workspace.task_graph import (
    CycleError,
    DuplicateTaskError,
    MissingDependencyError,
    SelfDependencyError,
    TaskGraph,
)


def test_missing_dependency_is_rejected():
    with pytest.raises(MissingDependencyError):
        TaskGraph([TaskSpec("child", dependencies=("missing",))])


def test_self_dependency_is_rejected():
    with pytest.raises(SelfDependencyError):
        TaskGraph([TaskSpec("task", dependencies=("task",))])


def test_cycle_is_rejected():
    with pytest.raises(CycleError):
        TaskGraph(
            [
                TaskSpec("a", dependencies=("c",)),
                TaskSpec("b", dependencies=("a",)),
                TaskSpec("c", dependencies=("b",)),
            ]
        )


def test_duplicate_task_is_rejected():
    with pytest.raises(DuplicateTaskError):
        TaskGraph([TaskSpec("same"), TaskSpec("same")])


def test_topological_order_is_stable_across_insertion_orders():
    first = TaskGraph(
        [
            TaskSpec("c", dependencies=("a",)),
            TaskSpec("b", dependencies=("a",)),
            TaskSpec("a"),
        ]
    )
    second = TaskGraph(
        [
            TaskSpec("a"),
            TaskSpec("b", dependencies=("a",)),
            TaskSpec("c", dependencies=("a",)),
        ]
    )

    assert first.topological_ids() == second.topological_ids() == ("a", "b", "c")


def test_only_completed_dependency_releases_dependant():
    graph = TaskGraph([TaskSpec("root"), TaskSpec("child", dependencies=("root",))])

    blocked = graph.ready_tasks(
        {"root": TaskSnapshot("root", state=TaskState.BLOCKED)}
    )
    failed = graph.ready_tasks(
        {"root": TaskSnapshot("root", state=TaskState.FAILED)}
    )
    completed = graph.ready_tasks(
        {
            "root": TaskSnapshot(
                "root",
                state=TaskState.COMPLETED,
                outcome=_outcome(),
            )
        }
    )

    assert blocked == ()
    assert failed == ()
    assert tuple(task.task_id for task in completed) == ("child",)


def _outcome():
    from aeos.core.workspace.contracts import (
        EvidenceClaim,
        KnowledgeKind,
        OutcomeStatus,
        TaskOutcome,
    )

    return TaskOutcome(
        OutcomeStatus.SUCCEEDED,
        "done",
        (EvidenceClaim(KnowledgeKind.FACT, "done", ("ref",)),),
    )
