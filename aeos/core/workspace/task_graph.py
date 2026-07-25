"""DAG validado de tarefas."""

from __future__ import annotations

import heapq
from collections.abc import Iterable, Mapping

from aeos.core.workspace.contracts import TaskSnapshot, TaskSpec, TaskState


class TaskGraphError(ValueError):
    """Erro base de validação do grafo."""


class DuplicateTaskError(TaskGraphError):
    pass


class MissingDependencyError(TaskGraphError):
    pass


class SelfDependencyError(TaskGraphError):
    pass


class CycleError(TaskGraphError):
    pass


class TaskGraph:
    """Representação imutável por convenção, validada na construção."""

    def __init__(self, tasks: Iterable[TaskSpec]) -> None:
        indexed: dict[str, TaskSpec] = {}
        for task in tasks:
            if task.task_id in indexed:
                raise DuplicateTaskError(f"duplicate task_id: {task.task_id}")
            indexed[task.task_id] = task

        for task in indexed.values():
            if task.task_id in task.dependencies:
                raise SelfDependencyError(
                    f"task {task.task_id!r} depends on itself"
                )
            missing = sorted(set(task.dependencies).difference(indexed))
            if missing:
                raise MissingDependencyError(
                    f"task {task.task_id!r} has missing dependencies: "
                    f"{', '.join(missing)}"
                )

        self._tasks = indexed
        self._topological_ids = self._topological_sort()

    def _topological_sort(self) -> tuple[str, ...]:
        indegree = {
            task_id: len(task.dependencies)
            for task_id, task in self._tasks.items()
        }
        dependants: dict[str, list[str]] = {
            task_id: [] for task_id in self._tasks
        }
        for task in self._tasks.values():
            for dependency in task.dependencies:
                dependants[dependency].append(task.task_id)

        available = [task_id for task_id, degree in indegree.items() if degree == 0]
        heapq.heapify(available)
        ordered: list[str] = []
        while available:
            task_id = heapq.heappop(available)
            ordered.append(task_id)
            for dependant in sorted(dependants[task_id]):
                indegree[dependant] -= 1
                if indegree[dependant] == 0:
                    heapq.heappush(available, dependant)

        if len(ordered) != len(self._tasks):
            cyclic = sorted(
                task_id for task_id, degree in indegree.items() if degree > 0
            )
            raise CycleError(f"task graph contains a cycle: {', '.join(cyclic)}")
        return tuple(ordered)

    def task(self, task_id: str) -> TaskSpec:
        return self._tasks[task_id]

    def topological_ids(self) -> tuple[str, ...]:
        return self._topological_ids

    def ready_tasks(
        self, snapshots: Mapping[str, TaskSnapshot]
    ) -> tuple[TaskSpec, ...]:
        unknown = sorted(set(snapshots).difference(self._tasks))
        if unknown:
            raise KeyError(f"snapshots contain unknown tasks: {', '.join(unknown)}")

        ready: list[TaskSpec] = []
        for task_id in self._topological_ids:
            task = self._tasks[task_id]
            snapshot = snapshots.get(task_id)
            if snapshot is not None and snapshot.task_id != task_id:
                raise ValueError(f"snapshot key/task_id mismatch for {task_id!r}")
            state = snapshot.state if snapshot is not None else TaskState.PENDING
            if state not in {TaskState.PENDING, TaskState.READY}:
                continue
            if all(
                snapshots.get(dependency, TaskSnapshot(dependency)).state
                is TaskState.COMPLETED
                for dependency in task.dependencies
            ):
                ready.append(task)
        return tuple(ready)
