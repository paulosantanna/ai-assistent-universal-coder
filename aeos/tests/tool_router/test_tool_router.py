from __future__ import annotations

from aeos.core.tool_router.router import ToolRouter, register_adapter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.tool_router.adapters.filesystem_readonly_adapter import FilesystemReadonlyAdapter
from aeos.core.tool_router.adapters.filesystem_sandbox_write_adapter import FilesystemSandboxWriteAdapter
from aeos.core.tool_router.adapters.package_local_adapter import PackageLocalAdapter
from aeos.core.tool_router.adapters.test_runner_mock_adapter import TestRunnerMockAdapter
from aeos.core.evidence.evidence_store import EvidenceStore


EXECUTION_ID = "test-tool-router-001"


class TestToolRouter:
    def setup_method(self):
        register_adapter("filesystem-readonly", FilesystemReadonlyAdapter)
        register_adapter("filesystem-write-sandbox", FilesystemSandboxWriteAdapter)
        register_adapter("package-local", PackageLocalAdapter)
        register_adapter("test-runner-controlled", TestRunnerMockAdapter)

        self.evidence = EvidenceStore()
        self.router = ToolRouter(workspace_root=".", evidence_store=self.evidence)
        self.router.initialize()
        self.router.register_adapter_instance("filesystem-readonly", FilesystemReadonlyAdapter())
        self.router.register_adapter_instance("filesystem-write-sandbox", FilesystemSandboxWriteAdapter())
        self.router.register_adapter_instance("package-local", PackageLocalAdapter())
        self.router.register_adapter_instance("test-runner-controlled", TestRunnerMockAdapter())

    def test_block_unknown_tool(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="tester", role="tester",
            tool_id="unknown-tool", action="filesystem.read",
            capability="READ_FILES", resource="test.txt",
        )
        result = self.router.route(req)
        assert result.status == "BLOCKED"
        assert "unknown" in (result.error or "").lower()

    def test_block_action_without_capability(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="tester", role="tester",
            tool_id="filesystem-readonly", action="filesystem.read",
            capability="NONEXISTENT", resource="test.txt",
        )
        result = self.router.route(req)
        assert result.status == "BLOCKED"

    def test_block_policy_denied(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="coder", role="coder",
            tool_id="filesystem-write-sandbox", action="filesystem.write",
            capability="WRITE_SANDBOX_FILES", resource="outside.txt",
        )
        result = self.router.route(req)
        assert result.status == "BLOCKED"

    def test_allow_readonly_with_permission(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="architect", role="architect",
            tool_id="filesystem-readonly", action="filesystem.exists",
            capability="READ_FILES", resource="aeos/config",
        )
        result = self.router.route(req)
        assert result.status == "PASS"
        assert result.output.get("exists") is True

    def test_allow_sandbox_write(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="coder", role="coder",
            tool_id="filesystem-write-sandbox", action="filesystem.write_sandbox",
            capability="WRITE_SANDBOX_FILES", resource="test_write.txt",
            input={"content": "hello"},
        )
        result = self.router.route(req)
        assert result.status == "PASS"
        assert result.output.get("written") is True

    def test_block_write_outside_sandbox(self):
        adapter = FilesystemSandboxWriteAdapter(sandbox_base=".aeos/sandbox")
        self.router.register_adapter_instance("filesystem-write-sandbox", adapter)
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="coder", role="coder",
            tool_id="filesystem-write-sandbox", action="filesystem.write_sandbox",
            capability="WRITE_SANDBOX_FILES", resource="../outside.txt",
            input={"content": "blocked"},
        )
        result = self.router.route(req)
        assert result.status == "PASS"
        assert "outside sandbox" in (result.output.get("error", "") or "").lower()

    def test_evidence_stored(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="architect", role="architect",
            tool_id="filesystem-readonly", action="filesystem.list",
            capability="LIST_DIRECTORIES", resource="aeos/config",
        )
        self.router.route(req)
        assert len(self.router.get_decisions()) > 0
        assert len(self.router.get_results()) > 0

    def test_tool_result_has_required_fields(self):
        req = ToolRequest(
            execution_id=EXECUTION_ID, actor="tester", role="tester",
            tool_id="filesystem-readonly", action="filesystem.list",
            capability="READ_FILES", resource="aeos/config",
        )
        result = self.router.route(req)
        assert result.execution_id == EXECUTION_ID
        assert result.tool_id == "filesystem-readonly"
        assert result.status in ("PASS", "BLOCKED", "ERROR", "WAITING_APPROVAL")
