import pytest

from aeos.core.workspace.contracts import TaskSnapshot, TaskSpec, TaskState
from aeos.core.workspace.scheduler import DeterministicScheduler
from aeos.core.workspace.task_graph import TaskGraph


def test_scheduler_orders_priority_desc_then_task_id_asc():
    graph = TaskGraph(
        [
            TaskSpec("z-low", priority=1),
            TaskSpec("z-high", priority=5),
            TaskSpec("a-high", priority=5),
        ]
    )

    selected = DeterministicScheduler().select(graph, {})

    assert tuple(task.task_id for task in selected) == (
        "a-high",
        "z-high",
        "z-low",
    )


def test_scheduler_is_independent_of_insertion_order():
    tasks = [
        TaskSpec("beta", priority=2),
        TaskSpec("alpha", priority=2),
        TaskSpec("omega", priority=1),
    ]
    scheduler = DeterministicScheduler()

    forward = scheduler.select(TaskGraph(tasks), {})
    reverse = scheduler.select(TaskGraph(reversed(tasks)), {})

    assert forward == reverse


def test_scheduler_does_not_release_blocked_dependency():
    graph = TaskGraph(
        [
            TaskSpec("root", priority=1),
            TaskSpec("child", priority=100, dependencies=("root",)),
        ]
    )

    selected = DeterministicScheduler().select(
        graph,
        {"root": TaskSnapshot("root", state=TaskState.BLOCKED)},
    )

    assert selected == ()


def test_scheduler_limit_is_deterministic_and_validated():
    graph = TaskGraph([TaskSpec("b"), TaskSpec("a")])
    scheduler = DeterministicScheduler()

    assert tuple(task.task_id for task in scheduler.select(graph, {}, limit=1)) == (
        "a",
    )
    assert scheduler.select(graph, {}, limit=0) == ()
    with pytest.raises(ValueError):
        scheduler.select(graph, {}, limit=-1)
