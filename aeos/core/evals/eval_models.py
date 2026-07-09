from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

EVAL_STATUS_PASS = "PASS"
EVAL_STATUS_FAIL = "FAIL"
EVAL_STATUS_ERROR = "ERROR"
EVAL_STATUS_SKIPPED = "SKIPPED"

EvalStatus = str  # "PASS" | "FAIL" | "ERROR" | "SKIPPED"


@dataclass
class EvalCase:
    case_id: str
    suite_id: str
    description: str
    severity: str = "medium"  # "low" | "medium" | "high" | "critical"
    expected: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    blocking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "suite_id": self.suite_id,
            "description": self.description,
            "severity": self.severity,
            "expected": self.expected,
            "inputs": self.inputs,
            "blocking": self.blocking,
        }


@dataclass
class EvalResult:
    execution_id: str
    suite_id: str
    case_id: str
    status: EvalStatus
    score: float = 0.0
    severity: str = "medium"
    expected: str = ""
    actual: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    blocking: bool = False
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "suite_id": self.suite_id,
            "case_id": self.case_id,
            "status": self.status,
            "score": self.score,
            "severity": self.severity,
            "expected": self.expected,
            "actual": self.actual,
            "evidence_refs": self.evidence_refs,
            "blocking": self.blocking,
            "error": self.error,
        }


@dataclass
class EvalSuite:
    suite_id: str
    description: str = ""
    cases: list[EvalCase] = field(default_factory=list)
    blocking: bool = False
    min_pass_score: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "description": self.description,
            "cases": [c.to_dict() for c in self.cases],
            "blocking": self.blocking,
            "min_pass_score": self.min_pass_score,
        }


@dataclass
class EvalScorecard:
    execution_id: str
    suites: dict[str, dict[str, Any]] = field(default_factory=dict)
    overall_score: float = 0.0
    total_cases: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    blocking_failures: list[str] = field(default_factory=list)
    status: str = "PASS"

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "suites": self.suites,
            "overall_score": self.overall_score,
            "total_cases": self.total_cases,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "errors": self.errors,
            "blocking_failures": self.blocking_failures,
            "status": self.status,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_eval_id() -> str:
    return f"eval-{uuid4().hex[:12]}"
