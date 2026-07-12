from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    PrepareRenameParams,
    Position,
    Range,
    ResponseError,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
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


_RENAMEABLE_KINDS = frozenset({
    SymbolKind.AGENT,
    SymbolKind.SKILL,
    SymbolKind.PLAYBOOK,
    SymbolKind.PLAYBOOK_STEP,
    SymbolKind.TOOL,
    SymbolKind.COMMAND,
    SymbolKind.VARIABLE,
    SymbolKind.INPUT,
    SymbolKind.OUTPUT,
})

_EXTERNAL_ARTIFACT_KEYS = frozenset({
    "agents.registry", "skills.registry", "playbooks.registry",
    "mcps.registry", "lcps.registry", "blueprints.registry",
    "enterprise-skills.registry", "enterprise-playbooks.registry",
    "workbench-profiles.registry", "overlay.registry.index",
})


class PrepareRenameFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def prepare_rename(self, params: PrepareRenameParams) -> Range | ResponseError | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return ResponseError(
                    code=-32600,
                    message="No symbol found at the given position",
                )

            kind = self._get_kind(symbol)
            if kind not in _RENAMEABLE_KINDS:
                return ResponseError(
                    code=-32600,
                    message=f"Symbols of type '{kind.value}' cannot be renamed",
                )

            name = getattr(symbol, "name", symbol.stable_id)
            source_uri = getattr(symbol, "source_uri", "")

            refs_count = self._count_external_references(stable_id=symbol.stable_id, symbol=symbol)
            if refs_count > 0:
                return ResponseError(
                    code=-32600,
                    message=f"Cannot rename '{name}': it is referenced by {refs_count} external artifact(s). "
                            f"Remove or update those references first",
                )

            if self._is_registered_in_external_registry(symbol):
                return ResponseError(
                    code=-32600,
                    message=f"Cannot rename '{name}': registered in external registry. "
                            f"Update the registry entry first",
                )

            if self._has_ambiguous_name(symbol):
                return ResponseError(
                    code=-32600,
                    message=f"Cannot rename '{name}': ambiguous symbol name. "
                            f"Multiple symbols share this name across the workspace",
                )

            range_ = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
            if range_ is None:
                return ResponseError(
                    code=-32600,
                    message="Cannot determine symbol range for rename",
                )

            return range_

    def _count_external_references(self, stable_id: str, symbol: Any) -> int:
        count = 0
        all_symbols = self._semantic_model.symbol_table.all_symbols()
        source_uri = getattr(symbol, "source_uri", "")
        for other in all_symbols:
            other_uri = getattr(other, "source_uri", "")
            if other_uri == source_uri:
                continue
            refs = getattr(other, "references", [])
            if isinstance(refs, list) and stable_id in refs:
                count += 1

            if isinstance(other, Agent) and other.parent_id == stable_id:
                count += 1
            if isinstance(other, Skill) and stable_id in other.tools:
                count += 1
            if isinstance(other, PlaybookStep):
                if other.tool == stable_id or other.skill == stable_id or other.playbook == stable_id:
                    count += 1

        return count

    def _is_registered_in_external_registry(self, symbol: Any) -> bool:
        name = getattr(symbol, "name", "")
        if not name:
            return False
        registries = self._semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)
        source_uri = getattr(symbol, "source_uri", "")
        for reg in registries:
            reg_uri = getattr(reg, "source_uri", "")
            if reg_uri == source_uri or reg_uri == "":
                continue
            entries = getattr(reg, "entries", {})
            if isinstance(entries, dict) and name in entries:
                return True
            if any(name in str(v) for v in entries.values() if isinstance(v, (str, dict, list))):
                return True
        return False

    def _has_ambiguous_name(self, symbol: Any) -> bool:
        name = getattr(symbol, "name", symbol.stable_id)
        same_name = self._semantic_model.symbol_table.get_by_name(name)
        return len(same_name) > 1

    @staticmethod
    def _get_kind(symbol: Any) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN
