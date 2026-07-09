from __future__ import annotations

from typing import Any, Optional

from aeos.core.playbook_engine.playbook_models import PlaybookContract, PlaybookStep
from aeos.core.playbook_engine.playbook_dag import PlaybookDAG


class PlaybookPlanner:
    def __init__(self):
        self.dag: Optional[PlaybookDAG] = None

    def plan(self, contract: PlaybookContract, available_skills: list[str]) -> dict[str, Any]:
        self.dag = PlaybookDAG(contract)

        cycles = self.dag.detect_cycles()
        if cycles:
            return {
                "valid": False,
                "cycles": cycles,
                "execution_order": [],
                "unresolved": [],
            }

        unresolved = self.dag.detect_unresolved_dependencies(available_skills)
        execution_order = self.dag.topological_sort()

        return {
            "valid": len(cycles) == 0,
            "cycles": cycles,
            "execution_order": [s.to_dict() for s in execution_order],
            "unresolved": unresolved,
        }
