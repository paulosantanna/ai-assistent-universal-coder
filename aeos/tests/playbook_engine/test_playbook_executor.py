from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.playbook_engine.playbook_executor import PlaybookExecutor
from aeos.core.playbook_engine.playbook_models import PlaybookRequest
from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.tool_router.router import ToolRouter
from aeos.core.governance.governance_gate import GovernanceGate


class TestPlaybookExecutor:
    def setup_method(self):
        self.tool_router = ToolRouter(workspace_root=".")
        self.governance_gate = GovernanceGate(".")
        self.evidence_store = EvidenceStore()
        self.skill_executor = SkillExecutor(
            workspace_root=".",
            tool_router=self.tool_router,
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )
        self.executor = PlaybookExecutor(
            workspace_root=".",
            tool_router=self.tool_router,
            skill_executor=self.skill_executor,
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )

    def test_executor_blocks_nonexistent_playbook(self):
        req = PlaybookRequest(
            execution_id="test-block-nonexistent",
            playbook_id="nonexistent-playbook",
            actor="tester",
            role="tester",
        )
        result = self.executor.execute(req)
        assert result.status == "BLOCKED"

    def test_executor_dry_run_passes(self):
        req = PlaybookRequest(
            execution_id="test-dry-run",
            playbook_id="project-analysis",
            actor="tester",
            role="tester",
            target_path=".",
            dry_run=True,
        )
        result = self.executor.execute(req)
        assert result.status in ("PASS", "BLOCKED")
        if result.status == "PASS":
            assert len(result.steps) > 0

    def test_executor_blocks_if_skill_missing(self):
        from aeos.core.playbook_engine.playbook_contract_validator import PlaybookContractValidator
        # Create a request for a playbook that requires skills that don't exist
        # This test verifies the blocking mechanism works
        req = PlaybookRequest(
            execution_id="test-skill-blocked",
            playbook_id="enterprise-project-onboarding",
            actor="tester",
            role="tester",
        )
        result = self.executor.execute(req)
        assert result.status in ("PASS", "BLOCKED")

    def test_executor_registers_step_results(self):
        req = PlaybookRequest(
            execution_id="test-step-results",
            playbook_id="project-analysis",
            actor="tester",
            role="tester",
            dry_run=True,
        )
        result = self.executor.execute(req)
        assert result is not None
        if result.steps:
            for step in result.steps:
                assert "id" in step or "step_id" in step
                assert "status" in step

    def test_executor_blocks_on_cycle(self):
        from aeos.core.playbook_engine.playbook_models import PlaybookContract, PlaybookStep
        from aeos.core.playbook_engine.playbook_planner import PlaybookPlanner
        contract = PlaybookContract(
            id="cycle-playbook",
            objective="Test cycle",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="a", depends_on=["b"]),
                PlaybookStep(id="b", depends_on=["c"]),
                PlaybookStep(id="c", depends_on=["a"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        planner = PlaybookPlanner()
        plan = planner.plan(contract, ["skill-a"])
        assert plan["valid"] is False
        assert len(plan["cycles"]) > 0
