from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.symbols import SemanticSymbol, _symbol_kind, _symbol_name


class ScopeKind(Enum):
    WORKSPACE = "workspace"
    FILE = "file"
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"
    STEP = "step"
    BLOCK = "block"
    REGISTRY = "registry"
    INLINE = "inline"


@dataclass
class Scope:
    kind: ScopeKind
    name: str = ""
    range: Range | None = None
    uri: str = ""
    parent: Scope | None = None
    children: list[Scope] = field(default_factory=list)
    symbols: list[SemanticSymbol] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: Scope) -> None:
        child.parent = self
        self.children.append(child)

    def add_symbol(self, symbol: SemanticSymbol) -> None:
        self.symbols.append(symbol)

    def find_scope_at(self, position: Position) -> Scope | None:
        if self.range is not None:
            if not _position_in_range(position, self.range):
                return None
        for child in self.children:
            found = child.find_scope_at(position)
            if found is not None:
                return found
        return self

    def find_symbol_in_scope(self, name: str, kind: SymbolKind | None = None) -> list[SemanticSymbol]:
        results: list[SemanticSymbol] = []
        for sym in self.symbols:
            if _symbol_name(sym) == name:
                if kind is None or _symbol_kind(sym) == kind:
                    results.append(sym)
        return results

    def resolve_name_in_scope(self, name: str, kind: SymbolKind | None = None) -> list[SemanticSymbol]:
        results = self.find_symbol_in_scope(name, kind)
        if results:
            return results
        if self.parent is not None:
            return self.parent.resolve_name_in_scope(name, kind)
        return []

    def ancestors(self) -> list[Scope]:
        chain: list[Scope] = []
        current = self.parent
        while current is not None:
            chain.append(current)
            current = current.parent
        return chain

    def descendants(self) -> list[Scope]:
        result: list[Scope] = []
        for child in self.children:
            result.append(child)
            result.extend(child.descendants())
        return result

    def depth(self) -> int:
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()

    def path(self) -> list[Scope]:
        if self.parent is None:
            return [self]
        return self.parent.path() + [self]


@dataclass
class ScopeTree:
    _lock: threading.RLock = field(default_factory=threading.RLock)
    root: Scope = field(default_factory=lambda: Scope(kind=ScopeKind.WORKSPACE, name="root"))
    _by_uri: dict[str, Scope] = field(default_factory=dict)

    def add_scope(self, uri: str, scope: Scope) -> None:
        with self._lock:
            self._by_uri[uri] = scope
            self.root.add_child(scope)

    def get_scope(self, uri: str) -> Scope | None:
        with self._lock:
            return self._by_uri.get(uri)

    def remove_scope(self, uri: str) -> bool:
        with self._lock:
            scope = self._by_uri.pop(uri, None)
            if scope is None:
                return False
            if scope.parent is not None:
                scope.parent.children.remove(scope)
            return True

    def get_or_create_file_scope(self, uri: str) -> Scope:
        with self._lock:
            existing = self._by_uri.get(uri)
            if existing is not None:
                return existing
            scope = Scope(kind=ScopeKind.FILE, name=uri, uri=uri)
            self._by_uri[uri] = scope
            self.root.add_child(scope)
            return scope

    def find_scope_at(self, uri: str, position: Position) -> Scope | None:
        with self._lock:
            file_scope = self._by_uri.get(uri)
            if file_scope is None:
                return None
            return file_scope.find_scope_at(position)

    def resolve_name(self, uri: str, name: str, position: Position, kind: SymbolKind | None = None) -> list[SemanticSymbol]:
        with self._lock:
            scope = self.find_scope_at(uri, position)
            if scope is None:
                file_scope = self._by_uri.get(uri)
                if file_scope is None:
                    return []
                return file_scope.resolve_name_in_scope(name, kind)
            return scope.resolve_name_in_scope(name, kind)

    def add_symbol_to_scope(self, uri: str, symbol: SemanticSymbol, scope_kind: ScopeKind | None = None) -> None:
        with self._lock:
            scope = self._by_uri.get(uri)
            if scope is None:
                scope = self.get_or_create_file_scope(uri)
            if scope_kind is not None:
                target = self._find_or_create_child_scope(scope, scope_kind, symbol)
            else:
                target = scope
            target.add_symbol(symbol)

    def _find_or_create_child_scope(self, parent: Scope, kind: ScopeKind, symbol: SemanticSymbol) -> Scope:
        name = _symbol_name(symbol)
        for child in parent.children:
            if child.kind == kind and child.name == name:
                return child
        child = Scope(kind=kind, name=name, uri=parent.uri)
        parent.add_child(child)
        return child

    def get_all_uris(self) -> list[str]:
        with self._lock:
            return list(self._by_uri.keys())

    def clear(self) -> None:
        with self._lock:
            self.root = Scope(kind=ScopeKind.WORKSPACE, name="root")
            self._by_uri.clear()


def _position_in_range(position: Position, range_: Range) -> bool:
    if position.line < range_.start.line:
        return False
    if position.line > range_.end.line:
        return False
    if position.line == range_.start.line and position.character < range_.start.character:
        return False
    if position.line == range_.end.line and position.character > range_.end.character:
        return False
    return True
