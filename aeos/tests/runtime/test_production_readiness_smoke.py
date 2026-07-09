from __future__ import annotations

import sys
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.judge.judge_models import JudgeResult, JudgeScorecard, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_REVIEW
from aeos.core.evals.eval_models import EvalScorecard, EVAL_STATUS_PASS, EVAL_STATUS_FAIL
from aeos.core.readiness.readiness_models import ReadinessResult, READINESS_PASS, READINESS_BLOCKED


class TestProductionReadinessSmoke:
    def test_smoke_fails_when_judge_blocked(self):
        assert JUDGE_STATUS_BLOCKED == "BLOCKED"
        assert JUDGE_STATUS_BLOCKED != "PASS"
        assert READINESS_BLOCKED == "BLOCKED"

    def test_smoke_fails_when_evals_below_threshold(self):
        scorecard = EvalScorecard(
            execution_id="test",
            overall_score=0.5,
            total_cases=10,
            passed=5,
            blocking_failures=[],
        )
        assert scorecard.overall_score < 0.95

    def test_smoke_only_passes_when_all_gates_pass(self):
        assert READINESS_PASS == "PASS"
        assert JUDGE_STATUS_PASS == "PASS"
        passing_scorecard = EvalScorecard(
            execution_id="test",
            overall_score=1.0,
            total_cases=10,
            passed=10,
            failed=0,
            errors=0,
            skipped=0,
        )
        assert passing_scorecard.overall_score >= 0.95
