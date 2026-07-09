from __future__ import annotations

import json
from pathlib import Path

from aeos.core.policy.policy_models import PolicyDecision


class PolicyReporter:
    def __init__(self, output_dir: str = ".aeos/evidence"):
        self.output_dir = Path(output_dir)

    def write_decisions_jsonl(self, execution_id: str, decisions: list[PolicyDecision]) -> str:
        base = self.output_dir / execution_id
        base.mkdir(parents=True, exist_ok=True)
        fp = base / "policy-decisions.jsonl"
        with open(fp, "a", encoding="utf-8") as f:
            for d in decisions:
                f.write(json.dumps(d.to_dict(), ensure_ascii=False) + "\n")
        return str(fp)
