"""AEOS Enterprise Judge Engine — deterministic judge with enterprise gates."""

from .enterprise_judge_gates import ENTERPRISE_JUDGE_BLOCKERS
from .judge_enterprise_gates import ENTERPRISE_BLOCKING_GATES


class EnterpriseJudgeEngine:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.min_score = self.config.get("min_score", 9.0)
        self.blocking_gates = set(ENTERPRISE_BLOCKING_GATES)
        self.judge_blockers = set(ENTERPRISE_JUDGE_BLOCKERS)

    def evaluate(self, evidence: dict) -> dict:
        checks = {}
        blocks = []

        for gate in self.blocking_gates:
            detection = evidence.get(gate, False)
            if detection:
                blocks.append(f"enterprise_gate_blocked:{gate}")
            checks[gate] = "PASS" if not detection else "BLOCKED"

        for blocker in self.judge_blockers:
            detection = evidence.get(blocker, False)
            if detection:
                blocks.append(f"judge_blocker:{blocker}")
            checks[blocker] = "PASS" if not detection else "BLOCKED"

        deterministic_blocks = [b for b in blocks if b in ENTERPRISE_BLOCKING_GATES]
        final_score = max(0.0, 10.0 - (len(blocks) * 2.0))

        return {
            "decision": "BLOCKED" if blocks else "PASS",
            "final_score": final_score,
            "min_score": self.min_score,
            "checks": checks,
            "blocking_reasons": blocks,
            "deterministic_blocks": deterministic_blocks,
        }