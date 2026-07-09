from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.judge.judge_scorecard import JudgeScorecardGenerator
from aeos.core.judge.judge_models import JudgeResult, JudgeScorecard, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_REVIEW


class TestJudgeScorecard:
    def setup_method(self):
        self.generator = JudgeScorecardGenerator()

    def test_generates_scorecard(self):
        result = JudgeResult(
            execution_id="test-sc-001",
            status=JUDGE_STATUS_PASS,
            score=0.98,
        )
        scorecard = self.generator.generate(result)
        assert scorecard.execution_id == "test-sc-001"
        assert scorecard.status == JUDGE_STATUS_PASS
        assert scorecard.overall_score == 0.98

    def test_scorecard_has_categories(self):
        result = JudgeResult(
            execution_id="test-sc-002",
            status=JUDGE_STATUS_BLOCKED,
            score=0.4,
            blocking_rules=["permission_denied"],
        )
        scorecard = self.generator.generate(result)
        assert isinstance(scorecard.categories, dict)
        assert "permissions" in scorecard.categories

    def test_scorecard_critical_blockers(self):
        result = JudgeResult(
            execution_id="test-sc-003",
            status=JUDGE_STATUS_BLOCKED,
            score=0.3,
            blocking_rules=["permission_denied", "secret_exposed"],
        )
        scorecard = self.generator.generate(result)
        assert len(scorecard.critical_blockers) == 2

    def test_scorecard_warnings(self):
        result = JudgeResult(
            execution_id="test-sc-004",
            status=JUDGE_STATUS_REVIEW,
            score=0.85,
            warnings=["unsupported_claim: Missing evidence"],
        )
        scorecard = self.generator.generate(result)
        assert len(scorecard.warnings) == 1
