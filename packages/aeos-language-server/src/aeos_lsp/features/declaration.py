from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    DeclarationParams,
    Location,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


class DeclarationFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_declaration(self, params: DeclarationParams) -> list[Location] | Location | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            declaration_range = getattr(symbol, "declaration", None)
            source_uri = getattr(symbol, "source_uri", uri)

            if declaration_range is not None:
                return Location(uri=source_uri, range=declaration_range)

            selection_range = getattr(symbol, "selection_range", None)
            if selection_range is not None:
                return Location(uri=source_uri, range=selection_range)

            full_range = getattr(symbol, "full_range", None)
            if full_range is not None:
                return Location(uri=source_uri, range=full_range)

            return Location(
                uri=source_uri,
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
            )
