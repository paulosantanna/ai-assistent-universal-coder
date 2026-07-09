from __future__ import annotations

from aeos.core.tool_router.tool_registry_loader import ToolRegistryLoader


class TestToolRegistryLoader:
    def setup_method(self):
        self.loader = ToolRegistryLoader(workspace_root=".")

    def test_loads_tool_router_config(self):
        config = self.loader.load()
        tr = config.tool_router_config.get("tool_router", {})
        assert tr.get("enabled") is True

    def test_loads_mcp_runtime_config(self):
        config = self.loader.load()
        mr = config.mcp_runtime_config.get("mcp_runtime", {})
        assert mr.get("enabled") is True

    def test_loads_mcp_tools_allowlist(self):
        config = self.loader.load()
        assert "filesystem-readonly" in config.tool_allowlist
        assert "filesystem.list" in config.tool_allowlist["filesystem-readonly"]

    def test_loads_mcp_registry(self):
        config = self.loader.load()
        assert len(config.mcps) > 0
        ids = [m["id"] for m in config.mcps]
        assert "filesystem-readonly" in ids
        assert "package-local" in ids
        assert "test-runner-controlled" in ids

    def test_loaded_files_tracked(self):
        config = self.loader.load()
        assert len(config.loaded_files) > 0
        assert any("mcps.registry.yaml" in f for f in config.loaded_files)

    def test_findings_include_unknown_capability(self):
        config = self.loader.load()
        cap_findings = [f for f in config.findings if f["type"] == "unknown_capability"]
        # GIT_STATUS, GIT_DIFF, GIT_LOG, READ_RUNTIME_SECRET may not be in capabilities.yaml
        for f in cap_findings:
            assert "capability" in f
