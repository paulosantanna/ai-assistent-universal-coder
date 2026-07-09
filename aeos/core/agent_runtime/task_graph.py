from __future__ import annotations

from dataclasses import asdict
from typing import Any

from aeos.core.agent_runtime.agent_models import AgentTask


class TaskGraph:
    def __init__(self, execution_id: str):
        self.execution_id = execution_id
        self.tasks: dict[str, AgentTask] = {}
        self.dependencies: dict[str, list[str]] = {}

    def add_task(self, task: AgentTask, depends_on: list[str] | None = None) -> None:
        self.tasks[task.task_id] = task
        self.dependencies[task.task_id] = depends_on or []

    def ready_tasks(self) -> list[AgentTask]:
        completed = {tid for tid, t in self.tasks.items() if t.status in ("COMPLETED", "BLOCKED")}
        ready = []
        for tid, task in self.tasks.items():
            if task.status != "PENDING":
                continue
            deps = self.dependencies.get(tid, [])
            if all(d in completed for d in deps):
                ready.append(task)
        return ready

    def detect_cycles(self) -> list[str]:
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycles: list[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.dependencies.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        cycles.append(f"Cycle involving: {node} -> {neighbor}")
                        return True
                elif neighbor in rec_stack:
                    cycles.append(f"Cycle detected: {node} -> {neighbor}")
                    return True
            rec_stack.discard(node)
            return False

        for tid in self.tasks:
            if tid not in visited:
                dfs(tid)
        return cycles

    def unresolved_required_tasks(self) -> list[str]:
        return [tid for tid, t in self.tasks.items() if t.status not in ("COMPLETED", "BLOCKED")]

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "tasks": {k: v.to_dict() for k, v in self.tasks.items()},
            "dependencies": self.dependencies,
        }
