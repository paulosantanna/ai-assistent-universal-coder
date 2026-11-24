"""A worker is born for one generation, delivers, and dies. Resume is refused."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


class ResumeForbidden(Exception):
    """A dead worker is not a session. The same task gets a new id."""


@dataclass(frozen=True)
class WorkerLife:
    worker_id: str
    task_id: str
    role: str
    generation: int
    state: str

    @property
    def resume_forbidden(self) -> bool:
        return True


class Ledger:
    def __init__(self) -> None:
        self._workers: dict[str, WorkerLife] = {}
        self._generation: dict[str, int] = {}

    def born(self, task_id: str, role: str, generation: int | None = None) -> WorkerLife:
        if generation is None:
            generation = self._generation.get(task_id, 0) + 1
            self._generation[task_id] = generation
        else:
            self._generation[task_id] = max(self._generation.get(task_id, 0), generation)
        worker = WorkerLife(str(uuid4()), task_id, role, generation, "born")
        self._workers[worker.worker_id] = worker
        return worker

    def die(self, worker_id: str) -> WorkerLife:
        current = self._workers[worker_id]
        dead = WorkerLife(current.worker_id, current.task_id, current.role, current.generation, "died")
        self._workers[worker_id] = dead
        return dead

    def resume(self, worker_id: str) -> WorkerLife:
        raise ResumeForbidden(worker_id)

    def recreate(self, task_id: str, role: str) -> WorkerLife:
        previous = [item for item in self._workers.values() if item.task_id == task_id]
        if any(item.state != "died" for item in previous):
            raise ResumeForbidden("recreate requires every previous worker of the task to be dead")
        generation = max(item.generation for item in previous) + 1
        return self.born(task_id, role, generation)

    def get(self, worker_id: str) -> WorkerLife:
        return self._workers[worker_id]
