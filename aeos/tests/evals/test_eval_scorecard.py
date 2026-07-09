from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.evals.eval_scorecard import EvalScorecardGenerator
from aeos.core.evals.eval_models import EvalResult, EvalScorecard, EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED


class TestEvalScorecard:
    def setup_method(self):
        self.generator = EvalScorecardGenerator()

    def test_generates_scorecard_all_pass(self):
        results = [
            EvalResult(execution_id="e1", suite_id="s1", case_id="c1", status=EVAL_STATUS_PASS, score=1.0),
            EvalResult(execution_id="e1", suite_id="s1", case_id="c2", status=EVAL_STATUS_PASS, score=1.0),
        ]
        sc = self.generator.generate(results)
        assert sc.total_cases == 2
        assert sc.passed == 2
        assert sc.overall_score == 1.0
        assert sc.status == EVAL_STATUS_PASS

    def test_generates_scorecard_with_failures(self):
        results = [
            EvalResult(execution_id="e1", suite_id="s1", case_id="c1", status=EVAL_STATUS_PASS, score=1.0),
            EvalResult(execution_id="e1", suite_id="s1", case_id="c2", status=EVAL_STATUS_FAIL, score=0.0, blocking=True),
        ]
        sc = self.generator.generate(results)
        assert sc.total_cases == 2
        assert sc.passed == 1
        assert sc.failed == 1
        assert sc.overall_score == 0.5
        assert len(sc.blocking_failures) == 1

    def test_generates_suite_scores(self):
        results = [
            EvalResult(execution_id="e1", suite_id="suite_a", case_id="c1", status=EVAL_STATUS_PASS, score=1.0),
            EvalResult(execution_id="e1", suite_id="suite_b", case_id="c2", status=EVAL_STATUS_FAIL, score=0.0),
        ]
        sc = self.generator.generate(results)
        assert "suite_a" in sc.suites
        assert "suite_b" in sc.suites
        assert sc.suites["suite_a"]["score"] == 1.0
        assert sc.suites["suite_b"]["score"] == 0.0

    def test_overall_score_not_1_when_low(self):
        results = [
            EvalResult(execution_id="e1", suite_id="s1", case_id="c1", status=EVAL_STATUS_PASS, score=1.0),
            EvalResult(execution_id="e1", suite_id="s1", case_id="c2", status=EVAL_STATUS_FAIL, score=0.0, blocking=False),
            EvalResult(execution_id="e1", suite_id="s1", case_id="c3", status=EVAL_STATUS_SKIPPED, score=0.0, blocking=False),
            EvalResult(execution_id="e1", suite_id="s1", case_id="c4", status=EVAL_STATUS_ERROR, score=0.0, blocking=False),
        ]
        sc = self.generator.generate(results)
        assert sc.overall_score == 0.25
        assert sc.overall_score < 1.0
