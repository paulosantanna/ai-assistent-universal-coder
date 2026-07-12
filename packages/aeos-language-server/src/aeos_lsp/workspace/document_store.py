from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import (
    Position,
    Range,
    TextDocumentContentChangeEvent,
    TextDocumentContentChangePartial,
    TextDocumentContentChangeWholeDocument,
)

from aeos_lsp.workspace.snapshot import DocumentSnapshot

STALE_DOCUMENT_TIMEOUT_SECONDS = 300.0
MAX_DOCUMENTS_DEFAULT = 1000


@dataclass
class DocumentEntry:
    uri: str
    version: int
    text: str
    language_id: str = ""
    position_encoding: str = "utf-16"
    last_accessed: float = 0.0

    def snapshot(self) -> DocumentSnapshot:
        return DocumentSnapshot(
            uri=self.uri,
            version=self.version,
            text=self.text,
        )


class DocumentStore:
    def __init__(self, max_documents: int = MAX_DOCUMENTS_DEFAULT) -> None:
        self._max_documents = max_documents
        self._lock = threading.Lock()
        self._documents: dict[str, DocumentEntry] = {}

    @property
    def count(self) -> int:
        with self._lock:
            return len(self._documents)

    def get(self, uri: str) -> DocumentEntry | None:
        with self._lock:
            entry = self._documents.get(uri)
            if entry is not None:
                entry.last_accessed = time.monotonic()
            return entry

    def get_text(self, uri: str) -> str | None:
        entry = self.get(uri)
        return entry.text if entry is not None else None

    def set(self, uri: str, text: str, version: int, language_id: str = "") -> None:
        with self._lock:
            self._evict_if_needed()
            entry = DocumentEntry(
                uri=uri,
                version=version,
                text=text,
                language_id=language_id,
                last_accessed=time.monotonic(),
            )
            self._documents[uri] = entry

    def delete(self, uri: str) -> bool:
        with self._lock:
            return self._documents.pop(uri, None) is not None

    def apply_incremental_change(self, uri: str, change: TextDocumentContentChangePartial, version: int) -> bool:
        with self._lock:
            entry = self._documents.get(uri)
            if entry is None:
                return False
            r = change.range
            if r is None:
                entry.text = change.text
                entry.version = version
                entry.last_accessed = time.monotonic()
                return True
            start_offset = _offset_at_position(entry.text, r.start)
            end_offset = _offset_at_position(entry.text, r.end)
            entry.text = entry.text[:start_offset] + change.text + entry.text[end_offset:]
            entry.version = version
            entry.last_accessed = time.monotonic()
            return True

    def get_snapshot(self, uri: str) -> DocumentSnapshot | None:
        entry = self.get(uri)
        if entry is None:
            return None
        return entry.snapshot()

    def has_uri(self, uri: str) -> bool:
        with self._lock:
            return uri in self._documents

    def list_uris(self) -> list[str]:
        with self._lock:
            return list(self._documents.keys())

    def get_stale_uris(self, max_age_seconds: float = STALE_DOCUMENT_TIMEOUT_SECONDS) -> list[str]:
        now = time.monotonic()
        stale: list[str] = []
        with self._lock:
            for uri, entry in self._documents.items():
                if now - entry.last_accessed > max_age_seconds:
                    stale.append(uri)
        return stale

    def _evict_if_needed(self) -> None:
        while len(self._documents) >= self._max_documents:
            oldest_uri: str | None = None
            oldest_time = float("inf")
            for uri, entry in self._documents.items():
                if entry.last_accessed < oldest_time:
                    oldest_time = entry.last_accessed
                    oldest_uri = uri
            if oldest_uri is not None:
                self._documents.pop(oldest_uri, None)


def _offset_at_position(text: str, position: Position) -> int:
    lines = text.splitlines(keepends=True)
    if position.line < 0:
        return 0
    if position.line >= len(lines):
        return len(text)
    offset = 0
    for i in range(position.line):
        offset += len(lines[i])
    return offset + min(position.character, len(lines[position.line].rstrip("\n\r")))
