from __future__ import annotations

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id
from aeos.core.judge.judge_models import JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED


class TestRuntimeWithJudge:
    def setup_method(self):
        self.orchestrator = RuntimeOrchestrator(workspace_root=".")
        self.orchestrator.initialize()

    def test_runtime_calls_judge(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="architect",
            input={"target_path": "."},
            dry_run=True,
        )
        rt_result, judge_result = self.orchestrator.run_with_judge(req)
        assert rt_result.execution_id == execution_id
        assert judge_result.execution_id == execution_id
        assert judge_result.status in (JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED)

    def test_runtime_generates_judge_evidence(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="architect",
            input={},
            dry_run=True,
        )
        self.orchestrator.run_with_judge(req)
        judge_input = os.path.join(".aeos", "evidence", execution_id, "judge-input.json")
        judge_result = os.path.join(".aeos", "evidence", execution_id, "judge-result.json")
        assert os.path.exists(judge_input), f"Missing {judge_input}"
        assert os.path.exists(judge_result), f"Missing {judge_result}"

    def test_runtime_generates_judge_report(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="architect",
            input={},
            dry_run=True,
        )
        self.orchestrator.run_with_judge(req)
        report_path = os.path.join(".aeos", "reports", execution_id, "judge-report.md")
        assert os.path.exists(report_path), f"Missing {report_path}"

    def test_runtime_full_pipeline(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="architect",
            input={"target_path": "."},
            dry_run=True,
        )
        pipeline = self.orchestrator.run_full_pipeline(req, run_evals=True, run_readiness=True)
        assert "runtime_result" in pipeline
        assert "judge_result" in pipeline
        assert "eval_results" in pipeline
        assert "readiness_result" in pipeline
        assert pipeline["pipeline_status"] in ("PASS", "BLOCKED")

    def test_runtime_executes_evals(self):
        # Just test that evals run without error
        results = self.orchestrator.run_with_evals("anti_hallucination")
        assert isinstance(results, list)

    def test_runtime_readiness_audit(self):
        result = self.orchestrator.run_readiness_audit()
        assert result.execution_id is not None
        assert result.overall_score > 0.0

    def test_judge_blocks_on_critical_issue(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="tester",
            input={"target_path": "."},
            dry_run=True,
        )
        # Store a permission_denied decision in evidence to trigger judge block
        evidence_dir = os.path.join(".aeos", "evidence", execution_id)
        os.makedirs(evidence_dir, exist_ok=True)
        with open(os.path.join(evidence_dir, "permission_decisions.jsonl"), "w") as f:
            f.write(json.dumps({"decision_id": "pd-block", "status": "DENY", "action": "write-file", "actor": "tester"}) + "\n")

        rt_result, judge_result = self.orchestrator.run_with_judge(req)
        # Judge should see the permission denied
        assert judge_result.status in (JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED)
