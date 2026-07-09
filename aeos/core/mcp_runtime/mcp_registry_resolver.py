from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.mcp_runtime.mcp_models import MCPEntry, MCPValidationFinding, MCPValidationReport
from aeos.core.mcp_runtime.mcp_security_validator import MCPSecurityValidator


DANGEROUS_COMMANDS = {
    "rm", "del", "format", "sudo", "curl", "wget",
    "shred", "dd", "mkfs", "fdisk", "chmod", "chown",
}

DANGEROUS_KEYWORDS = {
    "browser", "cookies", "auth", "secret", "credential",
    "password", "token", "key", "certificate",
}


class MCPRegistryResolver:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._entries: dict[str, MCPEntry] = {}
        self._allowlist: dict[str, set[str]] = {}
        self.security_validator = MCPSecurityValidator()

    def load(self) -> MCPValidationReport:
        report = MCPValidationReport()
        registry_path = self.workspace_root / "aeos" / "registries" / "mcps.registry.yaml"

        if not registry_path.exists():
            report.blocked += 1
            report.findings.append(MCPValidationFinding(
                mcp_id="*",
                finding_type="registry_not_found",
                severity="critical",
                detail=f"MCP registry not found: {registry_path}",
            ))
            return report

        with open(registry_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        for entry in raw.get("mcps", []):
            mcp_id = entry.get("id", "unknown")
            mcp = MCPEntry(
                id=mcp_id,
                type=entry.get("type", "unknown"),
                transport=entry.get("transport", "stdio"),
                config_path=entry.get("config", ""),
                risk_level=entry.get("risk_level", "low"),
                capabilities=entry.get("capabilities", []),
                tools=entry.get("tools", []),
                enabled=entry.get("enabled", True),
                approval_required=entry.get("approval_required", False),
                write_allowed=entry.get("write_allowed", False),
                sandbox_required=entry.get("sandbox_required", False),
                allowlist_required=entry.get("allowlist_required", False),
                reason=entry.get("reason", ""),
            )
            self._entries[mcp_id] = mcp
            self._allowlist[mcp_id] = set(entry.get("tools", []))

        self._validate_all(report)

        return report

    def _validate_all(self, report: MCPValidationReport):
        allowlist_path = self.workspace_root / "aeos" / "config" / "mcp-tools.allowlist.yaml"
        allowlist = {}
        if allowlist_path.exists():
            with open(allowlist_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            allowlist = data.get("allowlist", {})

        caps_path = self.workspace_root / "aeos" / "config" / "capabilities.yaml"
        known_caps = set()
        if caps_path.exists():
            with open(caps_path, "r", encoding="utf-8") as f:
                caps_data = yaml.safe_load(f) or {}
            known_caps = set(caps_data.get("capabilities", []))

        for mcp in self._entries.values():
            report.mcps_validated += 1
            findings = self.security_validator.validate(mcp, allowlist, known_caps)
            for f in findings:
                report.findings.append(f)

        passed = 0
        blocked = 0
        seen_ids = set()
        for finding in report.findings:
            if finding.severity == "critical":
                if finding.mcp_id not in seen_ids:
                    blocked += 1
                    seen_ids.add(finding.mcp_id)

        report.passed = report.mcps_validated - blocked
        report.blocked = blocked

    def resolve(self, mcp_id: str) -> Optional[MCPEntry]:
        return self._entries.get(mcp_id)

    def is_tool_allowed(self, mcp_id: str, tool_name: str) -> bool:
        allowed = self._allowlist.get(mcp_id)
        if allowed is None:
            return False
        return tool_name in allowed

    def list_enabled(self) -> list[dict]:
        return [e.to_dict() for e in self._entries.values() if e.enabled]

    def generate_risk_report(self, execution_id: str, report: MCPValidationReport) -> str:
        out_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        out_dir.mkdir(parents=True, exist_ok=True)

        lines = [
            "# MCP Risk Report",
            f"",
            f"- **Execution ID**: {execution_id}",
            f"- **MCPs Validated**: {report.mcps_validated}",
            f"- **PASS**: {report.passed}",
            f"- **BLOCKED**: {report.blocked}",
            f"",
            "## Findings",
            f"",
            "| MCP ID | Type | Severity | Detail |",
            "|--------|------|----------|--------|",
        ]
        for finding in report.findings:
            lines.append(f"| {finding.mcp_id} | {finding.finding_type} | {finding.severity} | {finding.detail} |")

        lines.extend([
            f"",
            "## Registered MCPs",
            f"",
            "| ID | Type | Risk | Enabled | Tools |",
            "|----|------|------|---------|-------|",
        ])
        for entry in self._entries.values():
            tools = ", ".join(entry.tools)
            lines.append(f"| {entry.id} | {entry.type} | {entry.risk_level} | {entry.enabled} | {tools} |")

        content = "\n".join(lines)
        fp = out_dir / "mcp-risk-report.md"
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return str(fp)
