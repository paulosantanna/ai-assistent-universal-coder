from __future__ import annotations

from typing import Any

from aeos.core.evals.eval_models import EvalResult, EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED


class EvalResultValidator:
    def validate(self, result: EvalResult) -> list[str]:
        errors: list[str] = []
        if not result.execution_id:
            errors.append("execution_id is required")
        if not result.suite_id:
            errors.append("suite_id is required")
        if not result.case_id:
            errors.append("case_id is required")
        if result.status not in (EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED):
            errors.append(f"Invalid status: {result.status}")
        if result.score < 0.0 or result.score > 1.0:
            errors.append(f"Score out of range: {result.score}")
        return errors

    def is_valid(self, result: EvalResult) -> bool:
        return len(self.validate(result)) == 0

    def is_critical_failure(self, result: EvalResult) -> bool:
        return result.blocking and result.status in (EVAL_STATUS_FAIL, EVAL_STATUS_ERROR)
