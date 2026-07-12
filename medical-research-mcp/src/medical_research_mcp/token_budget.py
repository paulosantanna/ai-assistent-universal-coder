from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


@dataclass(frozen=True)
class TokenBudget:
    total: int
    root_percent: int = 14
    evidence_percent: int = 22
    specialists_percent: int = 44
    synthesis_percent: int = 8
    judge_percent: int = 12

    def allocate(self) -> dict[str, int]:
        if self.total < 2048:
            raise ValueError("Token budget must be at least 2048")
        percentages = (
            self.root_percent + self.evidence_percent + self.specialists_percent
            + self.synthesis_percent + self.judge_percent
        )
        if percentages != 100:
            raise ValueError("Token budget percentages must total 100")
        return {
            "root": self.total * self.root_percent // 100,
            "evidence": self.total * self.evidence_percent // 100,
            "specialists": self.total * self.specialists_percent // 100,
            "synthesis": self.total * self.synthesis_percent // 100,
            "judge": self.total * self.judge_percent // 100,
        }


RISK_MULTIPLIERS = {
    "LOW": 0.70,
    "MEDIUM": 1.00,
    "HIGH": 1.25,
    "CRITICAL": 1.50,
}


def task_budget(base_tokens: int, risk: str, complexity: float = 1.0) -> int:
    multiplier = RISK_MULTIPLIERS.get(risk.upper(), 1.0)
    bounded_complexity = min(max(complexity, 0.5), 2.0)
    return max(512, int(base_tokens * multiplier * bounded_complexity))


def context_cache_key(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def context_compaction_policy() -> list[str]:
    return [
        "Pass paths, symbols, line ranges, hashes, and evidence indexes instead of repository dumps.",
        "Use bounded handovers with explicit inclusion and exclusion scope.",
        "Run deterministic scanners before requesting model reasoning.",
        "Cache repository inventories, source metadata, and findings by content hash.",
        "Do not resend unchanged evidence.",
        "Deduplicate findings before Root synthesis.",
        "Stop parallel investigations when sufficient evidence already resolves the question.",
        "Reserve Judge context for scope, claims, direct evidence, contradictions, and blockers.",
        "Never remove evidence required for safety, scientific validity, or reproducibility.",
    ]
