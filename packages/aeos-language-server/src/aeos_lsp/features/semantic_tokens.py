from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    Position,
    Range,
    SemanticTokenModifiers,
    SemanticTokens,
    SemanticTokensDelta,
    SemanticTokensDeltaParams,
    SemanticTokensEdit,
    SemanticTokensParams,
    SemanticTokensRangeParams,
    SemanticTokenTypes,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
    AgentLayer,
    DeprecationStatus,
    Input,
    Output,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
    Tool,
    Variable,
)
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.symbols import SemanticSymbol


_AEOS_TOKEN_TYPES: list[str] = [
    "agent", "skill", "playbook", "tool", "policy", "permission",
    "gate", "evidence", "model", "variable", "input", "output",
    "step", "registry", "deprecated", "unsafe", "unresolved",
    "readOnly", "mutating",
]

_AEOS_TOKEN_MODIFIERS: list[str] = [
    "declaration", "definition", "readonly", "static", "deprecated",
    "abstract", "async", "modification", "documentation", "defaultLibrary",
]

def _modifier_bit(name: str) -> int:
    try:
        return 1 << _AEOS_TOKEN_MODIFIERS.index(name)
    except ValueError:
        return 0


def _type_index(name: str) -> int:
    try:
        return _AEOS_TOKEN_TYPES.index(name)
    except ValueError:
        return 0


def _encode_token(
    line: int, col: int, length: int, type_idx: int, mod_mask: int
) -> int:
    return (line << 24) | (col << 16) | (length << 8) | (type_idx << 4) | mod_mask


_TOKEN_TYPE_MAP: dict[SymbolKind, int] = {
    SymbolKind.AGENT: _AEOS_TOKEN_TYPES.index("agent"),
    SymbolKind.SKILL: _AEOS_TOKEN_TYPES.index("skill"),
    SymbolKind.PLAYBOOK: _AEOS_TOKEN_TYPES.index("playbook"),
    SymbolKind.TOOL: _AEOS_TOKEN_TYPES.index("tool"),
    SymbolKind.COMMAND: _AEOS_TOKEN_TYPES.index("tool"),
    SymbolKind.POLICY: _AEOS_TOKEN_TYPES.index("policy"),
    SymbolKind.PERMISSION: _AEOS_TOKEN_TYPES.index("permission"),
    SymbolKind.REGISTRY: _AEOS_TOKEN_TYPES.index("registry"),
    SymbolKind.MODEL_PROFILE: _AEOS_TOKEN_TYPES.index("model"),
    SymbolKind.TOKEN_BUDGET: _AEOS_TOKEN_TYPES.index("readOnly"),
    SymbolKind.VARIABLE: _AEOS_TOKEN_TYPES.index("variable"),
    SymbolKind.INPUT: _AEOS_TOKEN_TYPES.index("input"),
    SymbolKind.OUTPUT: _AEOS_TOKEN_TYPES.index("output"),
    SymbolKind.PLAYBOOK_STEP: _AEOS_TOKEN_TYPES.index("step"),
    SymbolKind.QUALITY_GATE: _AEOS_TOKEN_TYPES.index("gate"),
    SymbolKind.JUDGE_RULE: _AEOS_TOKEN_TYPES.index("gate"),
    SymbolKind.EVIDENCE_REQUIREMENT: _AEOS_TOKEN_TYPES.index("evidence"),
    SymbolKind.LAYER: _AEOS_TOKEN_TYPES.index("agent"),
}

_TYPE_MODIFIER_MAP: dict[SymbolKind, int] = {
    SymbolKind.AGENT: _modifier_bit("declaration"),
    SymbolKind.SKILL: _modifier_bit("declaration"),
    SymbolKind.PLAYBOOK: _modifier_bit("declaration"),
}


def _encode_semantic_token(
    prev_line: int,
    prev_char: int,
    line: int,
    char: int,
    length: int,
    type_idx: int,
    modifier_bits: int,
) -> list[int]:
    delta_line = line - prev_line
    delta_char = char if delta_line == 0 else char
    return [delta_line, delta_char, length, type_idx, modifier_bits]


class SemanticTokensFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    @property
    def token_types(self) -> list[str]:
        return _AEOS_TOKEN_TYPES

    @property
    def token_modifiers(self) -> list[str]:
        return _AEOS_TOKEN_MODIFIERS

    def provide_semantic_tokens(self, params: SemanticTokensParams) -> SemanticTokens | None:
        uri = params.text_document.uri
        with self._lock:
            tokens = self._collect_tokens(uri)
            if not tokens:
                return None
            return SemanticTokens(data=tokens)

    def provide_semantic_tokens_delta(self, params: SemanticTokensDeltaParams) -> SemanticTokens | SemanticTokensDelta | None:
        uri = params.text_document.uri
        with self._lock:
            tokens = self._collect_tokens(uri)
            if not tokens:
                return None
            return SemanticTokensDelta(
                result_id=str(hash(tuple(tokens))),
                edits=[
                    SemanticTokensEdit(
                        start=0,
                        delete_count=0,
                        data=tokens,
                    )
                ],
            )

    def provide_semantic_tokens_range(self, params: SemanticTokensRangeParams) -> SemanticTokens | None:
        uri = params.text_document.uri
        range_ = params.range
        with self._lock:
            all_tokens = self._collect_tokens(uri)
            if not all_tokens:
                return None
            filtered = self._filter_tokens_by_range(all_tokens, range_)
            return SemanticTokens(data=filtered) if filtered else None

    def _collect_tokens(self, uri: str) -> list[int]:
        raw: list[int] = []
        symbols = self._semantic_model.get_symbols_by_uri(uri)
        if not symbols:
            return raw

        sorted_symbols = sorted(
            symbols,
            key=lambda s: (
                getattr(s, "selection_range", None) or getattr(s, "full_range", Range(start=Position(0, 0), end=Position(0, 0)))
            ).start.line,
        )

        prev_line = 0
        prev_char = 0

        for sym in sorted_symbols:
            sr = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)
            if sr is None:
                continue

            start = sr.start
            end = sr.end
            length = end.character - start.character
            if length <= 0:
                length = max(len(getattr(sym, "name", sym.stable_id)), 1)

            type_idx = self._token_type(sym)
            mod_bits = self._token_modifiers(sym)

            encoded = _encode_semantic_token(
                prev_line, prev_char,
                start.line, start.character,
                length, type_idx, mod_bits,
            )
            raw.extend(encoded)
            prev_line = start.line
            prev_char = start.character

        return raw

    def _token_type(self, symbol: SemanticSymbol) -> int:
        kind = self._get_kind(symbol)
        base_type = _TOKEN_TYPE_MAP.get(kind, 0)

        deprecation = getattr(symbol, "deprecation", None)
        if deprecation and isinstance(deprecation, DeprecationStatus) and deprecation in (
            DeprecationStatus.DEPRECATED, DeprecationStatus.REMOVED, DeprecationStatus.SUPERSEDED,
        ):
            base_type = _AEOS_TOKEN_TYPES.index("deprecated")

        mutating = getattr(symbol, "mutating", False)
        if mutating:
            base_type = _AEOS_TOKEN_TYPES.index("mutating")

        return base_type

    def _token_modifiers(self, symbol: SemanticSymbol) -> int:
        bits = 0
        kind = self._get_kind(symbol)

        if kind in (SymbolKind.AGENT, SymbolKind.SKILL, SymbolKind.PLAYBOOK):
            bits |= _modifier_bit("declaration")

        deprecation = getattr(symbol, "deprecation", None)
        if deprecation and isinstance(deprecation, DeprecationStatus) and deprecation in (
            DeprecationStatus.DEPRECATED, DeprecationStatus.REMOVED,
        ):
            bits |= _modifier_bit("deprecated")

        visibility = getattr(symbol, "visibility", None)
        if visibility is not None and hasattr(visibility, "value"):
            if visibility.value == "private":
                bits |= _modifier_bit("readonly")

        mutating = getattr(symbol, "mutating", False)
        if mutating:
            bits |= _modifier_bit("modification")

        return bits

    @staticmethod
    def _get_kind(symbol: Any) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN

    @staticmethod
    def _filter_tokens_by_range(data: list[int], range_: Range) -> list[int]:
        if not data:
            return []

        filtered: list[int] = []
        current_line = 0
        current_char = 0

        i = 0
        while i < len(data):
            delta_line = data[i]
            delta_char = data[i + 1]
            length = data[i + 2]
            type_idx = data[i + 3]
            mod_bits = data[i + 4]

            current_line += delta_line
            if delta_line == 0:
                current_char += delta_char
            else:
                current_char = delta_char

            if range_.start.line <= current_line <= range_.end.line:
                if current_line == range_.start.line and current_char < range_.start.character:
                    pass
                elif current_line == range_.end.line and current_char + length > range_.end.character:
                    pass
                else:
                    filtered.extend([delta_line, delta_char, length, type_idx, mod_bits])

            i += 5

        return filtered
