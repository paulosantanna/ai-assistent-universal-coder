from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.readiness.production_gate import ProductionGate
from aeos.core.readiness.readiness_models import ReadinessResult, READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW


class TestProductionGate:
    def setup_method(self):
        self.gate = ProductionGate(workspace_root=".")

    def test_evaluate_returns_result(self):
        result = self.gate.evaluate()
        assert result.execution_id is not None
        assert result.status in (READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW, "ERROR")

    def test_can_deploy_false_if_blocked(self):
        blocked_result = ReadinessResult(
            execution_id="test-blocked",
            status=READINESS_BLOCKED,
            overall_score=0.5,
            critical_blockers=["missing_critical_module"],
        )
        can_deploy = self.gate.can_deploy(blocked_result)
        assert can_deploy is False

    def test_can_deploy_false_if_critical_blockers(self):
        result = ReadinessResult(
            execution_id="test-critical",
            status=READINESS_PASS,
            overall_score=0.98,
            critical_blockers=["critical_blocker_present"],
        )
        assert self.gate.can_deploy(result) is False

    def test_can_deploy_false_if_low_score(self):
        result = ReadinessResult(
            execution_id="test-low-score",
            status=READINESS_PASS,
            overall_score=0.80,
            critical_blockers=[],
        )
        assert self.gate.can_deploy(result) is False

    def test_can_deploy_true_if_passing(self):
        passing_result = ReadinessResult(
            execution_id="test-pass",
            status=READINESS_PASS,
            overall_score=0.98,
            critical_blockers=[],
            categories={
                "architecture": 1.0,
                "security": 1.0,
                "evidence_integrity": 1.0,
                "tests": 1.0,
                "production_safety": 0.95,
            },
        )
        can_deploy = self.gate.can_deploy(passing_result)
        assert can_deploy is True

    def test_is_blocked(self):
        blocked_result = ReadinessResult(
            execution_id="test-blocked",
            status=READINESS_BLOCKED,
            overall_score=0.5,
        )
        assert self.gate.is_blocked(blocked_result) is True

    def test_is_blocked_false_for_pass(self):
        passing = ReadinessResult(
            execution_id="test-pass",
            status=READINESS_PASS,
            overall_score=0.98,
        )
        assert self.gate.is_blocked(passing) is False

    def test_persists_scorecard(self):
        result = self.gate.evaluate()
        import json
        from pathlib import Path
        fp = Path(".aeos") / "evidence" / result.execution_id / "production-readiness-scorecard.json"
        assert fp.exists(), f"Scorecard not found at {fp}"
