from __future__ import annotations

from aeos.core.mcp_runtime.mcp_models import MCPEntry
from aeos.core.mcp_runtime.mcp_security_validator import MCPSecurityValidator


class TestMCPSecurityValidator:
    def setup_method(self):
        self.validator = MCPSecurityValidator()
        self.known_caps = {"READ_FILES", "LIST_DIRECTORIES", "WRITE_SANDBOX_FILES", "RUN_TESTS"}
        self.allowlist = {
            "test-safe": ["tool.one", "tool.two"],
            "test-critical": ["critical.tool"],
            "test-unknown-cap": ["tool.x"],
            "secrets-runtime": [],
        }

    def _make_mcp(self, **kwargs) -> MCPEntry:
        defaults = {
            "id": "test-mcp", "type": "generic", "transport": "stdio",
            "config_path": "", "risk_level": "low",
            "capabilities": ["READ_FILES"], "tools": ["tool.one"],
            "enabled": True, "approval_required": False,
        }
        defaults.update(kwargs)
        return MCPEntry(**defaults)

    def test_valid_mcp_no_findings(self):
        mcp = self._make_mcp(id="test-safe")
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert len(findings) == 0

    def test_block_critical_enabled_default(self):
        mcp = self._make_mcp(id="test-critical", risk_level="critical", enabled=True)
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert any(f.finding_type == "critical_mcp_enabled_default" for f in findings)

    def test_block_unknown_capability(self):
        mcp = self._make_mcp(id="test-unknown-cap", capabilities=["UNKNOWN_CAP"])
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert any(f.finding_type == "unknown_capability" for f in findings)

    def test_block_disabled_mcp_type(self):
        mcp = self._make_mcp(id="secrets-runtime", type="secrets-runtime", enabled=True)
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert any(f.finding_type == "disabled_mcp_type_enabled" for f in findings)

    def test_block_unrestricted_shell(self):
        mcp = self._make_mcp(id="shell-danger", type="shell-unrestricted", enabled=True)
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert any(f.finding_type == "unrestricted_shell" for f in findings)

    def test_detect_dangerous_name(self):
        mcp = self._make_mcp(id="browser-auth-cookies", type="generic")
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        browser_findings = [f for f in findings if f.finding_type == "dangerous_mcp_name"]
        assert len(browser_findings) > 0

    def test_detect_dangerous_config_path(self):
        mcp = self._make_mcp(id="test-unsafe", config_path="aeos/mcps/secrets-runtime.mcp.yaml")
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        browser_findings = [f for f in findings if f.finding_type == "dangerous_config_path"]
        assert len(browser_findings) > 0

    def test_medium_severity_for_unlisted_tool(self):
        mcp = self._make_mcp(id="test-safe", tools=["tool.three"])
        findings = self.validator.validate(mcp, self.allowlist, self.known_caps)
        assert any(f.finding_type == "tool_not_in_allowlist" for f in findings)
