from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    Location,
    Position,
    Range,
    ReferenceParams,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


class ReferencesFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_references(self, params: ReferenceParams) -> list[Location] | None:
        uri = params.text_document.uri
        pos = params.position
        include_declaration = params.context.include_declaration

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            locations: list[Location] = []
            stable_id = symbol.stable_id
            source_uri = getattr(symbol, "source_uri", uri)

            if include_declaration:
                decl_range = getattr(symbol, "declaration", None) or getattr(symbol, "selection_range", None)
                if decl_range is not None:
                    locations.append(Location(uri=source_uri, range=decl_range))

            ref_table = self._semantic_model.reference_table
            refs = ref_table.find_references(stable_id)
            for ref in refs:
                loc = Location(
                    uri=ref.source_uri,
                    range=ref.source_range,
                )
                if loc not in locations:
                    locations.append(loc)

            defns = ref_table.find_definitions(stable_id)
            for ref in defns:
                loc = Location(
                    uri=ref.target_uri,
                    range=ref.target_range,
                )
                if loc not in locations:
                    locations.append(loc)

            return locations if locations else None
