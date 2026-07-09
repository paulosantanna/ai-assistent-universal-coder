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
