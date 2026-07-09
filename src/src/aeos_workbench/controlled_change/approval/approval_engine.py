"""ApprovalEngine — granular approval system with scope, action, and expiration."""

import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Any


class ApprovalRecord:
    def __init__(self, execution_id: str, action: str, scope: str, approver: str = "", reason: str = "", expiration_days: int = 30):
        self.execution_id = execution_id
        self.approval_id = f"ap-{uuid.uuid4().hex[:12]}"
        self.action = action
        self.scope = scope
        self.approver = approver or "pending"
        self.reason = reason
        self.status = "pending"
        self.decision = None
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.resolved_at: Optional[str] = None
        self.expiration = (datetime.now(timezone.utc) + timedelta(days=expiration_days)).isoformat()

    def to_dict(self) -> dict:
        return {
            "execution_id": self.execution_id,
            "approval_id": self.approval_id,
            "action": self.action,
            "scope": self.scope,
            "approver": self.approver,
            "reason": self.reason,
            "status": self.status,
            "decision": self.decision,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "expiration": self.expiration,
        }


FORBIDDEN_SCOPES = ["**", "*", "all", "everything", "global"]
FORBIDDEN_ACTIONS = ["all", "*", "any"]
GRANULAR_ACTIONS = [
    "filesystem.read",
    "filesystem.write_sandbox",
    "filesystem.write_aeos",
    "patch.propose",
    "refactoring.propose",
    "sandbox.generate_test",
    "dependency.analyze",
    "read.files",
]
GRANULAR_SCOPES = [
    ".aeos/sandbox/**",
    ".aeos/patches/**",
    ".aeos/reports/**",
    ".aeos/evidence/**",
    ".aeos/dry-runs/**",
    "src/**/*.py",
    "src/**/*.ts",
    "runtime/**/*.ts",
]


class ApprovalEngine:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.approvals_dir = self.workspace_root / ".aeos" / "approvals"
        self.approvals_dir.mkdir(parents=True, exist_ok=True)

    def _validate_approval(self, action: str, scope: str) -> list[str]:
        errors = []
        if action in FORBIDDEN_ACTIONS:
            errors.append(f"Action '{action}' is forbidden — use granular actions only")
        if scope in FORBIDDEN_SCOPES:
            errors.append(f"Scope '{scope}' is forbidden — global unrestricted approval is prohibited")
        if action not in GRANULAR_ACTIONS and not action.startswith("playbook."):
            errors.append(f"Action '{action}' is not in the granular approval list: {GRANULAR_ACTIONS}")
        return errors

    def create_approval(self, execution_id: str, action: str, scope: str, approver: str = "", reason: str = "", expiration_days: int = 30) -> dict:
        errors = self._validate_approval(action, scope)
        if errors:
            return {"status": "error", "errors": errors, "approval": None}

        record = ApprovalRecord(execution_id, action, scope, approver, reason, expiration_days)
        path = self.approvals_dir / f"{record.approval_id}.approval.json"
        path.write_text(json.dumps(record.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return {"status": "created", "approval": record.to_dict()}

    def approve(self, execution_id: str, action: str, scope: str, approver: str = "human", reason: str = "Approved") -> dict:
        record = self._find_or_create(execution_id, action, scope)
        errors = self._validate_approval(action, scope)
        if errors:
            return {"status": "error", "errors": errors}

        record.status = "approved"
        record.decision = "approved"
        record.approver = approver
        record.reason = reason
        record.resolved_at = datetime.now(timezone.utc).isoformat()
        self._save(record)
        return {"status": "approved", "approval": record.to_dict()}

    def deny(self, execution_id: str, action: str, scope: str, reason: str = "Denied", approver: str = "human") -> dict:
        record = self._find_or_create(execution_id, action, scope)
        record.status = "denied"
        record.decision = "denied"
        record.approver = approver
        record.reason = reason
        record.resolved_at = datetime.now(timezone.utc).isoformat()
        self._save(record)
        return {"status": "denied", "approval": record.to_dict()}

    def is_approved(self, execution_id: str, action: str, scope: str) -> bool:
        approvals = self.list_approvals(execution_id)
        for a in approvals:
            if a["action"] == action and self._scope_matches(a["scope"], scope):
                if a["status"] == "approved" and a["decision"] == "approved":
                    exp = a.get("expiration", "")
                    if exp and datetime.fromisoformat(exp) > datetime.now(timezone.utc):
                        return True
        return False

    def list_approvals(self, execution_id: Optional[str] = None) -> list[dict]:
        records = []
        for path in self.approvals_dir.glob("*.approval.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if not execution_id or data.get("execution_id") == execution_id:
                records.append(data)
        return sorted(records, key=lambda r: r.get("created_at", ""))

    def show_approval(self, approval_id: str) -> Optional[dict]:
        path = self.approvals_dir / f"{approval_id}.approval.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        path = self.approvals_dir / f"{approval_id}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def show_approval_by_execution(self, execution_id: str) -> Optional[dict]:
        for path in self.approvals_dir.glob("*.approval.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("execution_id") == execution_id:
                return data
        return None

    def _find_or_create(self, execution_id: str, action: str, scope: str) -> ApprovalRecord:
        for path in self.approvals_dir.glob("*.approval.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("execution_id") == execution_id and data.get("action") == action and data.get("scope") == scope:
                record = ApprovalRecord(execution_id, action, scope)
                record.__dict__.update(data)
                return record
        return ApprovalRecord(execution_id, action, scope)

    def _save(self, record: ApprovalRecord):
        path = self.approvals_dir / f"{record.approval_id}.approval.json"
        path.write_text(json.dumps(record.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def _scope_matches(self, pattern: str, target: str) -> bool:
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            return target.startswith(prefix)
        if pattern.endswith("/*"):
            prefix = pattern[:-1]
            return target.startswith(prefix) and "/" not in target[len(prefix):]
        return pattern == target