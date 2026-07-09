"""Evidence Cache Invalidator — clears cache entries based on invalidation policies."""

from pathlib import Path
import json


class EvidenceCacheInvalidator:
    def __init__(self, cache_root: str):
        self.cache_root = Path(cache_root) / ".aeos" / "cache"

    def invalidate(self, playbook_id: str = None, reason: str = "policy_change") -> int:
        if not self.cache_root.exists():
            return 0
        count = 0
        for f in self.cache_root.iterdir():
            if f.suffix == ".json" and (playbook_id is None or playbook_id in f.stem):
                f.unlink()
                count += 1
        return count

    def invalidate_all(self) -> int:
        if not self.cache_root.exists():
            return 0
        count = len(list(self.cache_root.glob("*.json")))
        for f in self.cache_root.glob("*.json"):
            f.unlink()
        return count

    def status(self) -> dict:
        if not self.cache_root.exists():
            return {"total_entries": 0, "total_size_mb": 0.0}
        total_bytes = sum(f.stat().st_size for f in self.cache_root.glob("*.json"))
        return {
            "total_entries": len(list(self.cache_root.glob("*.json"))),
            "total_size_mb": total_bytes / (1024 * 1024),
        }