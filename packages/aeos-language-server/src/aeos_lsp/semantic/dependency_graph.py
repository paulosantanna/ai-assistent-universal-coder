from __future__ import annotations

import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from aeos_lsp.semantic.models import SymbolKind


@dataclass
class DependencyNode:
    id: str
    kind: SymbolKind = SymbolKind.UNKNOWN
    uri: str = ""
    dependencies: set[str] = field(default_factory=set)
    dependents: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_dependency(self, target_id: str) -> None:
        self.dependencies.add(target_id)

    def add_dependent(self, source_id: str) -> None:
        self.dependents.add(source_id)

    def remove_dependency(self, target_id: str) -> None:
        self.dependencies.discard(target_id)

    def remove_dependent(self, source_id: str) -> None:
        self.dependents.discard(source_id)


class DependencyGraph:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._nodes: dict[str, DependencyNode] = {}

    def add_node(self, node: DependencyNode) -> None:
        with self._lock:
            self._nodes[node.id] = node

    def add_dependency(self, source_id: str, target_id: str) -> None:
        with self._lock:
            source = self._nodes.get(source_id)
            target = self._nodes.get(target_id)
            if source is None:
                source = DependencyNode(id=source_id)
                self._nodes[source_id] = source
            if target is None:
                target = DependencyNode(id=target_id)
                self._nodes[target_id] = target
            source.add_dependency(target_id)
            target.add_dependent(source_id)

    def remove_node(self, node_id: str) -> bool:
        with self._lock:
            node = self._nodes.pop(node_id, None)
            if node is None:
                return False
            for dep_id in node.dependencies:
                dep = self._nodes.get(dep_id)
                if dep is not None:
                    dep.remove_dependent(node_id)
            for dep_id in node.dependents:
                dep = self._nodes.get(dep_id)
                if dep is not None:
                    dep.remove_dependency(node_id)
            return True

    def get_node(self, node_id: str) -> DependencyNode | None:
        with self._lock:
            return self._nodes.get(node_id)

    def has_node(self, node_id: str) -> bool:
        with self._lock:
            return node_id in self._nodes

    def get_dependencies(self, node_id: str) -> list[DependencyNode]:
        with self._lock:
            node = self._nodes.get(node_id)
            if node is None:
                return []
            return [self._nodes[nid] for nid in node.dependencies if nid in self._nodes]

    def get_dependents(self, node_id: str) -> list[DependencyNode]:
        with self._lock:
            node = self._nodes.get(node_id)
            if node is None:
                return []
            return [self._nodes[nid] for nid in node.dependents if nid in self._nodes]

    def all_nodes(self) -> list[DependencyNode]:
        with self._lock:
            return list(self._nodes.values())

    def count(self) -> int:
        with self._lock:
            return len(self._nodes)

    def clear(self) -> None:
        with self._lock:
            self._nodes.clear()

    def has_cycle(self) -> bool:
        with self._lock:
            visited: set[str] = set()
            rec_stack: set[str] = set()

            def _dfs(node_id: str) -> bool:
                visited.add(node_id)
                rec_stack.add(node_id)
                node = self._nodes.get(node_id)
                if node is not None:
                    for dep_id in node.dependencies:
                        if dep_id not in visited:
                            if _dfs(dep_id):
                                return True
                        elif dep_id in rec_stack:
                            return True
                rec_stack.discard(node_id)
                return False

            for nid in self._nodes:
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
                node = self._nodes.get(node_id)
                if node is not None:
                    for dep_id in node.dependencies:
                        if dep_id not in visited:
                            _dfs(dep_id)
                        elif dep_id in rec_stack:
                            idx = rec_stack.index(dep_id)
                            cycles.append(list(rec_stack[idx:]))
                rec_stack.pop()

            for nid in self._nodes:
                if nid not in visited:
                    _dfs(nid)
            return cycles

    def topological_sort(self) -> list[str]:
        with self._lock:
            in_degree: dict[str, int] = {}
            for nid, node in self._nodes.items():
                in_degree.setdefault(nid, 0)
                for dep_id in node.dependencies:
                    in_degree.setdefault(dep_id, 0)
                    in_degree[nid] = in_degree.get(nid, 0) + 1
            queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
            result: list[str] = []
            while queue:
                nid = queue.popleft()
                result.append(nid)
                node = self._nodes.get(nid)
                if node is not None:
                    for dep_id in node.dependents:
                        in_degree[dep_id] -= 1
                        if in_degree[dep_id] == 0:
                            queue.append(dep_id)
            if len(result) != len(self._nodes):
                return []
            return result

    def reachable_from(self, node_id: str) -> list[str]:
        with self._lock:
            visited: set[str] = set()
            queue = deque([node_id])
            while queue:
                nid = queue.popleft()
                if nid in visited:
                    continue
                visited.add(nid)
                node = self._nodes.get(nid)
                if node is not None:
                    for dep_id in node.dependencies:
                        if dep_id not in visited:
                            queue.append(dep_id)
            visited.discard(node_id)
            return list(visited)

    def reverse_reachable_from(self, node_id: str) -> list[str]:
        with self._lock:
            visited: set[str] = set()
            queue = deque([node_id])
            while queue:
                nid = queue.popleft()
                if nid in visited:
                    continue
                visited.add(nid)
                node = self._nodes.get(nid)
                if node is not None:
                    for dep_id in node.dependents:
                        if dep_id not in visited:
                            queue.append(dep_id)
            visited.discard(node_id)
            return list(visited)

    def impact_analysis(self, changed_node_ids: set[str]) -> dict[str, list[str]]:
        with self._lock:
            result: dict[str, list[str]] = {}
            for nid in changed_node_ids:
                affected = self.reverse_reachable_from(nid)
                if affected:
                    result[nid] = affected
            return result

    def subgraph(self, node_ids: set[str]) -> DependencyGraph:
        with self._lock:
            sub = DependencyGraph()
            for nid in node_ids:
                node = self._nodes.get(nid)
                if node is not None:
                    sub.add_node(DependencyNode(
                        id=node.id,
                        kind=node.kind,
                        uri=node.uri,
                        dependencies=node.dependencies & node_ids,
                        dependents=node.dependents & node_ids,
                        metadata=dict(node.metadata),
                    ))
            return sub

    def merge(self, other: DependencyGraph) -> None:
        with self._lock:
            for node in other.all_nodes():
                existing = self._nodes.get(node.id)
                if existing is not None:
                    existing.dependencies.update(node.dependencies)
                    existing.dependents.update(node.dependents)
                    existing.metadata.update(node.metadata)
                else:
                    self._nodes[node.id] = DependencyNode(
                        id=node.id,
                        kind=node.kind,
                        uri=node.uri,
                        dependencies=set(node.dependencies),
                        dependents=set(node.dependents),
                        metadata=dict(node.metadata),
                    )
