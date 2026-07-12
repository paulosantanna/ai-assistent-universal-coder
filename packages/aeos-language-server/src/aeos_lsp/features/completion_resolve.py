from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    InsertTextFormat,
    MarkupContent,
    MarkupKind,
    TextEdit,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class CompletionResolveFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def resolve_completion(self, item: CompletionItem) -> CompletionItem:
        with self._lock:
            label = item.label
            if not isinstance(label, str):
                return item

            sym = self._semantic_model.get_symbol_by_id(label)
            if sym is None:
                symbols_by_name = self._semantic_model.symbol_table.get_by_name(label)
                if symbols_by_name:
                    sym = symbols_by_name[0]

            if sym is not None:
                doc_lines: list[str] = []
                kind = getattr(sym, "symbol_kind", None) or getattr(sym, "kind", SymbolKind.UNKNOWN)
                doc_lines.append(f"**{kind.value}**: `{label}`")

                documentation = getattr(sym, "documentation", "") or getattr(sym, "description", "")
                if documentation:
                    doc_lines.append("")
                    doc_lines.append(str(documentation))

                source_uri = getattr(sym, "source_uri", "")
                if source_uri:
                    doc_lines.append("")
                    doc_lines.append(f"*Source:* `{source_uri}`")

                stable_id = getattr(sym, "stable_id", "")
                if stable_id:
                    doc_lines.append(f"*ID:* `{stable_id}`")

                deprecation = getattr(sym, "deprecation", None)
                if deprecation and hasattr(deprecation, "value") and deprecation.value != "current":
                    doc_lines.append("")
                    doc_lines.append(f"*Status:* {deprecation.value}")

                visibility = getattr(sym, "visibility", None)
                if visibility:
                    doc_lines.append(f"*Visibility:* {visibility.value if hasattr(visibility, 'value') else visibility}")

                item.documentation = MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(doc_lines),
                )

                if isinstance(sym, (list, tuple)):
                    sym = sym[0]

                item.detail = f"({kind.value}) {stable_id}" if stable_id else f"({kind.value})"

            return item
