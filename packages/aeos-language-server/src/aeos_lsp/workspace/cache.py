from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CacheEntry:
    key: str
    value: Any
    size_bytes: int = 0
    accessed_at: float = 0.0
    created_at: float = 0.0


class DocumentCache:
    def __init__(self, max_size_mb: int = 256) -> None:
        self._max_size_bytes = max_size_mb * 1024 * 1024
        self._current_size: int = 0
        self._lock = threading.Lock()
        self._cache: dict[str, CacheEntry] = {}
        self._access_order: list[str] = []
        self._hits: int = 0
        self._misses: int = 0
        self._invalidations: int = 0

    @property
    def size_bytes(self) -> int:
        with self._lock:
            return self._current_size

    @property
    def max_size_bytes(self) -> int:
        return self._max_size_bytes

    @property
    def count(self) -> int:
        with self._lock:
            return len(self._cache)

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    @property
    def invalidations(self) -> int:
        return self._invalidations

    def get(self, key: str) -> object | None:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None
            self._hits += 1
            entry.accessed_at = time.monotonic()
            self._access_order.remove(key)
            self._access_order.append(key)
            return entry.value

    def set(self, key: str, value: object, size_bytes: int = 0) -> None:
        with self._lock:
            if key in self._cache:
                self._current_size -= self._cache[key].size_bytes
                self._access_order.remove(key)
            entry = CacheEntry(
                key=key,
                value=value,
                size_bytes=size_bytes,
                accessed_at=time.monotonic(),
                created_at=time.monotonic(),
            )
            self._cache[key] = entry
            self._current_size += size_bytes
            self._access_order.append(key)
            self._evict()

    def delete(self, key: str) -> bool:
        with self._lock:
            entry = self._cache.pop(key, None)
            if entry is None:
                return False
            self._current_size -= entry.size_bytes
            self._access_order.remove(key)
            return True

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._current_size = 0
            self._hits = 0
            self._misses = 0
            self._invalidations = 0

    def invalidate_by_content_hash(self, content_hash: str) -> bool:
        with self._lock:
            keys_to_remove = [k for k, v in self._cache.items() if v.value.get("content_hash") == content_hash]
            for key in keys_to_remove:
                self._current_size -= self._cache[key].size_bytes
                del self._cache[key]
                self._access_order.remove(key)
                self._invalidations += 1
            return len(keys_to_remove) > 0

    def stats(self) -> dict[str, object]:
        with self._lock:
            return {
                "count": len(self._cache),
                "size_bytes": self._current_size,
                "max_size_bytes": self._max_size_bytes,
                "hits": self._hits,
                "misses": self._misses,
                "invalidations": self._invalidations,
                "hit_ratio": self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0.0,
            }

    def _evict(self) -> None:
        while self._current_size > self._max_size_bytes and self._access_order:
            oldest_key = self._access_order.pop(0)
            entry = self._cache.pop(oldest_key, None)
            if entry:
                self._current_size -= entry.size_bytes
