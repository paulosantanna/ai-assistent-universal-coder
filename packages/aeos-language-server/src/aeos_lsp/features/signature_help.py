from __future__ import annotations

import re
import threading
from typing import Any

from lsprotocol.types import (
    ParameterInformation,
    Position,
    SignatureHelp,
    SignatureHelpParams,
    SignatureInformation,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    PlaybookStep,
    Skill,
    SymbolKind,
    Tool,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class SignatureHelpFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_signature_help(self, params: SignatureHelpParams) -> SignatureHelp | None:
        uri = params.text_document.uri
        pos = params.position

        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return None

        text = doc.source
        lines = text.splitlines(keepends=False)
        if pos.line >= len(lines):
            return None

        line = lines[pos.line]
        before_cursor = line[:pos.character]

        sig_info = self._detect_call_context(before_cursor, uri)
        if sig_info is None:
            return None

        callable_sym, active_param = sig_info
        sig = self._build_signature(callable_sym)

        if sig is None:
            return None

        return SignatureHelp(
            signatures=[sig],
            active_signature=0,
            active_parameter=active_param,
        )

    def _detect_call_context(self, before_cursor: str, uri: str) -> tuple[Any, int] | None:
        open_paren = before_cursor.rfind("(")
        if open_paren == -1:
            open_paren = before_cursor.rfind("{")
        if open_paren == -1:
            return None

        call_start = before_cursor[:open_paren].strip()
        call_name = call_start.split()[-1] if call_start.split() else call_start

        after_paren = before_cursor[open_paren + 1:]
        active_param = 0
        depth = 0
        for ch in after_paren:
            if ch == "," and depth == 0:
                active_param += 1
            elif ch in "({":
                depth += 1
            elif ch in ")}":
                depth -= 1

        callable_sym = self._find_callable(call_name, uri)
        if callable_sym is not None:
            return (callable_sym, active_param)

        return None

    def _find_callable(self, name: str, uri: str) -> Any:
        sym = self._semantic_model.get_symbol_by_id(name)
        if sym is not None and isinstance(sym, (Skill, Tool)):
            return sym

        symbols = self._semantic_model.symbol_table.get_by_name(name)
        for s in symbols:
            if isinstance(s, (Skill, Tool)):
                return s
            if isinstance(s, PlaybookStep):
                return s

        env_entry = f"env:{name}"
        env_sym = self._semantic_model.get_symbol_by_id(env_entry)
        if env_sym is not None:
            return env_sym

        return None

    def _build_signature(self, callable_sym: Any) -> SignatureInformation | None:
        label = getattr(callable_sym, "name", callable_sym.stable_id)
        params: list[str] = []
        param_details: list[str] = []
        doc = getattr(callable_sym, "documentation", "") or getattr(callable_sym, "description", "")

        if isinstance(callable_sym, Skill):
            params = list(getattr(callable_sym, "inputs", []))
            outputs = list(getattr(callable_sym, "outputs", []))
            sig_parts = [f"({', '.join(params)})" if params else "()"]
            if outputs:
                sig_parts.append(f" -> ({', '.join(outputs)})")
            label = f"{callable_sym.name}{''.join(sig_parts)}"
            param_details = [f"Input: {p}" for p in params]

        elif isinstance(callable_sym, Tool):
            inputs = getattr(callable_sym, "inputs", [])
            if isinstance(inputs, list):
                input_names: list[str] = []
                for inp in inputs:
                    if isinstance(inp, dict):
                        n = inp.get("name", str(inp))
                        input_names.append(n)
                    else:
                        input_names.append(str(inp))
            elif isinstance(inputs, dict):
                input_names = list(inputs.keys())
            else:
                input_names = []

            params = input_names
            sig_parts = [f"({', '.join(params)})" if params else "()"]
            label = f"{callable_sym.name}{''.join(sig_parts)}"
            param_details = [f"Arg: {p}" for p in params]

        elif isinstance(callable_sym, PlaybookStep):
            step_inputs = getattr(callable_sym, "inputs", {})
            if isinstance(step_inputs, dict):
                params = list(step_inputs.keys())
            param_details = [f"Param: {p}" for p in params]

        active_label = getattr(callable_sym, "name", label)

        if not params:
            return SignatureInformation(
                label=f"{active_label}()",
                documentation=str(doc)[:500] if doc else "",
                parameters=[],
            )

        sig_label = f"{active_label}({', '.join(params)})"
        parameters = [
            ParameterInformation(
                label=param_name,
                documentation=param_doc if param_doc else "",
            )
            for param_name, param_doc in zip(params, param_details or [""] * len(params))
        ]

        return SignatureInformation(
            label=sig_label,
            documentation=str(doc)[:500] if doc else "",
            parameters=parameters,
        )
