from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4


ToolStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "WAITING_APPROVAL"


@dataclass
class ToolRequest:
    execution_id: str
    actor: str
    role: str
    tool_id: str
    action: str
    capability: str
    resource: str
    input: dict[str, Any] = field(default_factory=dict)
    approval_id: Optional[str] = None
    branch: Optional[str] = None
    command: Optional[str] = None
    details: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: f"tr-{uuid4().hex[:12]}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "actor": self.actor,
            "role": self.role,
            "tool_id": self.tool_id,
            "action": self.action,
            "capability": self.capability,
            "resource": self.resource,
            "input": self.input,
            "approval_id": self.approval_id,
            "branch": self.branch,
            "command": self.command,
            "details": self.details,
            "request_id": self.request_id,
        }


@dataclass
class ToolDecision:
    decision_id: str
    execution_id: str
    request_id: str
    tool_id: str
    action: str
    status: ToolStatus
    permission_allowed: bool
    policy_allowed: bool
    governance_status: str
    reason: str
    permission_decision_id: str = ""
    policy_decision_id: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "execution_id": self.execution_id,
            "request_id": self.request_id,
            "tool_id": self.tool_id,
            "action": self.action,
            "status": self.status,
            "permission_allowed": self.permission_allowed,
            "policy_allowed": self.policy_allowed,
            "governance_status": self.governance_status,
            "reason": self.reason,
            "permission_decision_id": self.permission_decision_id,
            "policy_decision_id": self.policy_decision_id,
            "evidence_refs": self.evidence_refs,
            "timestamp": self.timestamp,
        }


@dataclass
class ToolResult:
    execution_id: str
    request_id: str
    tool_id: str
    action: str
    status: ToolStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    permission_decision_id: str = ""
    policy_decision_id: str = ""
    governance_status: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    duration_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "request_id": self.request_id,
            "tool_id": self.tool_id,
            "action": self.action,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "permission_decision_id": self.permission_decision_id,
            "policy_decision_id": self.policy_decision_id,
            "governance_status": self.governance_status,
            "evidence_refs": self.evidence_refs,
            "duration_ms": self.duration_ms,
        }


@dataclass
class ToolRegistryConfig:
    mcps: list[dict[str, Any]] = field(default_factory=list)
    mcp_runtime_config: dict[str, Any] = field(default_factory=dict)
    tool_router_config: dict[str, Any] = field(default_factory=dict)
    tool_allowlist: dict[str, list[str]] = field(default_factory=dict)
    blocked_tools: list[str] = field(default_factory=list)

    findings: list[dict[str, Any]] = field(default_factory=list)
    loaded_files: list[str] = field(default_factory=list)


def generate_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_decision_id() -> str:
    return f"td-{uuid4().hex[:12]}"
