"""Approval Gateway — human-in-the-loop via local approval files."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

APPROVAL_REQUIRED_ACTIONS = {
    "filesystem.delete",
    "filesystem.write_outside_sandbox",
    "git.commit",
    "git.push",
    "git.merge",
    "shell.run",
    "secrets.read",
    "deploy.run",
    "database.schema_change",
}


class ApprovalGateway:
    def __init__(self, approvals_dir: Path):
        self.approvals_dir = approvals_dir
        self.approvals_dir.mkdir(parents=True, exist_ok=True)

    def requires_approval(self, action: str) -> bool:
        return action in APPROVAL_REQUIRED_ACTIONS

    def create_approval_request(self, execution_id: str, action: str, context: dict) -> dict:
        existing = self.check_approval(execution_id)
        if existing and existing.get("status") == "approved":
            return existing
        request = {
            "execution_id": execution_id,
            "approval_id": f"ap-{uuid.uuid4().hex[:8]}",
            "action": action,
            "context": context,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "resolved_at": None,
            "decided_by": None,
            "decision": None,
            "reason": None,
        }
        path = self.approvals_dir / f"{execution_id}.approval.yaml"
        if path.exists():
            maybe_existing = json.loads(path.read_text(encoding="utf-8"))
            if maybe_existing.get("status") == "approved":
                request = maybe_existing
        path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return request

    def check_approval(self, execution_id: str) -> Optional[dict]:
        path = self.approvals_dir / f"{execution_id}.approval.yaml"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return data

    def is_approved(self, execution_id: str) -> bool:
        data = self.check_approval(execution_id)
        if not data:
            return False
        return data.get("status") == "approved" and data.get("decision") == "approved"

    def resolve(
        self,
        execution_id: str,
        decision: str,
        decided_by: str = "human",
        reason: str = "",
    ) -> dict:
        request = self.check_approval(execution_id) or {
            "execution_id": execution_id,
            "approval_id": f"ap-{uuid.uuid4().hex[:8]}",
            "action": "manual_resolve",
            "context": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        request["status"] = decision
        request["decision"] = decision
        request["decided_by"] = decided_by
        request["resolved_at"] = datetime.now(timezone.utc).isoformat()
        request["reason"] = reason
        path = self.approvals_dir / f"{execution_id}.approval.yaml"
        path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return request