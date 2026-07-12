from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    Hover,
    HoverParams,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
    DeprecationStatus,
    Input,
    ModelProfile,
    Output,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
    TokenBudget,
    Tool,
    Variable,
)
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.symbols import SemanticSymbol


class HoverFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_hover(self, params: HoverParams) -> Hover | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            lines = self._build_hover_content(symbol)
            range_ = getattr(symbol, "selection_range", None)

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(lines),
                ),
                range=range_,
            )

    def _build_hover_content(self, symbol: SemanticSymbol) -> list[str]:
        lines: list[str] = []
        kind = self._get_kind(symbol)
        name = getattr(symbol, "name", symbol.stable_id)
        stable_id = getattr(symbol, "stable_id", "")
        source_uri = getattr(symbol, "source_uri", "")

        lines.append(f"**{kind.value}**: `{name}`")
        lines.append("")
        if stable_id and stable_id != name:
            lines.append(f"*ID:* `{stable_id}`")
        if source_uri:
            lines.append(f"*Source:* `{source_uri}`")

        doc = getattr(symbol, "documentation", "") or getattr(symbol, "description", "")
        if doc:
            lines.append("")
            lines.append(str(doc))

        deprecation = getattr(symbol, "deprecation", None)
        if deprecation and isinstance(deprecation, DeprecationStatus) and deprecation != DeprecationStatus.CURRENT:
            lines.append("")
            lines.append(f"*Status:* `{deprecation.value}`")

        visibility = getattr(symbol, "visibility", None)
        if visibility:
            v = visibility.value if hasattr(visibility, "value") else str(visibility)
            lines.append(f"*Visibility:* `{v}`")

        if isinstance(symbol, Agent):
            if symbol.parent_id:
                parent_result = self._semantic_model.resolver.resolve_by_id(symbol.parent_id)
                if parent_result.resolved:
                    pname = getattr(parent_result.symbol, "name", symbol.parent_id)
                    lines.append(f"*Extends:* `{pname}`")
                else:
                    lines.append(f"*Extends:* `{symbol.parent_id}` (unresolved)")
            if symbol.skills:
                lines.append(f"*Skills:* {', '.join(f'`{s}`' for s in symbol.skills)}")
            refs = getattr(symbol, "references", [])
            if refs:
                lines.append(f"*References:* {len(refs)}")
        elif isinstance(symbol, Skill):
            if symbol.tools:
                lines.append(f"*Tools:* {', '.join(f'`{t}`' for t in symbol.tools)}")
            if symbol.inputs:
                lines.append(f"*Inputs:* {', '.join(f'`{i}`' for i in symbol.inputs)}")
            if symbol.outputs:
                lines.append(f"*Outputs:* {', '.join(f'`{o}`' for o in symbol.outputs)}")
        elif isinstance(symbol, Playbook):
            if symbol.steps:
                lines.append(f"*Steps:* {len(symbol.steps)}")
            if symbol.variables:
                lines.append(f"*Variables:* {', '.join(f'`{v}`' for v in symbol.variables)}")
        elif isinstance(symbol, PlaybookStep):
            if symbol.tool:
                lines.append(f"*Tool:* `{symbol.tool}`")
            if symbol.skill:
                lines.append(f"*Skill:* `{symbol.skill}`")
            if symbol.playbook:
                lines.append(f"*Playbook:* `{symbol.playbook}`")
            if symbol.timeout:
                lines.append(f"*Timeout:* {symbol.timeout}s")
            if symbol.retry:
                lines.append(f"*Retry:* {symbol.retry}")
            if symbol.approval:
                lines.append(f"*Approval:* Required")
            if symbol.rollback:
                lines.append(f"*Rollback:* `{symbol.rollback}`")
        elif isinstance(symbol, Tool):
            if symbol.command:
                lines.append(f"*Command:* `{symbol.command}`")
            if symbol.mutating:
                lines.append("*Mutating:* Yes")
            if symbol.timeout:
                lines.append(f"*Timeout:* {symbol.timeout}s")
            if symbol.description:
                lines.append("")
                lines.append(str(symbol.description))
        elif isinstance(symbol, Variable):
            lines.append(f"*Type:* {symbol.type_ref or 'any'}")
            if symbol.default is not None:
                lines.append(f"*Default:* `{symbol.default}`")
        elif isinstance(symbol, (Input, Output)):
            lines.append(f"*Type:* {symbol.type_ref or 'any'}")
            if hasattr(symbol, "required") and symbol.required:
                lines.append("*Required:* Yes")
        elif isinstance(symbol, ModelProfile):
            lines.append(f"*Provider:* {symbol.provider or 'unknown'}")
            if symbol.context_window:
                lines.append(f"*Context:* {symbol.context_window} tokens")
            if symbol.max_tokens:
                lines.append(f"*Max output:* {symbol.max_tokens} tokens")
        elif isinstance(symbol, TokenBudget):
            if symbol.max_total_tokens:
                lines.append(f"*Max total:* {symbol.max_total_tokens} tokens")
            if symbol.max_input_tokens:
                lines.append(f"*Max input:* {symbol.max_input_tokens} tokens")
            if symbol.max_output_tokens:
                lines.append(f"*Max output:* {symbol.max_output_tokens} tokens")

        metadata = getattr(symbol, "metadata", {}) or {}
        if isinstance(metadata, dict) and metadata:
            lines.append("")
            lines.append("*Metadata:*")
            for k, v in metadata.items():
                lines.append(f"  - `{k}`: {v}")

        registry = getattr(symbol, "registry", None) or getattr(symbol, "registry_type", None)
        if registry:
            lines.append("")
            lines.append(f"*Registry:* `{registry}`")

        return lines

    @staticmethod
    def _get_kind(symbol: SemanticSymbol) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN
