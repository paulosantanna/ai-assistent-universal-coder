from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List, Dict, Optional
from uuid import uuid4

@dataclass
class AdvancedApproval:
    execution_id: str
    action: str
    scope: str
    approved_by: str
    reason: str
    expires_at: str
    constraints: Dict = field(default_factory=dict)
    approval_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

class ApprovalValidator:
    forbidden_scopes = {"**", "/", "..", "C:\\", "c:\\"}

    def validate(self, approval: AdvancedApproval) -> dict:
        if not approval.reason:
            return {"allowed": False, "reason": "missing_reason"}
        if approval.scope in self.forbidden_scopes:
            return {"allowed": False, "reason": "forbidden_scope"}
        try:
            expires = datetime.fromisoformat(approval.expires_at.replace("Z", "+00:00"))
            if expires < datetime.now(UTC):
                return {"allowed": False, "reason": "approval_expired"}
        except Exception:
            return {"allowed": False, "reason": "invalid_expiration"}
        return {"allowed": True, "reason": "approval_valid"}
