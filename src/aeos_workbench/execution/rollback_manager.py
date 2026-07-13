"""Rollback Manager — registers operations and rollback plans with optional encryption."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class RollbackManager:
    def __init__(
        self,
        evidence_dir: Path,
        execution_id: str,
        encryption=None,
        workspace_root: Optional[Path] = None,
    ):
        self.evidence_dir = evidence_dir / execution_id
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.encryption = encryption
        self.workspace_root = workspace_root
        self.operations: list[dict] = []

    def register_generated_file(
        self,
        file_path: Path,
        sandbox_relative: str,
        content_preview: str = "",
    ):
        self.operations.append({
            "operation_id": f"op-{len(self.operations) + 1}",
            "type": "generate",
            "file_path": str(file_path),
            "sandbox_relative": sandbox_relative,
            "rollback_action": "delete_generated_file",
            "content_preview": content_preview[:200],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def register_operation(self, operation: dict):
        self.operations.append(operation)

    def save(self, encrypt: bool = False) -> Path:
        execution_id = self.evidence_dir.name
        data = {
            "execution_id": execution_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "strategy": "sandbox_cleanup",
            "operations": self.operations,
            "summary": {
                "total_operations": len(self.operations),
                "delete_operations": sum(
                    1 for o in self.operations
                    if o.get("rollback_action") == "delete_generated_file"
                ),
            },
        }

        if encrypt and self.encryption and self.encryption.available:
            data = self.encryption.encrypt_rollback(data)

        path = self.evidence_dir / "rollback-plan.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def load(self, evidence_dir: Path, execution_id: str) -> dict:
        path = evidence_dir / execution_id / "rollback-plan.json"
        if not path.exists():
            raise FileNotFoundError(f"Rollback plan not found: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))

        if "operations_encrypted" in data and self.encryption:
            data = self.encryption.decrypt_rollback(data)

        return data
