from __future__ import annotations

import sys
import os
import json
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.judge.deterministic_judge import DeterministicJudge
from aeos.core.judge.judge_models import (
    JudgeInput, JudgeResult,
    JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW,
)
from aeos.core.judge.judge_blocking_rules import get_rule, is_critical, CRITICAL_RULES


class TestDeterministicJudge:
    def setup_method(self):
        self.judge = DeterministicJudge(workspace_root=".")
        self.base_input = JudgeInput(
            execution_id="test-judge-001",
            target_path=".",
            evidence_manifest_path="",
        )

    def test_blocked_missing_evidence_manifest(self):
        result = self.judge.evaluate(self.base_input)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "missing_evidence_manifest" in result.blocking_rules

    def test_blocked_permission_denied(self):
        ji = JudgeInput(
            execution_id="test-judge-002",
            permission_decisions=[
                {"decision_id": "pd-001", "status": "DENY", "action": "write-file", "actor": "tester"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "permission_denied" in result.blocking_rules

    def test_blocked_policy_denied(self):
        ji = JudgeInput(
            execution_id="test-judge-003",
            policy_decisions=[
                {"decision_id": "pd-002", "status": "DENY", "action": "git-merge", "reason": "policy:merge"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "policy_denied" in result.blocking_rules

    def test_blocked_governance_blocked(self):
        ji = JudgeInput(
            execution_id="test-judge-004",
            governance_decisions=[
                {"decision_id": "gd-001", "status": "BLOCKED", "blocking_reasons": ["permission denied"]},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "governance_blocked" in result.blocking_rules

    def test_blocked_tool_router_bypass(self):
        ji = JudgeInput(
            execution_id="test-judge-005",
            tool_results=[
                {"tool_id": "shell", "status": "BLOCKED", "error": "bypass detected", "decision_id": "td-001"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "tool_router_bypass" in result.blocking_rules

    def test_blocked_secret_exposure(self):
        ji = JudgeInput(
            execution_id="test-judge-006",
            tool_results=[
                {"tool_id": "search", "status": "PASS", "output": {"content": "API key: sk-1234"}, "result_id": "tr-001"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_BLOCKED
        assert "secret_exposed" in result.blocking_rules

    def test_blocked_unsupported_claim(self):
        ji = JudgeInput(
            execution_id="test-judge-007",
            claims=[
                {"claim": "This is a claim without evidence", "evidence_refs": []},
            ],
        )
        result = self.judge.evaluate(ji)
        assert "unsupported_claim" in result.blocking_rules or len(result.claims_rejected) > 0

    def test_blocked_package_verify_failed(self):
        ji = JudgeInput(
            execution_id="test-judge-008",
            package_refs=[
                {"path": "malicious.zip", "verified": False, "package_id": "pkg-001"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert "package_verify_failed" in result.blocking_rules

    def test_blocked_approval_wildcard(self):
        ji = JudgeInput(
            execution_id="test-judge-009",
            approval_refs=[
                {"approval_id": "app-001", "status": "APPROVED", "pattern": "*"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert "approval_wildcard" in result.blocking_rules

    def test_passes_with_clean_input(self):
        import tempfile
        tmp_manifest = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        import json
        json.dump({"execution_id": "test", "total_records": 1, "manifest_sha256": ""}, tmp_manifest)
        tmp_manifest.close()
        ji = JudgeInput(
            execution_id="test-judge-010",
            evidence_manifest_path=tmp_manifest.name,
            permission_decisions=[
                {"decision_id": "pd-010", "status": "ALLOW", "action": "read-file", "actor": "tester"},
            ],
            policy_decisions=[
                {"decision_id": "pld-010", "status": "ALLOW", "action": "read-file"},
            ],
            governance_decisions=[
                {"decision_id": "gd-010", "status": "PASS"},
            ],
            tool_results=[
                {"tool_id": "filesystem", "status": "PASS", "output": {"content": "ok"}, "result_id": "tr-010"},
            ],
            skill_results=[
                {"skill_id": "scanner", "status": "PASS", "request_id": "sr-001"},
            ],
            runtime_results=[
                {"execution_id": "test-judge-010", "run_type": "skill", "status": "PASS", "duration_ms": 100},
            ],
        )
        result = self.judge.evaluate(ji)
        assert result.status == JUDGE_STATUS_PASS
        assert len(result.blocking_rules) == 0
        assert result.score >= 0.95
        os.unlink(tmp_manifest.name)

    def test_blocking_rules_registry(self):
        assert "missing_evidence_manifest" in CRITICAL_RULES
        assert "permission_denied" in CRITICAL_RULES
        assert "policy_denied" in CRITICAL_RULES
        assert "secret_exposed" in CRITICAL_RULES
        assert get_rule("secret_exposed") is not None
        assert is_critical("missing_evidence_manifest") is True
        assert is_critical("unsupported_claim") is False

    def test_blocked_runtime_error(self):
        ji = JudgeInput(
            execution_id="test-judge-011",
            tool_results=[
                {"tool_id": "processor", "status": "ERROR", "error": "out of memory", "result_id": "tr-011"},
            ],
        )
        result = self.judge.evaluate(ji)
        assert "runtime_error" in result.blocking_rules

    def test_score_below_095_with_warnings(self):
        ji = JudgeInput(
            execution_id="test-judge-012",
            claims=[{"claim": "Performance is good", "evidence_refs": []}],
        )
        result = self.judge.evaluate(ji)
        assert result.score < 0.95 or result.status == JUDGE_STATUS_REVIEW
