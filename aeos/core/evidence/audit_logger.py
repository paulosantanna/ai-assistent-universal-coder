from __future__ import annotations

import json
from pathlib import Path

from aeos.core.evidence.evidence_models import AuditEntry, generate_record_id, now_iso


class AuditLogger:
    def __init__(self, output_dir: str = ".aeos/evidence"):
        self.output_dir = Path(output_dir)

    def log(self, execution_id: str, action: str, actor: str, status: str, detail: str = "") -> AuditEntry:
        entry = AuditEntry(
            entry_id=generate_record_id(),
            execution_id=execution_id,
            action=action,
            actor=actor,
            status=status,
            detail=detail,
            timestamp=now_iso(),
        )
        base = self.output_dir / execution_id
        base.mkdir(parents=True, exist_ok=True)
        fp = base / "audit-log.jsonl"
        with open(fp, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
        return entry
