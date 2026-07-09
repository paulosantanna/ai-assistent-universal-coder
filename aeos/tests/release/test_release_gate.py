import pytest
from aeos.core.release.release_gate import ReleaseGate
from aeos.core.release.release_models import (
    ReleaseCandidate, ReleaseStatus, ReleaseBlocker, ReleaseBlockerCategory,
)


class TestReleaseGate:
    def test_gate_passes_clean_candidate(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PASS,
            judge_status="PASS",
            judge_score=0.98,
            evals_passed=47,
            evals_total=47,
            evals_score=1.0,
            readiness_status="PASS",
            readiness_score=0.99,
            package_verified=True,
            package_path="/tmp/test.zip",
        )
        result = ReleaseGate.evaluate(candidate)
        assert result.passed
        assert len(result.errors) == 0

    def test_gate_blocks_judge_blocked(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PENDING,
            judge_status="BLOCKED",
            judge_score=0.6,
        )
        result = ReleaseGate.evaluate(candidate)
        assert not result.passed
        assert any("Judge" in e for e in result.errors)

    def test_gate_blocks_evals_below_threshold(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PENDING,
            evals_passed=20,
            evals_total=25,
            evals_score=0.80,
        )
        result = ReleaseGate.evaluate(candidate)
        assert not result.passed
        assert any("threshold" in e.lower() for e in result.errors)

    def test_gate_blocks_readiness_blocked(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PENDING,
            readiness_status="BLOCKED",
            readiness_score=0.80,
        )
        result = ReleaseGate.evaluate(candidate)
        assert not result.passed
        assert any("Readiness" in e for e in result.errors)

    def test_gate_blocks_package_verify_failed(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PENDING,
            package_verified=False,
        )
        result = ReleaseGate.evaluate(candidate)
        assert not result.passed
        assert any("Package" in e for e in result.errors)

    def test_gate_can_release_only_when_pass(self):
        good = ReleaseCandidate(
            candidate_id="rc-good",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PASS,
            judge_status="PASS",
            evals_score=1.0,
            readiness_status="PASS",
            package_verified=True,
        )
        good_result = ReleaseGate.evaluate(good)
        assert ReleaseGate.can_release(good_result)

        bad_candidate = ReleaseCandidate(
            candidate_id="rc-bad",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PENDING,
            judge_status="BLOCKED",
        )
        bad_result = ReleaseGate.evaluate(bad_candidate)
        assert not ReleaseGate.can_release(bad_result)
        assert ReleaseGate.is_blocked(bad_result)

    def test_gate_only_passes_when_all_gates_critical_pass(self):
        candidate = ReleaseCandidate(
            candidate_id="rc-test",
            version="1.0.0",
            created_at="2025-01-01T00:00:00",
            status=ReleaseStatus.PASS,
            judge_status="PASS",
            judge_score=0.95,
            evals_passed=47,
            evals_total=47,
            evals_score=1.0,
            readiness_status="PASS",
            readiness_score=0.95,
            package_verified=True,
        )
        result = ReleaseGate.evaluate(candidate)
        assert result.passed
