"""SHA256-based context cache for token budget management.

Caches compressed file content keyed by (file_path, content_hash, model_id).
Stores cache entries as JSON files in .aeos/cache/tokens/.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Optional


class TokenContextCache:
    """Cache for compressed file contexts, keyed by SHA256."""

    def __init__(self, cache_dir: Optional[str] = None):
        self._cache_dir = Path(cache_dir or ".aeos/cache/tokens")
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._hits: int = 0
        self._misses: int = 0

    def _key(self, file_path: str, content_hash: str, model_id: str) -> str:
        raw = f"{file_path}:{content_hash}:{model_id}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _entry_path(self, cache_key: str) -> Path:
        return self._cache_dir / f"{cache_key}.json"

    def get(self, file_path: str, content_hash: str, model_id: str) -> Optional[str]:
        key = self._key(file_path, content_hash, model_id)
        entry_path = self._entry_path(key)
        if entry_path.is_file():
            try:
                data = json.loads(entry_path.read_text(encoding="utf-8"))
                if data.get("content_hash") == content_hash:
                    self._hits += 1
                    return data.get("compressed", "")
            except (json.JSONDecodeError, OSError):
                pass
        self._misses += 1
        return None

    def put(
        self, file_path: str, content_hash: str, model_id: str, compressed: str
    ) -> None:
        key = self._key(file_path, content_hash, model_id)
        entry_path = self._entry_path(key)
        data = {
            "file_path": file_path,
            "content_hash": content_hash,
            "model_id": model_id,
            "compressed": compressed,
        }
        entry_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def invalidate(self, file_path: str) -> int:
        count = 0
        for entry in self._cache_dir.glob("*.json"):
            try:
                data = json.loads(entry.read_text(encoding="utf-8"))
                if data.get("file_path") == file_path:
                    entry.unlink()
                    count += 1
            except (json.JSONDecodeError, OSError):
                pass
        return count

    def invalidate_all(self) -> int:
        count = 0
        for entry in self._cache_dir.glob("*.json"):
            entry.unlink()
            count += 1
        self._hits = 0
        self._misses = 0
        return count

    @property
    def hit_count(self) -> int:
        return self._hits

    @property
    def miss_count(self) -> int:
        return self._misses

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return round(self._hits / total, 4)
