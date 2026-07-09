from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

READINESS_PASS = "PASS"
READINESS_BLOCKED = "BLOCKED"
READINESS_REVIEW = "REVIEW"
READINESS_ERROR = "ERROR"

ReadinessStatus = str  # "PASS" | "BLOCKED" | "REVIEW" | "ERROR"


@dataclass
class ReadinessResult:
    execution_id: str
    status: ReadinessStatus
    overall_score: float = 0.0
    categories: dict[str, float] = field(default_factory=dict)
    critical_blockers: list[str] = field(default_factory=list)
    high_risks: list[str] = field(default_factory=list)
    medium_risks: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "overall_score": self.overall_score,
            "categories": self.categories,
            "critical_blockers": self.critical_blockers,
            "high_risks": self.high_risks,
            "medium_risks": self.medium_risks,
            "recommendations": self.recommendations,
            "evidence_refs": self.evidence_refs,
            "timestamp": self.timestamp,
        }


@dataclass
class ReadinessScorecard:
    execution_id: str
    status: ReadinessStatus
    overall_score: float = 0.0
    categories: dict[str, float] = field(default_factory=dict)
    category_details: dict[str, dict[str, Any]] = field(default_factory=dict)
    critical_blockers: list[dict[str, Any]] = field(default_factory=list)
    high_risks: list[dict[str, Any]] = field(default_factory=list)
    medium_risks: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "overall_score": self.overall_score,
            "categories": self.categories,
            "category_details": self.category_details,
            "critical_blockers": self.critical_blockers,
            "high_risks": self.high_risks,
            "medium_risks": self.medium_risks,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_readiness_id() -> str:
    return f"readiness-{uuid4().hex[:12]}"
