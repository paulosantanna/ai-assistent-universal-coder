import json
from pathlib import Path

class AuditExporter:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def export_jsonl(self, execution_id: str, records: list[dict]):
        out = self.target_root / ".aeos" / "audit" / execution_id / "audit-export.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return str(out)
