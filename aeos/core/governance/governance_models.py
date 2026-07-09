from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


GOV_STATUS_PASS = "PASS"
GOV_STATUS_BLOCKED = "BLOCKED"
GOV_STATUS_WAITING_APPROVAL = "WAITING_APPROVAL"


@dataclass
class GovernanceRequest:
    execution_id: str
    action: str
    actor: str
    role: str
    capability: str
    resource: str = ""
    command: str = ""
    branch: str = ""
    approval_present: bool = False
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernanceResult:
    execution_id: str
    action: str
    status: str
    permission_allowed: bool
    policy_allowed: bool
    requires_approval: bool
    approval_present: bool
    blocking_reasons: list[str]
    evidence_refs: list[str]
    timestamp: str
    permission_decision_id: str = ""
    policy_decision_id: str = ""

    @property
    def blocking_reason(self) -> str:
        return "; ".join(self.blocking_reasons) if self.blocking_reasons else ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "action": self.action,
            "status": self.status,
            "permission_allowed": self.permission_allowed,
            "policy_allowed": self.policy_allowed,
            "requires_approval": self.requires_approval,
            "approval_present": self.approval_present,
            "blocking_reasons": self.blocking_reasons,
            "evidence_refs": self.evidence_refs,
            "timestamp": self.timestamp,
            "permission_decision_id": self.permission_decision_id,
            "policy_decision_id": self.policy_decision_id,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
