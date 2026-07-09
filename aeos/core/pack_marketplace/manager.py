"""AEOS Pack Marketplace Manager — full lifecycle: quarantine → staging → active."""

import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime, UTC
from .marketplace import PackMarketplace
from .contracts import PackRecord


class PackMarketplaceManager:
    def __init__(self, packs_root: str | Path, config: dict = None):
        self.packs_root = Path(packs_root)
        self.packs_root.mkdir(parents=True, exist_ok=True)
        self.marketplace = PackMarketplace()
        self.config = config or {}

    def import_pack(self, source_path: str, package_type: str, manifest: dict) -> dict:
        pack_id = f"pack-{uuid.uuid4().hex[:12]}"
        quarantine_dir = self.packs_root / "quarantine" / pack_id
        quarantine_dir.mkdir(parents=True, exist_ok=True)

        record = PackRecord(
            package_id=pack_id,
            package_type=package_type,
            state="quarantine",
            source_path=source_path,
            manifest=manifest,
        )
        self._save_record(record)

        return {
            "status": "imported_to_quarantine",
            "pack_id": pack_id,
            "state": "quarantine",
            "warnings": ["Pack must be verified and promoted to staging before active use"],
        }

    def verify_and_promote(self, pack_id: str, to_state: str, reason: str, requested_by: str) -> dict:
        record = self._load_record(pack_id)
        if not record:
            return {"status": "error", "errors": ["pack_not_found"]}

        if not self.marketplace.can_transition(record.state, to_state):
            return {"status": "error", "errors": [f"invalid_transition:{record.state}->{to_state}"]}

        record.state = to_state
        self._save_state(record)
        self._audit(pack_id, record.state, reason, requested_by)
        return {"status": "promoted", "pack_id": pack_id, "new_state": to_state}

    def list_packs(self, state: str = None) -> list[dict]:
        results = []
        for f in self.packs_root.rglob("*.json"):
            if f.name == "audit.jsonl":
                continue
            try:
                record = json.loads(f.read_text(encoding="utf-8"))
                if state is None or record.get("state") == state:
                    results.append(record)
            except (json.JSONDecodeError, OSError):
                pass
        return results

    def _save_state(self, record: PackRecord):
        path = self.packs_root / record.state / record.package_id / "record.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record.__dict__, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    def _load_record(self, pack_id: str) -> PackRecord | None:
        for state_dir in ["quarantine", "staging", "active", "archived", "rejected"]:
            path = self.packs_root / state_dir / pack_id / "record.json"
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                return PackRecord(**data)
        return None

    def _audit(self, pack_id: str, state: str, reason: str, requested_by: str):
        audit_path = self.packs_root / "audit.jsonl"
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "event": "pack_state_change",
                "pack_id": pack_id,
                "state": state,
                "reason": reason,
                "requested_by": requested_by,
                "timestamp": datetime.now(UTC).isoformat(),
            }, ensure_ascii=False) + "\n")