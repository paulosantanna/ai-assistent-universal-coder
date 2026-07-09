from __future__ import annotations

from pathlib import Path
from typing import Any

from aeos.core.mcp_runtime.mcp_models import MCPEntry, MCPValidationFinding


DANGEROUS_COMMANDS = {
    "rm", "del", "sudo", "curl", "wget",
    "shred", "dd", "mkfs", "fdisk",
}

DANGEROUS_KEYWORDS = {
    "browser", "cookie", "auth", "credential",
    "password", "token", "key", "certificate", "secret",
}

DISABLED_MCP_TYPES = {
    "secrets-runtime", "browser-authenticated", "database-write",
    "cloud-write", "deploy", "shell-unrestricted",
}


class MCPSecurityValidator:
    def validate(
        self,
        mcp: MCPEntry,
        allowlist: dict[str, list[str]],
        known_caps: set[str],
    ) -> list[MCPValidationFinding]:
        findings: list[MCPValidationFinding] = []

        if mcp.enabled and mcp.type in DISABLED_MCP_TYPES:
            findings.append(MCPValidationFinding(
                mcp_id=mcp.id,
                finding_type="disabled_mcp_type_enabled",
                severity="critical",
                detail=f"MCP type '{mcp.type}' is disabled by default but enabled",
            ))

        if mcp.enabled and mcp.risk_level == "critical":
            findings.append(MCPValidationFinding(
                mcp_id=mcp.id,
                finding_type="critical_mcp_enabled_default",
                severity="critical",
                detail=f"Critical risk MCP '{mcp.id}' is enabled by default",
            ))

        for cap in mcp.capabilities:
            if cap not in known_caps:
                findings.append(MCPValidationFinding(
                    mcp_id=mcp.id,
                    finding_type="unknown_capability",
                    severity="high",
                    detail=f"MCP '{mcp.id}' uses unknown capability '{cap}'",
                ))

        allowlisted_tools = set(allowlist.get(mcp.id, []))
        for tool in mcp.tools:
            if tool not in allowlisted_tools:
                findings.append(MCPValidationFinding(
                    mcp_id=mcp.id,
                    finding_type="tool_not_in_allowlist",
                    severity="medium",
                    detail=f"Tool '{tool}' not in allowlist for MCP '{mcp.id}'",
                ))

        if mcp.type == "shell" or mcp.type == "shell-unrestricted":
            findings.append(MCPValidationFinding(
                mcp_id=mcp.id,
                finding_type="unrestricted_shell",
                severity="critical",
                detail=f"MCP '{mcp.id}' uses unrestricted shell",
            ))

        mcp_id_lower = mcp.id.lower()
        for kw in DANGEROUS_KEYWORDS:
            if kw in mcp_id_lower:
                findings.append(MCPValidationFinding(
                    mcp_id=mcp.id,
                    finding_type="dangerous_mcp_name",
                    severity="high",
                    detail=f"MCP '{mcp.id}' contains dangerous keyword '{kw}'",
                ))

        config_path = mcp.config_path
        if config_path:
            config_lower = config_path.lower()
            for kw in DANGEROUS_KEYWORDS:
                if kw in config_lower:
                    findings.append(MCPValidationFinding(
                        mcp_id=mcp.id,
                        finding_type="dangerous_config_path",
                        severity="high",
                        detail=f"MCP config path '{config_path}' contains '{kw}'",
                    ))

        return findings
