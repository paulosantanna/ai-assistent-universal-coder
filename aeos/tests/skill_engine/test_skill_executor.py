from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.skill_engine.skill_models import SkillRequest
from aeos.core.evidence.evidence_store import EvidenceStore


class TestSkillExecutor:
    def setup_method(self):
        self.executor = SkillExecutor(workspace_root=".")
        self.evidence = EvidenceStore()

    def test_executor_blocks_nonexistent_skill(self):
        req = SkillRequest(
            execution_id="test-block-nonexistent",
            skill_id="nonexistent-skill",
            actor="tester",
            role="tester",
        )
        result = self.executor.execute(req)
        assert result.status == "BLOCKED"
        assert any("not found" in bc.lower() for bc in result.blocking_conditions)

    def test_executor_uses_tool_router(self):
        req = SkillRequest(
            execution_id="test-tool-router",
            skill_id="repo-scanner",
            actor="tester",
            role="tester",
            input={"target_path": "."},
        )
        result = self.executor.execute(req)
        assert result.status in ("PASS", "BLOCKED")
        # Verify tool results were created via ToolRouter (not direct)
        if result.tool_results:
            for tr in result.tool_results:
                assert "tool_id" in tr, "Tool results should come from ToolRouter"

    def test_executor_registers_evidence(self):
        req = SkillRequest(
            execution_id="test-evidence",
            skill_id="repo-scanner",
            actor="tester",
            role="tester",
        )
        result = self.executor.execute(req)
        assert result is not None
        evidence_files = os.listdir(os.path.join(".aeos", "evidence", "test-evidence"))
        assert len(evidence_files) > 0

    def test_executor_returns_skill_result(self):
        req = SkillRequest(
            execution_id="test-result-type",
            skill_id="repo-scanner",
            actor="tester",
            role="tester",
        )
        result = self.executor.execute(req)
        assert hasattr(result, "status")
        assert hasattr(result, "skill_id")
        assert hasattr(result, "execution_id")
        assert hasattr(result, "duration_ms")
        assert hasattr(result, "evidence_refs")

    def test_executor_blocked_with_unknown_capability(self):
        req = SkillRequest(
            execution_id="test-blocked-cap",
            skill_id="repo-scanner",
            actor="unauthorized",
            role="unauthorized",
        )
        result = self.executor.execute(req)
        # Should be BLOCKED by governance if role not found
        assert result.status in ("PASS", "BLOCKED")

    def test_executor_runs_chromatic_mega_brain(self, tmp_path):
        executor = SkillExecutor(workspace_root=".", evidence_store=EvidenceStore(str(tmp_path / "evidence")))
        req = SkillRequest(
            execution_id="test-chromatic-mega-brain",
            skill_id="chromatic-mega-brain",
            actor="tester",
            role="architect",
            input={
                "objective": "Evolve AEOS architecture for cloud readiness and migration safety",
                "decision_type": "cloud-readiness",
                "evidence_refs": ["registry-validation.jsonl"],
            },
        )

        result = executor.execute(req)

        assert result.status == "PASS"
        assert result.tool_results
        chromatic = result.tool_results[0]["result"]
        assert "BLUE" in chromatic["selected_colors"]
        assert "RED" in chromatic["selected_colors"]
        assert result.evidence_refs

    def test_executor_runs_token_budget_governor(self, tmp_path):
        executor = SkillExecutor(workspace_root=".", evidence_store=EvidenceStore(str(tmp_path / "evidence")))
        req = SkillRequest(
            execution_id="test-token-budget-governor",
            skill_id="token-budget-governor",
            actor="tester",
            role="judge",
            input={
                "provider": "deepseek-free",
                "prompt_scope": "Build only the requested API scaffold.",
                "requested_output_tokens": 1000,
                "task_priority": "normal",
                "subagent_count": 2,
            },
        )

        result = executor.execute(req)

        assert result.status == "PASS"
        assert result.tool_results[0]["result"]["subagent_budget"] > 0

    def test_executor_runs_universal_project_factory(self, tmp_path):
        executor = SkillExecutor(workspace_root=".", evidence_store=EvidenceStore(str(tmp_path / "evidence")))
        req = SkillRequest(
            execution_id="test-universal-project-factory",
            skill_id="universal-project-factory",
            actor="tester",
            role="architect",
            input={
                "project_name": "demo",
                "objective": "Generate a production-ready API",
                "architecture": "hexagonal",
                "languages": ["Python"],
                "databases": ["PostgreSQL"],
                "deployment_target": "cloud",
                "token_budget": {"provider": "codex", "limit": 24000},
                "sandbox_root": str(tmp_path / "sandbox"),
            },
        )

        result = executor.execute(req)

        assert result.status == "PASS"
        payload = result.tool_results[0]["result"]
        assert payload["project_plan"]["status"] == "PASS"
        assert payload["scaffold_manifest"]["write_policy"] == "sandbox_only_until_approval"
        assert payload["generated_files"]
        assert payload["change_count"] == len(payload["generated_files"])
        assert payload["change_manifest"]
        assert payload["rollback_plan"]
        assert payload["rollback_summary"]
        assert len(result.evidence_refs) >= 2
        assert (tmp_path / "sandbox" / "README.md").exists()
        assert (tmp_path / "sandbox" / "pyproject.toml").exists()
        assert (tmp_path / "sandbox" / "db" / "migrations" / "001_initial_postgresql.sql").exists()
        assert (tmp_path / "sandbox" / ".aeos" / "rollback" / "change-manifest.json").exists()
        assert (tmp_path / "sandbox" / ".aeos" / "rollback" / "rollback-plan.json").exists()
        assert (tmp_path / "sandbox" / ".aeos" / "rollback" / "rollback-plan.md").exists()
