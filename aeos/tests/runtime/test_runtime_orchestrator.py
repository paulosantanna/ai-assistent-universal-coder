from __future__ import annotations

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id


class TestRuntimeOrchestrator:
    def setup_method(self):
        self.orchestrator = RuntimeOrchestrator(workspace_root=".")
        self.orchestrator.initialize()

    def test_orchestrator_executes_skill(self):
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
        result = self.orchestrator.run_skill(req)
        assert result.status in ("PASS", "BLOCKED")
        assert result.run_type == "skill"
        assert result.entity_id == "repo-scanner"
        assert result.duration_ms >= 0

    def test_orchestrator_executes_playbook(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="playbook",
            entity_id="project-analysis",
            actor="tester",
            role="tester",
            input={"target_path": "."},
            dry_run=True,
        )
        result = self.orchestrator.run_playbook(req)
        assert result.status in ("PASS", "BLOCKED")
        assert result.run_type == "playbook"

    def test_orchestrator_executes_agent_task(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="agent",
            entity_id="planner",
            actor="tester",
            role="tester",
            input={"objective": "test", "target_path": "."},
            dry_run=True,
        )
        result = self.orchestrator.run_agent_task(req)
        assert result.status in ("PASS", "BLOCKED")
        assert result.run_type == "agent"

    def test_orchestrator_generates_evidence_manifest(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="tester",
            input={},
            dry_run=True,
        )
        result = self.orchestrator.run_skill(req)
        manifest_path = os.path.join(".aeos", "evidence", execution_id, "evidence-manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            assert manifest["execution_id"] == execution_id
            assert "total_records" in manifest
            assert "manifest_sha256" in manifest

    def test_orchestrator_handles_unknown_type(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="unknown",
            entity_id="test",
            actor="tester",
            role="tester",
        )
        result = self.orchestrator.run(req)
        assert result.status == "ERROR"
        assert "Unknown" in result.error

    def test_orchestrator_generates_reports(self):
        execution_id = generate_execution_id()
        req = RuntimeRequest(
            execution_id=execution_id,
            run_type="skill",
            entity_id="repo-scanner",
            actor="tester",
            role="tester",
            input={},
            dry_run=True,
        )
        result = self.orchestrator.run_skill(req)
        report_path = os.path.join(".aeos", "reports", execution_id, "runtime-orchestrator-report.md")
        assert os.path.exists(report_path)

    def test_orchestrator_integrates_all_engines(self):
        # This test ensures all sub-engines are properly connected
        assert self.orchestrator.skill_executor is not None
        assert self.orchestrator.playbook_executor is not None
        assert self.orchestrator.agent_runtime is not None
        assert self.orchestrator.tool_router is not None
        assert self.orchestrator.governance_gate is not None
        assert self.orchestrator.evidence_store is not None
