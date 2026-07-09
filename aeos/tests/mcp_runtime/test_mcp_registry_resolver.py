from __future__ import annotations

import json
from pathlib import Path

from aeos.core.mcp_runtime.mcp_registry_resolver import MCPRegistryResolver


EXECUTION_ID = "test-mcp-resolver-001"


class TestMCPRegistryResolver:
    def setup_method(self):
        self.resolver = MCPRegistryResolver(workspace_root=".")

    def test_loads_all_mcps(self):
        report = self.resolver.load()
        assert report.mcps_validated > 0
        assert len(self.resolver._entries) > 0

    def test_resolves_known_mcp(self):
        self.resolver.load()
        mcp = self.resolver.resolve("filesystem-readonly")
        assert mcp is not None
        assert mcp.type == "filesystem"

    def test_resolves_unknown_mcp(self):
        self.resolver.load()
        mcp = self.resolver.resolve("nonexistent")
        assert mcp is None

    def test_is_tool_allowed(self):
        self.resolver.load()
        assert self.resolver.is_tool_allowed("filesystem-readonly", "filesystem.list") is True
        assert self.resolver.is_tool_allowed("filesystem-readonly", "nonexistent") is False

    def test_list_enabled(self):
        self.resolver.load()
        enabled = self.resolver.list_enabled()
        ids = [e["id"] for e in enabled]
        assert "filesystem-readonly" in ids
        # secrets-runtime is disabled
        assert "secrets-runtime" not in ids

    def test_secrets_runtime_disabled(self):
        self.resolver.load()
        mcp = self.resolver.resolve("secrets-runtime")
        assert mcp is not None
        assert mcp.enabled is False

    def test_generates_risk_report(self):
        report = self.resolver.load()
        path = self.resolver.generate_risk_report(EXECUTION_ID, report)
        assert Path(path).exists()
        content = Path(path).read_text(encoding="utf-8")
        assert "MCP Risk Report" in content
        assert "filesystem-readonly" in content

    def test_validation_findings(self):
        report = self.resolver.load()
        assert len(report.findings) > 0
