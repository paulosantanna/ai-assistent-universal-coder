from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from datetime import datetime


class ReleaseStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    PASS = "pass"
    BLOCKED = "blocked"
    REVIEW = "review"
    FAILED = "failed"


class ReleaseBlockerCategory(Enum):
    TEST_FAILURE = "test_failure"
    SMOKE_TEST_BLOCKED = "smoke_test_blocked"
    JUDGE_BLOCKED = "judge_blocked"
    EVALS_BELOW_THRESHOLD = "evals_below_threshold"
    READINESS_BLOCKED = "readiness_blocked"
    PACKAGE_VERIFY_FAILED = "package_verify_failed"
    SECRET_EXPOSURE = "secret_exposure"
    POLICY_BYPASS = "policy_bypass"
    PERMISSION_BYPASS = "permission_bypass"
    TOOL_ROUTER_BYPASS = "tool_router_bypass"
    MANIFEST_MISMATCH = "manifest_mismatch"
    RUNTIME_BLOCKED = "runtime_blocked"
    CRITICAL_BLOCKER = "critical_blocker"


@dataclass
class ReleaseBlocker:
    category: ReleaseBlockerCategory
    description: str
    severity: str = "critical"  # critical, high, medium, low

    def to_dict(self) -> dict:
        return {"category": self.category.value, "description": self.description, "severity": self.severity}


@dataclass
class ReleaseCandidate:
    candidate_id: str
    version: str
    created_at: str
    status: ReleaseStatus
    blockers: list[ReleaseBlocker] = field(default_factory=list)
    judge_status: Optional[str] = None
    judge_score: Optional[float] = None
    evals_passed: Optional[int] = None
    evals_total: Optional[int] = None
    evals_score: Optional[float] = None
    readiness_status: Optional[str] = None
    readiness_score: Optional[float] = None
    package_verified: Optional[bool] = None
    package_path: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "version": self.version,
            "created_at": self.created_at,
            "status": self.status.value,
            "blockers": [b.to_dict() for b in self.blockers],
            "judge_status": self.judge_status,
            "judge_score": self.judge_score,
            "evals_passed": self.evals_passed,
            "evals_total": self.evals_total,
            "evals_score": self.evals_score,
            "readiness_status": self.readiness_status,
            "readiness_score": self.readiness_score,
            "package_verified": self.package_verified,
            "package_path": self.package_path,
            "summary": self.summary,
        }


@dataclass
class ReleaseGateResult:
    candidate: ReleaseCandidate
    passed: bool
    errors: list[str] = field(default_factory=list)
