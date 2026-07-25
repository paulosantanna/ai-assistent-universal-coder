"""Scheduler determinístico do kernel de tarefas."""

from __future__ import annotations

from collections.abc import Mapping

from aeos.core.workspace.contracts import TaskSnapshot, TaskSpec
from aeos.core.workspace.task_graph import TaskGraph


class DeterministicScheduler:
    """Seleciona tarefas prontas por prioridade decrescente e id crescente."""

    def select(
        self,
        graph: TaskGraph,
        snapshots: Mapping[str, TaskSnapshot],
        *,
        limit: int | None = None,
    ) -> tuple[TaskSpec, ...]:
        if limit is not None and limit < 0:
            raise ValueError("limit must be non-negative")
        ordered = sorted(
            graph.ready_tasks(snapshots),
            key=lambda task: (-task.priority, task.task_id),
        )
        if limit is None:
            return tuple(ordered)
        return tuple(ordered[:limit])
