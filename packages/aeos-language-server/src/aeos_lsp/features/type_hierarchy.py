from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    Position,
    Range,
    SymbolKind as LspSymbolKind,
    TypeHierarchyItem,
    TypeHierarchyPrepareParams,
    TypeHierarchySubtypesParams,
    TypeHierarchySupertypesParams,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import Agent, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class TypeHierarchyFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def prepare_type_hierarchy(self, params: TypeHierarchyPrepareParams) -> list[TypeHierarchyItem] | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            if not isinstance(symbol, Agent):
                return None

            item = self._to_type_hierarchy_item(symbol)
            return [item] if item is not None else None

    def provide_supertypes(self, params: TypeHierarchySupertypesParams) -> list[TypeHierarchyItem] | None:
        item = params.item

        with self._lock:
            stable_id = self._extract_stable_id(item)
            if stable_id is None:
                return None

            sym = self._semantic_model.get_symbol_by_id(stable_id)
            if sym is None or not isinstance(sym, Agent):
                return None

            supertypes: list[TypeHierarchyItem] = []

            if sym.parent_id:
                parent = self._semantic_model.resolver.resolve_by_id(sym.parent_id)
                if parent.resolved and parent.symbol is not None and isinstance(parent.symbol, Agent):
                    parent_item = self._to_type_hierarchy_item(parent.symbol)
                    if parent_item is not None:
                        supertypes.append(parent_item)

                ancestors = self._semantic_model.inheritance_graph.get_ancestors(stable_id)
                for ancestor_id in ancestors:
                    if ancestor_id != sym.parent_id:
                        ancestor = self._semantic_model.resolver.resolve_by_id(ancestor_id)
                        if ancestor.resolved and ancestor.symbol is not None and isinstance(ancestor.symbol, Agent):
                            ancestor_item = self._to_type_hierarchy_item(ancestor.symbol)
                            if ancestor_item is not None:
                                supertypes.append(ancestor_item)

            return supertypes if supertypes else None

    def provide_subtypes(self, params: TypeHierarchySubtypesParams) -> list[TypeHierarchyItem] | None:
        item = params.item

        with self._lock:
            stable_id = self._extract_stable_id(item)
            if stable_id is None:
                return None

            subtypes: list[TypeHierarchyItem] = []

            children_ids = self._semantic_model.inheritance_graph.get_children(stable_id)
            for child_id in children_ids:
                child = self._semantic_model.resolver.resolve_by_id(child_id)
                if child.resolved and child.symbol is not None and isinstance(child.symbol, Agent):
                    child_item = self._to_type_hierarchy_item(child.symbol)
                    if child_item is not None:
                        subtypes.append(child_item)

            descendants = self._semantic_model.inheritance_graph.get_descendants(stable_id)
            for desc_id in descendants:
                if desc_id not in children_ids:
                    desc = self._semantic_model.resolver.resolve_by_id(desc_id)
                    if desc.resolved and desc.symbol is not None and isinstance(desc.symbol, Agent):
                        desc_item = self._to_type_hierarchy_item(desc.symbol)
                        if desc_item is not None:
                            subtypes.append(desc_item)

            return subtypes if subtypes else None

    def _to_type_hierarchy_item(self, agent: Agent) -> TypeHierarchyItem | None:
        name = getattr(agent, "name", agent.stable_id)
        uri = getattr(agent, "source_uri", "")
        sr = getattr(agent, "selection_range", None) or getattr(agent, "full_range", None)
        if sr is None:
            return None

        detail_parts: list[str] = [f"agent: {agent.stable_id}"]
        if agent.parent_id:
            detail_parts.append(f"extends: {agent.parent_id}")
        if agent.skills:
            detail_parts.append(f"skills: {len(agent.skills)}")

        return TypeHierarchyItem(
            name=str(name),
            kind=LspSymbolKind.Class,
            tags=None,
            detail=" | ".join(detail_parts),
            uri=uri,
            range=getattr(agent, "full_range", sr) or sr,
            selection_range=sr,
            data={"stable_id": agent.stable_id},
        )

    def _extract_stable_id(self, item: TypeHierarchyItem) -> str | None:
        data = getattr(item, "data", None)
        if isinstance(data, dict):
            sid = data.get("stable_id")
            if sid:
                return str(sid)

        detail = getattr(item, "detail", "") or ""
        for part in detail.split(" | "):
            if part.startswith("agent: "):
                return part[7:]
            if part.startswith("extends: "):
                pass

        return None
