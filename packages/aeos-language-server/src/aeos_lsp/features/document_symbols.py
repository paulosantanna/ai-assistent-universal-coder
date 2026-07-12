from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    DocumentSymbol,
    DocumentSymbolParams,
    Position,
    Range,
    SymbolKind as LspSymbolKind,
    SymbolTag,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
    AgentLayer,
    Input,
    Output,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind as AeosSymbolKind,
    Tool,
    Variable,
)
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.symbols import SemanticSymbol


_KIND_MAPPING: dict[AeosSymbolKind, LspSymbolKind] = {
    AeosSymbolKind.WORKSPACE: LspSymbolKind.Namespace,
    AeosSymbolKind.REPOSITORY: LspSymbolKind.Namespace,
    AeosSymbolKind.AGENT: LspSymbolKind.Class,
    AeosSymbolKind.SKILL: LspSymbolKind.Function,
    AeosSymbolKind.PLAYBOOK: LspSymbolKind.Method,
    AeosSymbolKind.PLAYBOOK_STEP: LspSymbolKind.Method,
    AeosSymbolKind.TOOL: LspSymbolKind.Function,
    AeosSymbolKind.COMMAND: LspSymbolKind.Function,
    AeosSymbolKind.POLICY: LspSymbolKind.Property,
    AeosSymbolKind.PERMISSION: LspSymbolKind.Property,
    AeosSymbolKind.REGISTRY: LspSymbolKind.Module,
    AeosSymbolKind.MODEL_PROFILE: LspSymbolKind.Class,
    AeosSymbolKind.TOKEN_BUDGET: LspSymbolKind.Constant,
    AeosSymbolKind.VARIABLE: LspSymbolKind.Variable,
    AeosSymbolKind.INPUT: LspSymbolKind.Variable,
    AeosSymbolKind.OUTPUT: LspSymbolKind.Variable,
    AeosSymbolKind.LAYER: LspSymbolKind.Namespace,
    AeosSymbolKind.UNKNOWN: LspSymbolKind.String,
}


class DocumentSymbolsFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_symbols(self, params: DocumentSymbolParams) -> list[DocumentSymbol] | None:
        uri = params.text_document.uri

        with self._lock:
            symbols = self._semantic_model.get_symbols_by_uri(uri)
            if not symbols:
                return None

            top_level: list[DocumentSymbol] = []
            children_map: dict[str, list[DocumentSymbol]] = {}

            for sym in symbols:
                ds = self._to_document_symbol(sym)
                if ds is None:
                    continue
                parent_id = self._get_parent_id(sym)
                if parent_id:
                    children_map.setdefault(parent_id, []).append(ds)
                else:
                    top_level.append(ds)

            for parent_id, children in children_map.items():
                for tl in top_level:
                    if tl.name == parent_id or self._matches_id(tl, parent_id):
                        tl.children = tl.children + children
                        break

            merged = self._merge_hierarchy(top_level, children_map)

            return merged if merged else None

    def _to_document_symbol(self, symbol: SemanticSymbol) -> DocumentSymbol | None:
        kind = self._map_kind(symbol)
        name = getattr(symbol, "name", symbol.stable_id)
        detail = self._build_detail(symbol)

        selection_range = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
        full_range = getattr(symbol, "full_range", None) or selection_range

        if selection_range is None or full_range is None:
            return None

        tags: list[SymbolTag] = []
        deprecation = getattr(symbol, "deprecation", None)
        if deprecation is not None and hasattr(deprecation, "value") and deprecation.value in ("deprecated", "removed"):
            tags.append(SymbolTag.Deprecated)

        return DocumentSymbol(
            name=str(name),
            detail=detail,
            kind=kind,
            range=full_range,
            selection_range=selection_range,
            tags=tags or None,
            children=[],
        )

    def _build_detail(self, symbol: SemanticSymbol) -> str:
        parts: list[str] = []
        kind = self._get_symbol_kind(symbol)

        if isinstance(symbol, Agent):
            parts.append(f"agent: {symbol.stable_id}")
            if symbol.parent_id:
                parts.append(f"extends {symbol.parent_id}")
        elif isinstance(symbol, Skill):
            parts.append(f"skill: {symbol.stable_id}")
        elif isinstance(symbol, Playbook):
            parts.append(f"playbook: {symbol.stable_id}")
        elif isinstance(symbol, PlaybookStep):
            parts.append(f"step: {symbol.step_type or 'default'}")
        elif isinstance(symbol, Tool):
            parts.append(f"tool: {symbol.command}")
        elif isinstance(symbol, Variable):
            parts.append(f"var: {symbol.type_ref or 'any'}")
        elif isinstance(symbol, Input):
            parts.append(f"input: {symbol.type_ref or 'any'}")
        elif isinstance(symbol, Output):
            parts.append(f"output: {symbol.type_ref or 'any'}")
        elif isinstance(symbol, AgentLayer):
            parts.append(f"layer")

        return " | ".join(parts) if parts else kind.value

    def _get_parent_id(self, symbol: SemanticSymbol) -> str | None:
        if isinstance(symbol, PlaybookStep):
            for candidate in self._semantic_model.get_symbols_by_uri(getattr(symbol, "source_uri", "")):
                if isinstance(candidate, Playbook):
                    return candidate.name or candidate.stable_id
        if isinstance(symbol, (Variable, Input, Output)):
            for candidate in self._semantic_model.get_symbols_by_uri(getattr(symbol, "source_uri", "")):
                if isinstance(candidate, Playbook):
                    return candidate.name or candidate.stable_id
        if isinstance(symbol, AgentLayer):
            for candidate in self._semantic_model.get_symbols_by_uri(getattr(symbol, "source_uri", "")):
                if isinstance(candidate, Agent):
                    return candidate.name or candidate.stable_id
        return None

    def _merge_hierarchy(
        self,
        top_level: list[DocumentSymbol],
        children_map: dict[str, list[DocumentSymbol]],
    ) -> list[DocumentSymbol]:
        by_name: dict[str, DocumentSymbol] = {}
        for tl in top_level:
            by_name[tl.name] = tl

        for parent_id, children in children_map.items():
            if parent_id in by_name:
                by_name[parent_id].children = by_name[parent_id].children + children
            elif by_name:
                first = next(iter(by_name.values()))
                first.children = first.children + children

        return top_level

    @staticmethod
    def _map_kind(symbol: SemanticSymbol) -> LspSymbolKind:
        kind = DocumentSymbolsFeature._get_symbol_kind(symbol)
        return _KIND_MAPPING.get(kind, LspSymbolKind.String)

    @staticmethod
    def _get_symbol_kind(symbol: SemanticSymbol) -> AeosSymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return AeosSymbolKind.UNKNOWN

    @staticmethod
    def _matches_id(symbol: DocumentSymbol, stable_id: str) -> bool:
        return symbol.detail is not None and stable_id in symbol.detail
