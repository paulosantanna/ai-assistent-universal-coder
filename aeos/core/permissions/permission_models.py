from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class PermissionRequest:
    execution_id: str
    actor: str
    role: str
    action: str
    capability: str
    resource: str = ""


@dataclass
class PermissionDecision:
    decision_id: str
    execution_id: str
    actor: str
    role: str
    action: str
    capability: str
    resource: str
    allowed: bool
    requires_approval: bool
    approval_id: Optional[str]
    reason: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "execution_id": self.execution_id,
            "actor": self.actor,
            "role": self.role,
            "action": self.action,
            "capability": self.capability,
            "resource": self.resource,
            "allowed": self.allowed,
            "requires_approval": self.requires_approval,
            "approval_id": self.approval_id,
            "reason": self.reason,
            "timestamp": self.timestamp,
        }


@dataclass
class RoleCapabilityMapping:
    role: str
    capabilities: list[str] = field(default_factory=list)


@dataclass
class PermissionConfig:
    default: str = "deny"
    roles: dict[str, RoleCapabilityMapping] = field(default_factory=dict)
    approval_required_actions: list[str] = field(default_factory=list)


def generate_decision_id() -> str:
    import uuid
    return f"pd-{uuid.uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
