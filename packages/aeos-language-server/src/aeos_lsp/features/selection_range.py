from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    Position,
    Range,
    SelectionRange,
    SelectionRangeParams,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


class SelectionRangeFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_selection_ranges(self, params: SelectionRangeParams) -> list[SelectionRange] | None:
        uri = params.text_document.uri
        positions = params.positions

        with self._lock:
            results: list[SelectionRange] = []
            symbols = self._semantic_model.get_symbols_by_uri(uri)
            if not symbols:
                return None

            sorted_symbols = sorted(
                symbols,
                key=lambda s: (
                    getattr(s, "selection_range", getattr(s, "full_range", Range(start=Position(0, 0), end=Position(0, 0)))).start.line,
                    getattr(s, "selection_range", getattr(s, "full_range", Range(start=Position(0, 0), end=Position(0, 0)))).start.character,
                ),
            )

            for pos in positions:
                parent = self._build_selection_hierarchy(pos, sorted_symbols)
                if parent is not None:
                    results.append(parent)

            return results if results else None

    def _build_selection_hierarchy(self, position: Position, symbols: list[Any]) -> SelectionRange | None:
        containing: list[Range] = []

        for sym in symbols:
            sr = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)
            if sr is None:
                continue
            if self._position_in_range(position, sr):
                containing.append(sr)

        containing.sort(key=lambda r: (
            (r.end.line - r.start.line) * 1000 + (r.end.character - r.start.character),
        ))

        if not containing:
            return None

        result: SelectionRange | None = None
        for r in reversed(containing):
            result = SelectionRange(range=r, parent=result)

        return result

    @staticmethod
    def _position_in_range(position: Position, range_: Range) -> bool:
        if position.line < range_.start.line:
            return False
        if position.line > range_.end.line:
            return False
        if position.line == range_.start.line and position.character < range_.start.character:
            return False
        if position.line == range_.end.line and position.character > range_.end.character:
            return False
        return True
