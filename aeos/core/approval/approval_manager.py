"""AEOS Approval Manager — manages approval lifecycle with audit trail."""

import json
import uuid
from pathlib import Path
from datetime import datetime, UTC, timedelta
from .advanced_approval import AdvancedApproval, ApprovalValidator


class ApprovalManager:
    def __init__(self, target_root: str, config: dict = None):
        self.target_root = Path(target_root)
        self.config = config or {}
        self.approvals_dir = self.target_root / ".aeos" / "approvals"
        self.approvals_dir.mkdir(parents=True, exist_ok=True)
        self.validator = ApprovalValidator()
        self.max_duration_hours = float(self.config.get("max_duration_hours", 24))

    def request_approval(self, execution_id: str, action: str, scope: str, requested_by: str, reason: str) -> dict:
        expires_at = (datetime.now(UTC) + timedelta(hours=self.max_duration_hours)).isoformat()
        approval = AdvancedApproval(
            execution_id=execution_id,
            action=action,
            scope=scope,
            approved_by=requested_by,
            reason=reason,
            expires_at=expires_at,
        )
        validation = self.validator.validate(approval)
        if not validation.get("allowed", False):
            return {"status": "error", "errors": [validation.get("reason", "validation_failed")]}

        self._save(approval)
        self._audit_log("approval_requested", approval)
        return {"status": "pending", "approval_id": approval.approval_id, "expires_at": expires_at}

    def approve(self, execution_id: str, action: str, scope: str, approver: str, reason: str) -> dict:
        record = self._find_pending(execution_id, action, scope)
        if record is None:
            return {"status": "error", "errors": ["no_pending_approval_found"]}

        approval = AdvancedApproval(
            execution_id=execution_id,
            action=action,
            scope=scope,
            approved_by=approver,
            reason=reason,
            expires_at=record["expires_at"],
            approval_id=record["approval_id"],
        )
        validation = self.validator.validate(approval)
        if not validation.get("allowed", False):
            return {"status": "error", "errors": [validation.get("reason", "validation_failed")]}

        self._save_approved(approval)
        self._audit_log("approval_granted", approval)
        return {"status": "approved", "approval": approval}

    def deny(self, execution_id: str, action: str, scope: str, reason: str, denied_by: str) -> dict:
        record = {
            "execution_id": execution_id,
            "action": action,
            "scope": scope,
            "denied_by": denied_by,
            "reason": reason,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        self._audit_log("approval_denied", record)
        return {"status": "denied", "approval": record}

    def _find_pending(self, execution_id: str, action: str, scope: str) -> dict | None:
        for f in self.approvals_dir.glob("*.json"):
            record = json.loads(f.read_text(encoding="utf-8"))
            if (record.get("execution_id") == execution_id
                    and record.get("action") == action
                    and record.get("scope") == scope):
                return record
        return None

    def _append(self, approval: AdvancedApproval):
        path = self.approvals_dir / f"{approval.approval_id}.json"
        path.write_text(json.dumps(approval.__dict__, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    def _save_approved(self, approval: AdvancedApproval):
        path = self.approvals_dir / f"{approval.approval_id}.approved.json"
        path.write_text(json.dumps(approval.__dict__, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    def _audit_log(self, event: str, data):
        audit_path = self.approvals_dir / "approval-audit.jsonl"
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "event": event,
                "timestamp": datetime.now(UTC).isoformat(),
                "data": data,
            }, ensure_ascii=False, default=str) + "\n")