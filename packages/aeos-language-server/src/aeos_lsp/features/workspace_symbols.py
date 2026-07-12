from __future__ import annotations

import re
import threading
from typing import Any

from lsprotocol.types import (
    Location,
    Position,
    Range,
    SymbolInformation,
    SymbolKind as LspSymbolKind,
    SymbolTag,
    WorkspaceSymbol,
    WorkspaceSymbolParams,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


_KIND_MAPPING: dict[SymbolKind, LspSymbolKind] = {
    SymbolKind.WORKSPACE: LspSymbolKind.Namespace,
    SymbolKind.REPOSITORY: LspSymbolKind.Namespace,
    SymbolKind.AGENT: LspSymbolKind.Class,
    SymbolKind.SKILL: LspSymbolKind.Function,
    SymbolKind.PLAYBOOK: LspSymbolKind.Method,
    SymbolKind.PLAYBOOK_STEP: LspSymbolKind.Method,
    SymbolKind.TOOL: LspSymbolKind.Function,
    SymbolKind.COMMAND: LspSymbolKind.Function,
    SymbolKind.POLICY: LspSymbolKind.Property,
    SymbolKind.PERMISSION: LspSymbolKind.Property,
    SymbolKind.REGISTRY: LspSymbolKind.Module,
    SymbolKind.MODEL_PROFILE: LspSymbolKind.Class,
    SymbolKind.TOKEN_BUDGET: LspSymbolKind.Constant,
    SymbolKind.VARIABLE: LspSymbolKind.Variable,
    SymbolKind.INPUT: LspSymbolKind.Variable,
    SymbolKind.OUTPUT: LspSymbolKind.Variable,
    SymbolKind.LAYER: LspSymbolKind.Namespace,
    SymbolKind.UNKNOWN: LspSymbolKind.String,
}


class WorkspaceSymbolsFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_workspace_symbols(self, params: WorkspaceSymbolParams) -> list[WorkspaceSymbol]:
        query = params.query.strip()
        if not query:
            return self._all_workspace_symbols()

        with self._lock:
            results: list[WorkspaceSymbol] = []
            pattern = re.compile(re.escape(query), re.IGNORECASE)

            for sym in self._semantic_model.symbol_table.all_symbols():
                name = getattr(sym, "name", sym.stable_id)
                stable_id = getattr(sym, "stable_id", "")

                if pattern.search(name) or pattern.search(stable_id):
                    ws = self._to_workspace_symbol(sym, query)
                    if ws is not None:
                        results.append(ws)

            results.sort(key=lambda x: self._rank(x, query), reverse=True)
            return results

    def _all_workspace_symbols(self) -> list[WorkspaceSymbol]:
        with self._lock:
            results: list[WorkspaceSymbol] = []
            for sym in self._semantic_model.symbol_table.all_symbols():
                ws = self._to_workspace_symbol(sym, "")
                if ws is not None:
                    results.append(ws)
            return results

    def _to_workspace_symbol(self, sym: Any, query: str) -> WorkspaceSymbol | None:
        name = getattr(sym, "name", sym.stable_id)
        kind = self._map_kind(sym)
        source_uri = getattr(sym, "source_uri", "")
        selection_range = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)

        if not source_uri or selection_range is None:
            return None

        container_name = self._container_name(sym)

        tags: list[SymbolTag] = []
        deprecation = getattr(sym, "deprecation", None)
        if deprecation is not None and hasattr(deprecation, "value") and deprecation.value in ("deprecated", "removed"):
            tags.append(SymbolTag.Deprecated)

        return WorkspaceSymbol(
            name=str(name),
            kind=kind,
            tags=tags or None,
            container_name=container_name,
            location=Location(uri=source_uri, range=selection_range),
            data={"stable_id": sym.stable_id, "query": query},
        )

    def _container_name(self, sym: Any) -> str:
        parent_id = getattr(sym, "parent_id", None)
        if parent_id:
            parent = self._semantic_model.resolver.resolve_by_id(parent_id)
            if parent.resolved and parent.symbol is not None:
                return getattr(parent.symbol, "name", parent_id)
            return parent_id
        source_uri = getattr(sym, "source_uri", "")
        if source_uri:
            from pathlib import Path
            try:
                return Path(source_uri.replace("file://", "").replace("\\", "/")).name
            except Exception:
                pass
        return ""

    def _rank(self, ws: WorkspaceSymbol, query: str) -> float:
        name = ws.name.lower()
        q = query.lower()
        if name == q:
            return 100.0
        if name.startswith(q):
            return 50.0
        if q in name:
            return 20.0
        return 0.0

    @staticmethod
    def _map_kind(symbol: Any) -> LspSymbolKind:
        kind = WorkspaceSymbolsFeature._get_kind(symbol)
        return _KIND_MAPPING.get(kind, LspSymbolKind.String)

    @staticmethod
    def _get_kind(symbol: Any) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN

    def resolve_workspace_symbol(self, workspace_symbol: WorkspaceSymbol) -> WorkspaceSymbol:
        data = getattr(workspace_symbol, "data", None)
        if isinstance(data, dict):
            stable_id = data.get("stable_id")
            if stable_id:
                sym = self._semantic_model.get_symbol_by_id(stable_id)
                if sym is not None:
                    workspace_symbol = self._to_workspace_symbol(sym, data.get("query", "")) or workspace_symbol
        return workspace_symbol
