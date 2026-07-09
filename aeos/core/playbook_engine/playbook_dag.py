from __future__ import annotations

from typing import Any

from aeos.core.playbook_engine.playbook_models import PlaybookStep, PlaybookContract


class PlaybookDAG:
    def __init__(self, contract: PlaybookContract):
        self.contract = contract
        self._adjacency: dict[str, list[str]] = {}
        self._build_adjacency()

    def _build_adjacency(self) -> None:
        for step in self.contract.steps:
            self._adjacency[step.id] = step.depends_on

    def detect_cycles(self) -> list[str]:
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycles: list[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self._adjacency.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        cycles.append(f"Cycle involving: {node} -> {neighbor}")
                        return True
                elif neighbor in rec_stack:
                    cycles.append(f"Cycle detected: {node} -> {neighbor}")
                    return True
            rec_stack.discard(node)
            return False

        for step in self.contract.steps:
            if step.id not in visited:
                dfs(step.id)

        return cycles

    def detect_unresolved_dependencies(self, available_skills: list[str]) -> list[str]:
        unresolved: list[str] = []
        for step in self.contract.steps:
            if step.skill and step.skill not in available_skills:
                unresolved.append(f"Step '{step.id}' requires skill '{step.skill}' which is not available")
        return unresolved

    def topological_sort(self) -> list[PlaybookStep]:
        visited: set[str] = set()
        result: list[PlaybookStep] = []
        temp_marks: set[str] = set()

        def visit(step_id: str) -> None:
            if step_id in temp_marks:
                return
            if step_id in visited:
                return
            temp_marks.add(step_id)
            for dep in self._adjacency.get(step_id, []):
                visit(dep)
            temp_marks.discard(step_id)
            visited.add(step_id)
            step = next((s for s in self.contract.steps if s.id == step_id), None)
            if step:
                result.append(step)

        for step in self.contract.steps:
            if step.id not in visited:
                visit(step.id)

        return result

    def ready_steps(self, completed: set[str]) -> list[PlaybookStep]:
        ready = []
        for step in self.contract.steps:
            if step.id in completed:
                continue
            deps = self._adjacency.get(step.id, [])
            if all(d in completed for d in deps):
                ready.append(step)
        return ready

    def to_dict(self) -> dict[str, Any]:
        return {
            "playbook_id": self.contract.id,
            "adjacency": self._adjacency,
            "steps": [s.to_dict() for s in self.contract.steps],
        }
