from __future__ import annotations

from fnmatch import fnmatch
from uuid import uuid4
from .contracts import StepResourceSet, StepConflict

class ConflictDetector:
    def detect(self, steps: list[StepResourceSet]) -> list[StepConflict]:
        conflicts: list[StepConflict] = []

        for i, a in enumerate(steps):
            for b in steps[i+1:]:
                if self._overlap(a.write_set, b.write_set):
                    conflicts.append(self._conflict("WRITE_WRITE", a, b, "serialize", "write sets overlap"))
                if self._overlap(a.write_set, b.read_set) or self._overlap(b.write_set, a.read_set):
                    conflicts.append(self._conflict("READ_WRITE", a, b, "serialize", "read/write sets overlap"))
                if set(a.locks).intersection(set(b.locks)):
                    conflicts.append(self._conflict("RESOURCE_LOCK", a, b, "serialize", "shared lock"))

        return conflicts

    def _overlap(self, left: list[str], right: list[str]) -> bool:
        for l in left:
            for r in right:
                if l == r or fnmatch(l, r) or fnmatch(r, l):
                    return True
        return False

    def _conflict(self, ctype: str, a: StepResourceSet, b: StepResourceSet, decision: str, reason: str):
        return StepConflict(
            conflict_id=str(uuid4()),
            conflict_type=ctype,
            step_a=a.step_id,
            step_b=b.step_id,
            decision=decision,
            reason=reason,
        )
