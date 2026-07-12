from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import CodeLens, Command
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


class CodeLensResolveFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def resolve_code_lens(self, lens: CodeLens) -> CodeLens:
        with self._lock:
            cmd = lens.command
            if cmd is None:
                return lens

            title = lens.command.title if lens.command else ""
            uri = ""
            stable_id = ""

            if lens.command and lens.command.arguments:
                args = lens.command.arguments
                if len(args) >= 1:
                    uri = str(args[0])
                if len(args) >= 2:
                    stable_id = str(args[1])

            resolved_title = self._resolve_title(cmd.command, title, uri, stable_id)
            if resolved_title != title:
                if lens.command is not None:
                    lens.command.title = resolved_title

            return lens

    def _resolve_title(self, command: str, current_title: str, uri: str, stable_id: str) -> str:
        if command == "aeos.validateDocument":
            doc_name = self._get_doc_name(uri)
            return f"Validate {doc_name}" if doc_name else current_title
        elif command == "aeos.estimateTokens":
            sym_name = self._get_symbol_name(stable_id)
            return f"Estimate tokens for {sym_name}" if sym_name else current_title
        elif command == "aeos.dryRunSkill":
            sym_name = self._get_symbol_name(stable_id)
            return f"Dry-run skill '{sym_name}'" if sym_name else current_title
        elif command == "aeos.dryRunPlaybook":
            sym_name = self._get_symbol_name(stable_id)
            return f"Dry-run playbook '{sym_name}'" if sym_name else current_title
        elif command == "aeos.judgeArtifact":
            sym_name = self._get_symbol_name(stable_id)
            return f"Judge artifact '{sym_name}'" if sym_name else current_title
        elif command == "aeos.showReferences":
            sym_name = self._get_symbol_name(stable_id)
            return f"Show references for '{sym_name}'" if sym_name else current_title
        elif command == "aeos.showDependencyGraph":
            sym_name = self._get_symbol_name(stable_id)
            return f"Dependency graph for '{sym_name}'" if sym_name else current_title
        return current_title

    def _get_doc_name(self, uri: str) -> str:
        try:
            from pathlib import Path
            return Path(uri.replace("file://", "").replace("\\", "/")).name
        except Exception:
            return ""

    def _get_symbol_name(self, stable_id: str) -> str:
        if not stable_id:
            return ""
        sym = self._semantic_model.get_symbol_by_id(stable_id)
        if sym is not None:
            return getattr(sym, "name", stable_id)
        return stable_id
