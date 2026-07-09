from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MCPEntry:
    id: str
    type: str
    transport: str
    config_path: str
    risk_level: str
    capabilities: list[str]
    tools: list[str]
    enabled: bool = True
    approval_required: bool = False
    write_allowed: bool = False
    sandbox_required: bool = False
    allowlist_required: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "transport": self.transport,
            "risk_level": self.risk_level,
            "capabilities": list(self.capabilities),
            "tools": list(self.tools),
            "enabled": self.enabled,
            "approval_required": self.approval_required,
            "write_allowed": self.write_allowed,
            "sandbox_required": self.sandbox_required,
            "allowlist_required": self.allowlist_required,
            "reason": self.reason,
        }


@dataclass
class MCPValidationFinding:
    mcp_id: str
    finding_type: str
    severity: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_id": self.mcp_id,
            "finding_type": self.finding_type,
            "severity": self.severity,
            "detail": self.detail,
        }


@dataclass
class MCPValidationReport:
    mcps_validated: int = 0
    passed: int = 0
    blocked: int = 0
    findings: list[MCPValidationFinding] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcps_validated": self.mcps_validated,
            "passed": self.passed,
            "blocked": self.blocked,
            "findings": [f.to_dict() for f in self.findings],
        }
