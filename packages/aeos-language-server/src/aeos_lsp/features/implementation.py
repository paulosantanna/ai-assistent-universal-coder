from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    ImplementationParams,
    Location,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import Agent, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class ImplementationFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_implementation(self, params: ImplementationParams) -> list[Location] | Location | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            locations: list[Location] = []

            if isinstance(symbol, Agent):
                children_ids = self._semantic_model.inheritance_graph.get_children(symbol.stable_id)
                for child_id in children_ids:
                    child = self._semantic_model.resolver.resolve_by_id(child_id)
                    if child.resolved and child.symbol is not None:
                        locations.append(self._to_location(child.symbol))

                if symbol.parent_id:
                    parent = self._semantic_model.resolver.resolve_by_id(symbol.parent_id)
                    if parent.resolved and parent.symbol is not None:
                        pass

            else:
                refs = self._semantic_model.get_references(uri, pos)
                if isinstance(refs, list):
                    for ref in refs:
                        if isinstance(ref, dict):
                            ref_uri = ref.get("uri", "")
                            ref_range = ref.get("range")
                            if ref_range:
                                locations.append(Location(uri=ref_uri, range=ref_range))

            if not locations and isinstance(symbol, Agent):
                implementations = self._find_implementations(symbol)
                locations.extend(implementations)

            if len(locations) == 1:
                return locations[0]

            return locations if locations else None

    def _find_implementations(self, agent: Agent) -> list[Location]:
        locations: list[Location] = []
        all_agents = self._semantic_model.get_symbols_by_kind(SymbolKind.AGENT)
        for other in all_agents:
            if isinstance(other, Agent) and other.parent_id == agent.stable_id:
                locations.append(self._to_location(other))
        return locations

    def _to_location(self, symbol: Any) -> Location:
        uri = getattr(symbol, "source_uri", "")
        range_ = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
        if range_ is None:
            range_ = Range(start=Position(line=0, character=0), end=Position(line=0, character=0))
        return Location(uri=uri, range=range_)
