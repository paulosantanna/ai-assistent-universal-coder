from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    InlayHint,
    InlayHintKind,
    InlayHintLabelPart,
    InlayHintParams,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Input,
    Output,
    PlaybookStep,
    Skill,
    SymbolKind,
    Variable,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class InlayHintsFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_inlay_hints(self, params: InlayHintParams) -> list[InlayHint] | None:
        uri = params.text_document.uri
        range_ = params.range

        with self._lock:
            symbols = self._semantic_model.get_symbols_by_uri(uri)
            if not symbols:
                return None

            hints: list[InlayHint] = []

            for sym in symbols:
                sr = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)
                if sr is None:
                    continue

                if range_ is not None:
                    if sr.end.line < range_.start.line or sr.start.line > range_.end.line:
                        continue

                if isinstance(sym, Variable):
                    type_label = sym.type_ref or "any"
                    hint_pos = Position(line=sr.end.line, character=sr.end.character)
                    hints.append(InlayHint(
                        position=hint_pos,
                        label=f": {type_label}",
                        kind=InlayHintKind.Type,
                        padding_left=True,
                        tooltip=f"Variable type: {type_label}",
                    ))

                    if sym.default is not None:
                        hint_pos2 = Position(line=sr.end.line, character=sr.end.character)
                        hints.append(InlayHint(
                            position=hint_pos2,
                            label=f" = {sym.default}",
                            kind=InlayHintKind.Parameter,
                            padding_left=True,
                            tooltip=f"Default: {sym.default}",
                        ))

                elif isinstance(sym, Input):
                    type_label = sym.type_ref or "any"
                    required_label = " (required)" if sym.required else ""
                    hint_pos = Position(line=sr.end.line, character=sr.end.character)
                    hints.append(InlayHint(
                        position=hint_pos,
                        label=f": {type_label}{required_label}",
                        kind=InlayHintKind.Type,
                        padding_left=True,
                        tooltip=f"Input type: {type_label}{required_label}",
                    ))

                elif isinstance(sym, Output):
                    type_label = sym.type_ref or "any"
                    hint_pos = Position(line=sr.end.line, character=sr.end.character)
                    hints.append(InlayHint(
                        position=hint_pos,
                        label=f": {type_label}",
                        kind=InlayHintKind.Type,
                        padding_left=True,
                        tooltip=f"Output type: {type_label}",
                    ))

                elif isinstance(sym, Skill):
                    if sym.inputs:
                        hint_pos = Position(line=sr.start.line, character=sr.start.character)
                        hints.append(InlayHint(
                            position=hint_pos,
                            label=f"({', '.join(sym.inputs[:3])}{'...' if len(sym.inputs) > 3 else ''})",
                            kind=InlayHintKind.Parameter,
                            padding_left=True,
                            tooltip=f"Inputs: {', '.join(sym.inputs)}",
                        ))

                elif isinstance(sym, PlaybookStep):
                    if sym.skill:
                        hint_pos = Position(line=sr.end.line, character=sr.end.character)
                        params_parts: list[str] = []
                        if sym.inputs:
                            for k in list(sym.inputs.keys())[:3]:
                                params_parts.append(f"{k}: {sym.inputs[k]}")
                        label = f"({', '.join(params_parts)}{'...' if len(sym.inputs) > 3 else ''})" if params_parts else ""
                        if label:
                            hints.append(InlayHint(
                                position=hint_pos,
                                label=label,
                                kind=InlayHintKind.Parameter,
                                padding_left=True,
                                tooltip=f"Calling skill: {sym.skill}",
                            ))

            return hints if hints else None
