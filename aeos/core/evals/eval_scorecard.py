from __future__ import annotations

from typing import Any

from aeos.core.evals.eval_models import EvalResult, EvalScorecard, EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR


class EvalScorecardGenerator:
    def generate(self, results: list[EvalResult]) -> EvalScorecard:
        suites: dict[str, dict[str, Any]] = {}
        blocking_failures: list[str] = []
        total_cases = len(results)
        passed = sum(1 for r in results if r.status == EVAL_STATUS_PASS)
        failed = sum(1 for r in results if r.status == EVAL_STATUS_FAIL)
        errors = sum(1 for r in results if r.status == EVAL_STATUS_ERROR)
        skipped = sum(1 for r in results if r.status not in (EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR))

        for r in results:
            if r.suite_id not in suites:
                suites[r.suite_id] = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0, "score": 0.0}
            s = suites[r.suite_id]
            s["total"] += 1
            if r.status == EVAL_STATUS_PASS:
                s["passed"] += 1
            elif r.status == EVAL_STATUS_FAIL:
                s["failed"] += 1
                if r.blocking:
                    blocking_failures.append(f"{r.suite_id}/{r.case_id}")
            elif r.status == EVAL_STATUS_ERROR:
                s["errors"] += 1
            else:
                s["skipped"] += 1

        for sid, s in suites.items():
            s["score"] = s["passed"] / max(s["total"], 1)

        overall_score = passed / max(total_cases, 1)
        status = EVAL_STATUS_FAIL if blocking_failures else EVAL_STATUS_PASS

        return EvalScorecard(
            execution_id=results[0].execution_id if results else "unknown",
            suites=suites,
            overall_score=overall_score,
            total_cases=total_cases,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            blocking_failures=blocking_failures,
            status=status,
        )
