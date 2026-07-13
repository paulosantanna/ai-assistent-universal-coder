from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aeos.core.evidence.evidence_models import now_iso
from aeos.core.evidence.hash_utils import sha256, sha256_file


@dataclass(frozen=True)
class ChangeRecord:
    execution_id: str
    action: str
    path: str
    relative_path: str
    reason: str
    before_exists: bool
    before_sha256: str | None
    after_exists: bool
    after_sha256: str | None
    size_before: int
    size_after: int
    rollback: dict[str, Any]
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "action": self.action,
            "path": self.path,
            "relative_path": self.relative_path,
            "reason": self.reason,
            "before_exists": self.before_exists,
            "before_sha256": self.before_sha256,
            "after_exists": self.after_exists,
            "after_sha256": self.after_sha256,
            "size_before": self.size_before,
            "size_after": self.size_after,
            "rollback": self.rollback,
            "timestamp": self.timestamp,
        }


class ChangeTracker:
    """Track file writes with before/after hashes and rollback metadata."""

    def __init__(self, execution_id: str, root_dir: str | Path, reason: str):
        self.execution_id = execution_id
        self.root_dir = Path(root_dir).resolve()
        self.reason = reason
        self.records: list[ChangeRecord] = []

    def write_text(self, path: str | Path, content: str) -> ChangeRecord:
        target = Path(path).resolve()
        self._ensure_inside_root(target)
        before_exists = target.exists()
        before_sha = sha256_file(str(target)) if before_exists else None
        before_size = target.stat().st_size if before_exists else 0
        before_content_sha = before_sha

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        after_sha = sha256_file(str(target))
        after_size = target.stat().st_size
        action = "UPDATE" if before_exists else "CREATE"
        rollback = {
            "operation": "restore" if before_exists else "delete",
            "target": str(target),
            "method": "restore from version control or delete generated file",
            "before_sha256": before_content_sha,
            "after_sha256": after_sha,
            "requires_manual_confirmation": True,
        }
        record = ChangeRecord(
            execution_id=self.execution_id,
            action=action,
            path=str(target),
            relative_path=self._relative(target),
            reason=self.reason,
            before_exists=before_exists,
            before_sha256=before_sha,
            after_exists=True,
            after_sha256=after_sha,
            size_before=before_size,
            size_after=after_size,
            rollback=rollback,
            timestamp=now_iso(),
        )
        self.records.append(record)
        return record

    def write_manifests(self, output_dir: str | Path) -> dict[str, str]:
        output = Path(output_dir).resolve()
        output.mkdir(parents=True, exist_ok=True)
        changes = [record.to_dict() for record in self.records]
        change_manifest = {
            "execution_id": self.execution_id,
            "generated_at": now_iso(),
            "root_dir": str(self.root_dir),
            "reason": self.reason,
            "changes": changes,
        }
        change_manifest["manifest_sha256"] = sha256(change_manifest)
        rollback_plan = {
            "execution_id": self.execution_id,
            "generated_at": now_iso(),
            "strategy": "delete_generated_files_or_restore_previous_content",
            "operations": [record.rollback for record in self.records],
            "verification": [
                "verify files match expected pre-change hashes when before_sha256 exists",
                "verify generated-only files are removed when rollback operation is delete",
                "run affected tests after rollback",
            ],
        }
        rollback_plan["manifest_sha256"] = sha256(rollback_plan)

        change_path = output / "change-manifest.json"
        rollback_path = output / "rollback-plan.json"
        summary_path = output / "rollback-plan.md"
        change_path.write_text(json.dumps(change_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        rollback_path.write_text(json.dumps(rollback_plan, indent=2, ensure_ascii=False), encoding="utf-8")
        summary_path.write_text(self._rollback_markdown(rollback_plan), encoding="utf-8")
        return {
            "change_manifest": str(change_path),
            "rollback_plan": str(rollback_path),
            "rollback_summary": str(summary_path),
        }

    def _rollback_markdown(self, rollback_plan: dict[str, Any]) -> str:
        lines = [
            "# Rollback Plan",
            "",
            f"- Execution: `{self.execution_id}`",
            f"- Strategy: `{rollback_plan['strategy']}`",
            "",
            "## Operations",
            "",
        ]
        for index, operation in enumerate(rollback_plan["operations"], start=1):
            lines.append(f"{index}. `{operation['operation']}` `{operation['target']}`")
            lines.append(f"   - before: `{operation.get('before_sha256')}`")
            lines.append(f"   - after: `{operation.get('after_sha256')}`")
        lines.extend(["", "## Verification", ""])
        for item in rollback_plan["verification"]:
            lines.append(f"- {item}")
        return "\n".join(lines) + "\n"

    def _relative(self, target: Path) -> str:
        try:
            return str(target.relative_to(self.root_dir))
        except ValueError:
            return str(target)

    def _ensure_inside_root(self, target: Path) -> None:
        if target != self.root_dir and self.root_dir not in target.parents:
            raise ValueError(f"Refusing to track write outside root: {target}")
