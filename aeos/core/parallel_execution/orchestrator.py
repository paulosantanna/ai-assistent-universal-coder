"""AEOS Parallel Execution Orchestrator — schedules steps with conflict detection and deterministic ordering."""

from .conflict_detector import ConflictDetector
from .scheduler import DeterministicParallelScheduler
from .contracts import StepResourceSet, StepConflict


class ParallelOrchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.max_parallel = config.get("max_parallel_steps", 4)
        self.conflict_detector = ConflictDetector()
        self.scheduler = DeterministicParallelScheduler(max_parallel_steps=self.max_parallel)

    def orchestrate(self, steps: list[StepResourceSet]) -> dict:
        conflicts = self.conflict_detector.detect(steps)
        if conflicts:
            serialized = [c for c in conflicts if c.decision == "serialize"]
            if serialized:
                return {
                    "status": "sequential_forced",
                    "reason": "conflicts_detected",
                    "conflicts": len(serialized),
                    "groups": self._sequential_groups(steps),
                }

        ready_ids = [s.step_id for s in steps]
        groups = self.scheduler.schedule(ready_ids)
        return {
            "status": "parallel_scheduled",
            "reason": "no_conflicts",
            "groups": groups,
            "max_parallel": self.max_parallel,
        }

    def _sequential_groups(self, steps: list[StepResourceSet]) -> list[list[str]]:
        return [[s.step_id for s in steps]]