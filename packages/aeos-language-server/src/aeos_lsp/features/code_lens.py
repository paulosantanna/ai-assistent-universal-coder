from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    CodeLens,
    CodeLensParams,
    Command,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.parsing.dispatcher import AEOSDocumentType
from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


_AEOS_COMMANDS: dict[str, str] = {
    "validate_document": "aeos.validateDocument",
    "validate_workspace": "aeos.validateWorkspace",
    "dry_run_skill": "aeos.dryRunSkill",
    "dry_run_playbook": "aeos.dryRunPlaybook",
    "judge_artifact": "aeos.judgeArtifact",
    "show_references": "aeos.showReferences",
    "show_dependency_graph": "aeos.showDependencyGraph",
    "estimate_tokens": "aeos.estimateTokens",
    "open_evidence": "aeos.openEvidence",
    "preview_execution": "aeos.previewExecutionPlan",
}


class CodeLensFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_code_lenses(self, params: CodeLensParams) -> list[CodeLens] | None:
        uri = params.text_document.uri

        with self._lock:
            symbols = self._semantic_model.get_symbols_by_uri(uri)
            if not symbols:
                return None

            lenses: list[CodeLens] = []
            has_agent = False
            has_skill = False
            has_playbook = False

            for sym in symbols:
                kind = self._get_kind(sym)
                sym_range = getattr(sym, "full_range", None) or getattr(sym, "selection_range", None)
                if sym_range is None:
                    sym_range = Range(start=Position(line=0, character=0), end=Position(line=0, character=0))

                if kind == SymbolKind.AGENT:
                    has_agent = True
                    lenses.append(self._make_lens(
                        sym_range, "Validate agent", _AEOS_COMMANDS["validate_document"], [uri]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Show references", _AEOS_COMMANDS["show_references"], [uri, sym.stable_id]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Show dependency graph", _AEOS_COMMANDS["show_dependency_graph"], [uri, sym.stable_id]
                    ))

                elif kind == SymbolKind.SKILL:
                    has_skill = True
                    lenses.append(self._make_lens(
                        sym_range, "Validate skill", _AEOS_COMMANDS["validate_document"], [uri]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Dry-run skill", _AEOS_COMMANDS["dry_run_skill"], [uri, sym.stable_id]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Estimate tokens", _AEOS_COMMANDS["estimate_tokens"], [uri, sym.stable_id]
                    ))

                elif kind == SymbolKind.PLAYBOOK:
                    has_playbook = True
                    lenses.append(self._make_lens(
                        sym_range, "Validate playbook", _AEOS_COMMANDS["validate_document"], [uri]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Dry-run playbook", _AEOS_COMMANDS["dry_run_playbook"], [uri, sym.stable_id]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Preview execution plan", _AEOS_COMMANDS["preview_execution"], [uri, sym.stable_id]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Estimate tokens", _AEOS_COMMANDS["estimate_tokens"], [uri, sym.stable_id]
                    ))

                elif kind in (SymbolKind.POLICY, SymbolKind.PERMISSION, SymbolKind.REGISTRY):
                    lenses.append(self._make_lens(
                        sym_range, "Validate", _AEOS_COMMANDS["validate_document"], [uri]
                    ))
                    lenses.append(self._make_lens(
                        sym_range, "Judge artifact", _AEOS_COMMANDS["judge_artifact"], [uri, sym.stable_id]
                    ))

            if has_agent or has_skill or has_playbook:
                first_range = Range(start=Position(line=0, character=0), end=Position(line=0, character=0))
                lenses.append(self._make_lens(
                    first_range, "Validate workspace", _AEOS_COMMANDS["validate_workspace"], [uri]
                ))
                lenses.append(self._make_lens(
                    first_range, "Open evidence", _AEOS_COMMANDS["open_evidence"], [uri]
                ))

            return lenses if lenses else None

    def _make_lens(self, range_: Range, title: str, command: str, arguments: list[Any]) -> CodeLens:
        return CodeLens(
            range=range_,
            command=Command(
                title=title,
                command=command,
                arguments=arguments,
            ),
        )

    @staticmethod
    def _get_kind(symbol: Any) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN
