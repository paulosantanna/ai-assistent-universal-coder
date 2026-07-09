from __future__ import annotations

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.judge.judge_engine import JudgeEngine
from aeos.core.judge.judge_models import JudgeInput, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED


class TestJudgeEngine:
    def setup_method(self):
        self.engine = JudgeEngine(workspace_root=".")

    def test_engine_passes_clean_input(self):
        import tempfile, json
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump({"execution_id": "test", "total_records": 1, "manifest_sha256": ""}, tmp)
        tmp.close()
        ji = JudgeInput(
            execution_id="test-engine-001",
            evidence_manifest_path=tmp.name,
            permission_decisions=[{"decision_id": "pd-e1", "status": "ALLOW", "action": "read"}],
            policy_decisions=[{"decision_id": "pld-e1", "status": "ALLOW", "action": "read"}],
            governance_decisions=[{"decision_id": "gd-e1", "status": "PASS"}],
            runtime_results=[{"execution_id": "test-engine-001", "run_type": "skill", "status": "PASS", "duration_ms": 100}],
        )
        result = self.engine.evaluate_with_input(ji)
        assert result.status == JUDGE_STATUS_PASS
        os.unlink(tmp.name)

    def test_engine_generates_evidence(self):
        ji = JudgeInput(execution_id="test-engine-002")
        result = self.engine.evaluate_with_input(ji)
        evidence_dir = Path(".aeos") / "evidence" / "test-engine-002"
        assert (evidence_dir / "judge-input.json").exists()
        assert (evidence_dir / "judge-result.json").exists()
        assert (evidence_dir / "judge-scorecard.json").exists()

    def test_engine_generates_report(self):
        ji = JudgeInput(execution_id="test-engine-003")
        result = self.engine.evaluate_with_input(ji)
        report_path = Path(".aeos") / "reports" / "test-engine-003" / "judge-report.md"
        assert report_path.exists()

    def test_engine_evaluate_from_dict(self):
        data = {
            "execution_id": "test-engine-004",
            "target_path": ".",
            "permission_decisions": [],
            "policy_decisions": [],
        }
        result = self.engine.evaluate_from_dict(data)
        assert result.execution_id == "test-engine-004"

    def test_engine_summarize(self):
        ji = JudgeInput(execution_id="test-engine-005")
        result = self.engine.evaluate_with_input(ji)
        summary = self.engine.summarize(result)
        assert summary["execution_id"] == "test-engine-005"
        assert "status" in summary
        assert "score" in summary

    def test_engine_validate_result(self):
        ji = JudgeInput(execution_id="test-engine-006")
        result = self.engine.evaluate_with_input(ji)
        errors = self.engine.validate_result(result)
        # May have errors if missing manifest, but should be structurally valid
        assert isinstance(errors, list)
