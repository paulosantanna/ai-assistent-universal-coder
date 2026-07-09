from __future__ import annotations

from typing import Any

from aeos.core.judge.judge_models import JudgeResult, JudgeScorecard, JudgeStatus
from aeos.core.judge.judge_blocking_rules import get_category, get_severity


class JudgeScorecardGenerator:
    def generate(self, result: JudgeResult) -> JudgeScorecard:
        categories: dict[str, list[dict]] = {}
        for rule_id in result.blocking_rules:
            cat = get_category(rule_id)
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                "rule_id": rule_id,
                "status": "FAIL",
                "severity": get_severity(rule_id),
            })

        category_scores: dict[str, float] = {}
        for cat, cat_findings in categories.items():
            failures = len(cat_findings)
            category_scores[cat] = max(0.0, 1.0 - (failures * 0.1))

        # Ensure all known categories are present even if empty
        from aeos.core.judge.judge_blocking_rules import BLOCKING_RULES_REGISTRY
        all_cats = set(r.category for r in BLOCKING_RULES_REGISTRY.values())
        for cat in all_cats:
            if cat not in category_scores:
                category_scores[cat] = 1.0

        findings_flat: list[dict[str, Any]] = []
        for cat_findings in categories.values():
            findings_flat.extend(cat_findings)

        critical_blockers = list(result.blocking_rules)

        return JudgeScorecard(
            execution_id=result.execution_id,
            status=result.status,
            overall_score=result.score,
            categories=category_scores,
            findings=findings_flat,
            critical_blockers=critical_blockers,
            warnings=list(result.warnings),
        )
