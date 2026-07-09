from __future__ import annotations

from typing import Any

from aeos.core.readiness.readiness_models import ReadinessResult, ReadinessScorecard


class ReadinessScorecardGenerator:
    def generate(self, result: ReadinessResult) -> ReadinessScorecard:
        category_details: dict[str, dict[str, Any]] = {}
        for cat, score in result.categories.items():
            category_details[cat] = {"score": score}

        critical_blockers = []
        for cb in getattr(result, 'critical_blockers', []):
            critical_blockers.append({"description": cb, "severity": "critical"})

        high_risks = []
        for hr in getattr(result, 'high_risks', []):
            high_risks.append({"description": hr, "severity": "high"})

        medium_risks = []
        for mr in getattr(result, 'medium_risks', []):
            medium_risks.append({"description": mr, "severity": "medium"})

        return ReadinessScorecard(
            execution_id=result.execution_id,
            status=result.status,
            overall_score=result.overall_score,
            categories=dict(result.categories),
            category_details=category_details,
            critical_blockers=critical_blockers,
            high_risks=high_risks,
            medium_risks=medium_risks,
        )
