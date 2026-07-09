from pathlib import Path
from typing import Optional
from aeos.core.release.release_models import (
    ReleaseCandidate, ReleaseStatus, ReleaseGateResult, ReleaseBlocker, ReleaseBlockerCategory,
)
from aeos.core.packaging.package_verifier import PackageVerifier


class ReleaseGate:

    MIN_EVALS_SCORE = 0.95
    CRITICAL_CATEGORIES = {
        ReleaseBlockerCategory.JUDGE_BLOCKED,
        ReleaseBlockerCategory.READINESS_BLOCKED,
        ReleaseBlockerCategory.EVALS_BELOW_THRESHOLD,
        ReleaseBlockerCategory.PACKAGE_VERIFY_FAILED,
        ReleaseBlockerCategory.RUNTIME_BLOCKED,
        ReleaseBlockerCategory.SECRET_EXPOSURE,
        ReleaseBlockerCategory.CRITICAL_BLOCKER,
    }

    @staticmethod
    def evaluate(candidate: ReleaseCandidate) -> ReleaseGateResult:
        errors: list[str] = []

        if candidate.judge_status == "BLOCKED":
            errors.append(f"Judge BLOCKED (score={candidate.judge_score})")
        if candidate.evals_score is not None and candidate.evals_score < ReleaseGate.MIN_EVALS_SCORE:
            errors.append(f"Evals below threshold: {candidate.evals_score:.4f} < {ReleaseGate.MIN_EVALS_SCORE}")
        if candidate.readiness_status == "BLOCKED":
            errors.append(f"Readiness BLOCKED (score={candidate.readiness_score})")
        if candidate.package_verified is False:
            errors.append("Package verification failed")
        if not candidate.package_verified and candidate.package_path:
            errors.append("Package not verified")

        for blocker in candidate.blockers:
            if blocker.category in ReleaseGate.CRITICAL_CATEGORIES and blocker.severity == "critical":
                if blocker.description not in errors:
                    errors.append(blocker.description)

        passed = len(errors) == 0 and candidate.status in (ReleaseStatus.PASS, ReleaseStatus.REVIEW)

        if passed and candidate.status == ReleaseStatus.PASS:
            candidate.status = ReleaseStatus.PASS
        elif not passed:
            candidate.status = ReleaseStatus.BLOCKED
            if not errors:
                errors.append("Release gate evaluation failed")

        return ReleaseGateResult(
            candidate=candidate,
            passed=passed,
            errors=errors,
        )

    @staticmethod
    def can_release(result: ReleaseGateResult) -> bool:
        return result.passed and result.candidate.status == ReleaseStatus.PASS

    @staticmethod
    def is_blocked(result: ReleaseGateResult) -> bool:
        return result.candidate.status == ReleaseStatus.BLOCKED or not result.passed
