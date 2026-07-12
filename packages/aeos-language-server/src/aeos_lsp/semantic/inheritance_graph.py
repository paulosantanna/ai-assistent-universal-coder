from __future__ import annotations

import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from aeos_lsp.semantic.models import Agent, Skill, SymbolKind
from aeos_lsp.semantic.symbols import SemanticSymbol, SymbolTable


class InheritanceCycleError(Exception):
    def __init__(self, cycle: list[str]) -> None:
        self.cycle = cycle
        super().__init__(f"Inheritance cycle detected: {' -> '.join(cycle)}")


@dataclass
class InheritanceGraph:
    _lock: threading.RLock = field(default_factory=threading.RLock)
    _parents: dict[str, str] = field(default_factory=dict)
    _children: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    def add_relationship(self, child_id: str, parent_id: str) -> None:
        with self._lock:
            self._parents[child_id] = parent_id
            self._children[parent_id].append(child_id)

    def remove_node(self, node_id: str) -> bool:
        with self._lock:
            parent_id = self._parents.pop(node_id, None)
            if parent_id is not None:
                if node_id in self._children.get(parent_id, []):
                    self._children[parent_id].remove(node_id)
            children = self._children.pop(node_id, [])
            for child_id in children:
                self._parents.pop(child_id, None)
            return True

    def get_parent(self, node_id: str) -> str | None:
        with self._lock:
            return self._parents.get(node_id)

    def get_children(self, node_id: str) -> list[str]:
        with self._lock:
            return list(self._children.get(node_id, []))

    def get_ancestors(self, node_id: str) -> list[str]:
        with self._lock:
            chain: list[str] = []
            current = node_id
            seen: set[str] = set()
            while current in self._parents:
                if current in seen:
                    break
                seen.add(current)
                parent = self._parents[current]
                chain.append(parent)
                current = parent
            return chain

    def get_descendants(self, node_id: str) -> list[str]:
        with self._lock:
            result: list[str] = []
            queue = deque([node_id])
            seen: set[str] = set()
            while queue:
                nid = queue.popleft()
                if nid in seen:
                    continue
                seen.add(nid)
                if nid != node_id:
                    result.append(nid)
                for child in self._children.get(nid, []):
                    if child not in seen:
                        queue.append(child)
            return result

    def is_leaf(self, node_id: str) -> bool:
        with self._lock:
            return node_id not in self._children or len(self._children[node_id]) == 0

    def is_root(self, node_id: str) -> bool:
        with self._lock:
            return node_id not in self._parents

    def get_roots(self) -> list[str]:
        with self._lock:
            all_ids = set(self._parents.keys()) | set(self._children.keys())
            return [nid for nid in all_ids if nid not in self._parents]

    def get_leaves(self) -> list[str]:
        with self._lock:
            all_ids = set(self._parents.keys()) | set(self._children.keys())
            return [nid for nid in all_ids if nid not in self._children or len(self._children[nid]) == 0]

    def has_cycle(self) -> bool:
        with self._lock:
            visited: set[str] = set()
            rec_stack: set[str] = set()

            def _dfs(node_id: str) -> bool:
                visited.add(node_id)
                rec_stack.add(node_id)
                parent = self._parents.get(node_id)
                if parent is not None:
                    if parent not in visited:
                        if _dfs(parent):
                            return True
                    elif parent in rec_stack:
                        return True
                rec_stack.discard(node_id)
                return False

            all_ids = set(self._parents.keys()) | set(self._children.keys())
            for nid in all_ids:
                if nid not in visited:
                    if _dfs(nid):
                        return True
            return False

    def find_cycles(self) -> list[list[str]]:
        with self._lock:
            cycles: list[list[str]] = []
            visited: set[str] = set()
            rec_stack: list[str] = []

            def _dfs(node_id: str) -> None:
                visited.add(node_id)
                rec_stack.append(node_id)
                parent = self._parents.get(node_id)
                if parent is not None:
                    if parent not in visited:
                        _dfs(parent)
                    elif parent in rec_stack:
                        idx = rec_stack.index(parent)
                        cycles.append(list(rec_stack[idx:]))
                rec_stack.pop()

            all_ids = set(self._parents.keys()) | set(self._children.keys())
            for nid in all_ids:
                if nid not in visited:
                    _dfs(nid)
            return cycles

    def compute_mro(self, node_id: str, symbol_table: SymbolTable | None = None) -> list[str]:
        with self._lock:
            mro: list[str] = []
            seen: set[str] = set()

            def _dfs(current: str) -> None:
                parent = self._parents.get(current)
                if parent is not None and parent not in seen:
                    _dfs(parent)
                if current not in seen:
                    seen.add(current)
                    mro.append(current)

            _dfs(node_id)
            return mro

    def resolve_inherited_symbol(self, node_id: str, symbol_name: str, symbol_table: SymbolTable) -> list[SemanticSymbol]:
        mro = self.compute_mro(node_id, symbol_table)
        results: list[SemanticSymbol] = []
        seen_ids: set[str] = set()
        for ancestor_id in mro:
            if ancestor_id in seen_ids:
                continue
            seen_ids.add(ancestor_id)
            symbols = symbol_table.get_by_name(symbol_name)
            for sym in symbols:
                sid = getattr(sym, "stable_id", None)
                if sid == ancestor_id:
                    results.append(sym)
                elif hasattr(sym, "source_uri"):
                    uri = sym.source_uri
                    if ancestor_id in uri or uri.endswith(ancestor_id):
                        results.append(sym)
        return results

    def all_relationships(self) -> list[tuple[str, str]]:
        with self._lock:
            return [(child, parent) for child, parent in self._parents.items()]

    def count(self) -> int:
        with self._lock:
            return len(set(self._parents.keys()) | set(self._children.keys()))

    def clear(self) -> None:
        with self._lock:
            self._parents.clear()
            self._children.clear()
