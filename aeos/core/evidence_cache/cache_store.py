from pathlib import Path
import json
from datetime import datetime, UTC

class EvidenceCacheStore:
    def __init__(self, root: str):
        self.root = Path(root)

    def get(self, cache_key: str):
        path = self.root / ".aeos" / "cache" / f"{cache_key}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def put(self, cache_key: str, value: dict):
        path = self.root / ".aeos" / "cache" / f"{cache_key}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        value = dict(value)
        value["cached_at"] = datetime.now(UTC).isoformat()
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)
