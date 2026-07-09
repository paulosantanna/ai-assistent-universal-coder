from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.readiness.readiness_models import (
    ReadinessResult, ReadinessScorecard,
    READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW, READINESS_ERROR,
)
from aeos.core.readiness.readiness_auditor import ReadinessAuditor
from aeos.core.readiness.readiness_scorecard import ReadinessScorecardGenerator
from aeos.core.readiness.readiness_reporter import ReadinessReporter
from aeos.core.evidence.evidence_manifest import StagedManifestBuilder


class ProductionGate:
    MIN_PASS_SCORE = 0.95
    MIN_REVIEW_SCORE = 0.80

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.auditor = ReadinessAuditor(workspace_root)
        self.scorecard_gen = ReadinessScorecardGenerator()
        self.reporter = ReadinessReporter(workspace_root)

    def evaluate(self) -> ReadinessResult:
        result = self.auditor.audit()
        scorecard = self.scorecard_gen.generate(result)
        self._persist(result, scorecard)
        self.reporter.generate_report(result, scorecard)
        self._finalize_readiness_manifest(result.execution_id)
        return result

    def evaluate_with_result(self, result: ReadinessResult) -> bool:
        scorecard = self.scorecard_gen.generate(result)
        self._persist(result, scorecard)
        self.reporter.generate_report(result, scorecard)
        self._finalize_readiness_manifest(result.execution_id)
        return result.status == READINESS_PASS

    def _finalize_readiness_manifest(self, execution_id: str) -> None:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / execution_id
        builder = StagedManifestBuilder(execution_id, str(evidence_dir), str(self.workspace_root))
        builder.finalize_readiness_manifest()

    def can_deploy(self, result: Optional[ReadinessResult] = None) -> bool:
        if result is None:
            result = self.evaluate()
        return (
            result.status == READINESS_PASS
            and result.overall_score >= self.MIN_PASS_SCORE
            and len(result.critical_blockers) == 0
        )

    def is_blocked(self, result: Optional[ReadinessResult] = None) -> bool:
        if result is None:
            result = self.evaluate()
        return result.status in (READINESS_BLOCKED, READINESS_ERROR)

    def _persist(self, result: ReadinessResult, scorecard: ReadinessScorecard) -> None:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / result.execution_id
        evidence_dir.mkdir(parents=True, exist_ok=True)

        fp = evidence_dir / "production-readiness-scorecard.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(scorecard.to_dict(), f, indent=2, default=str)
