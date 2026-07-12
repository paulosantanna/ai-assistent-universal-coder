from __future__ import annotations

import threading
import time
from pathlib import Path
from urllib.parse import urlparse

from lsprotocol.types import DidChangeWatchedFilesParams, FileChangeType

from aeos_lsp.workspace.exclusions import Exclusions

DEBOUNCE_INTERVAL_SECONDS = 0.3


class FileWatcher:
    def __init__(
        self,
        exclusions: Exclusions | None = None,
        debounce_seconds: float = DEBOUNCE_INTERVAL_SECONDS,
    ) -> None:
        self._exclusions = exclusions or Exclusions()
        self._debounce_seconds = debounce_seconds
        self._lock = threading.Lock()
        self._pending_events: dict[str, tuple[str, FileChangeType, float]] = {}
        self._last_processed: dict[str, float] = {}
        self._on_change_callbacks: list[callable] = []

    def register_callback(self, callback: callable) -> None:
        self._on_change_callbacks.append(callback)

    def process_did_change_watched_files(self, params: DidChangeWatchedFilesParams) -> None:
        now = time.monotonic()
        for event in params.changes:
            uri = event.uri
            if self.ignored_file(uri):
                continue
            self._pending_events[uri] = (uri, event.type, now)
        self._flush_debounced()

    def ignored_file(self, uri: str) -> bool:
        from urllib.parse import urlparse

        parsed = urlparse(uri)
        path = Path(parsed.path)
        return self._exclusions.matches_exclusion(path)

    def _flush_debounced(self) -> None:
        now = time.monotonic()
        flushed: list[tuple[str, FileChangeType]] = []
        uris_to_remove: list[str] = []
        for uri, (event_uri, event_type, timestamp) in self._pending_events.items():
            if now - timestamp >= self._debounce_seconds:
                flushed.append((event_uri, event_type))
                uris_to_remove.append(uri)
        for uri in uris_to_remove:
            self._pending_events.pop(uri, None)
        for event_uri, event_type in flushed:
            for callback in self._on_change_callbacks:
                callback(event_uri, event_type)
