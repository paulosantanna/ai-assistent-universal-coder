from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List
from .contracts import TaskDefinition

class TaskGraph:
    def __init__(self, execution_id: str, playbook_id: str):
        self.execution_id = execution_id
        self.playbook_id = playbook_id
        self.tasks: Dict[str, TaskDefinition] = {}
        self.dependencies: Dict[str, List[str]] = {}

    def add_task(self, task: TaskDefinition, depends_on: List[str] | None = None):
        self.tasks[task.task_id] = task
        self.dependencies[task.task_id] = depends_on or []

    def ready_tasks(self) -> List[TaskDefinition]:
        completed = {task_id for task_id, task in self.tasks.items() if task.status == "COMPLETED"}
        ready = []
        for task_id, task in self.tasks.items():
            if task.status != "PENDING":
                continue
            if all(dep in completed for dep in self.dependencies.get(task_id, [])):
                ready.append(task)
        return ready

    def unresolved_required_tasks(self) -> List[str]:
        return [
            task_id for task_id, task in self.tasks.items()
            if task.status not in ("COMPLETED", "BLOCKED")
        ]

    def to_dict(self):
        return {
            "execution_id": self.execution_id,
            "playbook_id": self.playbook_id,
            "tasks": {k: asdict(v) for k, v in self.tasks.items()},
            "dependencies": self.dependencies,
        }
