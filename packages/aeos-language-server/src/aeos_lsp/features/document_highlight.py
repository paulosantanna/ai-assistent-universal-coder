from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    DocumentHighlight,
    DocumentHighlightKind,
    DocumentHighlightParams,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class DocumentHighlightFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_highlight(self, params: DocumentHighlightParams) -> list[DocumentHighlight] | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            highlights: list[DocumentHighlight] = []
            stable_id = symbol.stable_id
            name = getattr(symbol, "name", stable_id)

            own_range = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
            if own_range is not None:
                highlights.append(DocumentHighlight(
                    range=own_range,
                    kind=DocumentHighlightKind.Write,
                ))

            symbols_in_doc = self._semantic_model.get_symbols_by_uri(uri)
            for other in symbols_in_doc:
                other_id = getattr(other, "stable_id", "")
                other_name = getattr(other, "name", other_id)
                if other_id == stable_id or other_name == name:
                    other_range = getattr(other, "selection_range", None) or getattr(other, "full_range", None)
                    if other_range is not None and other_range != own_range:
                        highlights.append(DocumentHighlight(
                            range=other_range,
                            kind=DocumentHighlightKind.Read,
                        ))

            refs = self._semantic_model.reference_table.get_for_uri(uri)
            for ref in refs:
                target_uri = getattr(ref, "target_uri", "")
                if target_uri == uri or stable_id in str(target_uri):
                    if ref.source_range not in [h.range for h in highlights]:
                        kind = DocumentHighlightKind.Text if ref.kind.value == "usage" else DocumentHighlightKind.Read
                        highlights.append(DocumentHighlight(
                            range=ref.source_range,
                            kind=kind,
                        ))

                source_uri = getattr(ref, "source_uri", "")
                if source_uri == uri and hasattr(ref, "source_range"):
                    if ref.source_range not in [h.range for h in highlights]:
                        highlights.append(DocumentHighlight(
                            range=ref.source_range,
                            kind=DocumentHighlightKind.Read,
                        ))

            if uri in self._semantic_model.scope_tree._by_uri:
                scope = self._semantic_model.scope_tree._by_uri[uri]
                highlights = self._add_scope_highlights(scope, stable_id, name, highlights)

            return highlights if highlights else None

    def _add_scope_highlights(
        self,
        scope: Any,
        stable_id: str,
        name: str,
        highlights: list[DocumentHighlight],
    ) -> list[DocumentHighlight]:
        for sym in scope.symbols:
            sym_id = getattr(sym, "stable_id", "")
            sym_name = getattr(sym, "name", sym_id)
            if sym_id == stable_id or sym_name == name:
                r = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)
                if r is not None and r not in [h.range for h in highlights]:
                    highlights.append(DocumentHighlight(range=r, kind=DocumentHighlightKind.Read))
        for child in scope.children:
            highlights = self._add_scope_highlights(child, stable_id, name, highlights)
        return highlights
