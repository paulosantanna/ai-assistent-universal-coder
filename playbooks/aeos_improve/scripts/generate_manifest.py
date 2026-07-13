#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
entries = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name not in {"MANIFEST.json", "VALIDATION_REPORT.json", "VALIDATION_REPORT.txt"}:
        entries.append({
            "path": p.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size,
        })
payload = {
    "package": root.name,
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "file_count": len(entries),
    "files": entries,
}
(root / "MANIFEST.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"WROTE {root / 'MANIFEST.json'}")
