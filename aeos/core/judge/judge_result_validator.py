from __future__ import annotations

from typing import Any

from aeos.core.judge.judge_models import JudgeResult, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW


class JudgeResultValidator:
    def validate(self, result: JudgeResult) -> list[str]:
        errors: list[str] = []
        if not result.execution_id:
            errors.append("execution_id is required")
        if result.status not in (JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW):
            errors.append(f"Invalid status: {result.status}")
        if result.score < 0.0 or result.score > 1.0:
            errors.append(f"Score out of range [0,1]: {result.score}")
        if result.status == JUDGE_STATUS_PASS and result.score < 0.95:
            errors.append(f"PASS status but score {result.score} < 0.95")
        if result.status == JUDGE_STATUS_REVIEW and result.score < 0.80:
            errors.append(f"REVIEW status but score {result.score} < 0.80")
        if result.status == JUDGE_STATUS_BLOCKED and not result.blocking_rules:
            errors.append("BLOCKED status but no blocking_rules")
        if result.status == JUDGE_STATUS_PASS and result.blocking_rules:
            critical = [r for r in result.blocking_rules if r in (
                "missing_evidence_manifest", "manifest_hash_mismatch",
                "permission_denied", "policy_denied", "governance_blocked",
                "tool_router_bypass", "secret_exposed", "unsupported_claim",
            )]
            if critical:
                errors.append(f"PASS status but has critical blocking_rules: {critical}")
        return errors

    def is_valid(self, result: JudgeResult) -> bool:
        return len(self.validate(result)) == 0
