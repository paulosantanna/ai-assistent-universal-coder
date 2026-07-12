from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

from lsprotocol.types import Range


class ReferenceKind(Enum):
    DEFINITION = "definition"
    USAGE = "usage"
    CALL = "call"
    OVERRIDE = "override"
    IMPLEMENTATION = "implementation"
    IMPORT = "import"
    EXPORT = "export"
    INHERITANCE = "inheritance"
    COMPOSITION = "composition"
    MENTION = "mention"


class ReferenceRole(Enum):
    READ = "read"
    WRITE = "write"
    CALL = "call"
    INSTANTIATE = "instantiate"
    COMPOSE = "compose"
    EXTEND = "extend"
    DECLARE = "declare"
    REFERENCE = "reference"


@dataclass(frozen=True)
class Reference:
    source_uri: str
    source_range: Range
    target_uri: str
    target_range: Range
    kind: ReferenceKind = ReferenceKind.USAGE
    role: ReferenceRole = ReferenceRole.REFERENCE
    data: dict = field(default_factory=dict)


@dataclass
class ReferenceTable:
    _lock: threading.RLock = field(default_factory=threading.RLock)
    _outgoing: dict[str, list[Reference]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _incoming: dict[str, list[Reference]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _by_uri: dict[str, list[Reference]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add_reference(self, ref: Reference) -> None:
        with self._lock:
            self._outgoing[ref.source_uri].append(ref)
            self._incoming[ref.target_uri].append(ref)
            self._by_uri[ref.source_uri].append(ref)
            self._by_uri[ref.target_uri].append(ref)

    def add_references(self, refs: list[Reference]) -> None:
        with self._lock:
            for ref in refs:
                self.add_reference(ref)

    def get_outgoing(self, uri: str) -> list[Reference]:
        with self._lock:
            return list(self._outgoing.get(uri, []))

    def get_incoming(self, uri: str) -> list[Reference]:
        with self._lock:
            return list(self._incoming.get(uri, []))

    def get_for_uri(self, uri: str) -> list[Reference]:
        with self._lock:
            return list(self._by_uri.get(uri, []))

    def get_by_kind(self, kind: ReferenceKind) -> list[Reference]:
        with self._lock:
            return [
                ref
                for refs in self._by_uri.values()
                for ref in refs
                if ref.kind == kind
            ]

    def find_references(self, target_uri: str) -> list[Reference]:
        with self._lock:
            return [
                ref for ref in self._incoming.get(target_uri, [])
                if ref.kind != ReferenceKind.DEFINITION
            ]

    def find_definitions(self, target_uri: str) -> list[Reference]:
        with self._lock:
            return [
                ref for ref in self._incoming.get(target_uri, [])
                if ref.kind == ReferenceKind.DEFINITION
            ]

    def remove_for_uri(self, uri: str) -> int:
        with self._lock:
            count = 0
            for lst in [self._outgoing, self._incoming, self._by_uri]:
                removed = lst.pop(uri, [])
                count += len(removed)
            for u in list(self._by_uri.keys()):
                self._by_uri[u] = [r for r in self._by_uri[u] if r.source_uri != uri and r.target_uri != uri]
            for u in list(self._outgoing.keys()):
                self._outgoing[u] = [r for r in self._outgoing[u] if r.source_uri != uri]
            for u in list(self._incoming.keys()):
                self._incoming[u] = [r for r in self._incoming[u] if r.target_uri != uri]
            return count

    def clear(self) -> None:
        with self._lock:
            self._outgoing.clear()
            self._incoming.clear()
            self._by_uri.clear()

    def count(self) -> int:
        with self._lock:
            return sum(len(refs) for refs in self._by_uri.values()) // 2
