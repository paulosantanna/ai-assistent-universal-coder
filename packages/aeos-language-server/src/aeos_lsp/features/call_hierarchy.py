from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    CallHierarchyIncomingCall,
    CallHierarchyIncomingCallsParams,
    CallHierarchyItem,
    CallHierarchyOutgoingCall,
    CallHierarchyOutgoingCallsParams,
    CallHierarchyPrepareParams,
    Position,
    Range,
    SymbolKind as LspSymbolKind,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
    Tool,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


_KIND_MAPPING: dict[SymbolKind, LspSymbolKind] = {
    SymbolKind.AGENT: LspSymbolKind.Class,
    SymbolKind.SKILL: LspSymbolKind.Function,
    SymbolKind.PLAYBOOK: LspSymbolKind.Method,
    SymbolKind.TOOL: LspSymbolKind.Function,
    SymbolKind.COMMAND: LspSymbolKind.Function,
}


class CallHierarchyFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def prepare_call_hierarchy(self, params: CallHierarchyPrepareParams) -> list[CallHierarchyItem] | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            kind = self._get_kind(symbol)
            if kind not in (SymbolKind.PLAYBOOK, SymbolKind.SKILL, SymbolKind.TOOL, SymbolKind.PLAYBOOK_STEP):
                return None

            item = self._to_call_hierarchy_item(symbol)
            return [item] if item is not None else None

    def provide_incoming_calls(self, params: CallHierarchyIncomingCallsParams) -> list[CallHierarchyIncomingCall] | None:
        item = params.item
        symbol_name = item.name
        symbol_uri = item.uri

        with self._lock:
            incoming: list[CallHierarchyIncomingCall] = []

            for sym in self._semantic_model.symbol_table.all_symbols():
                if isinstance(sym, Playbook):
                    for step_id in sym.steps:
                        step = self._semantic_model.resolver.resolve_by_id(step_id)
                        if step.resolved and step.symbol is not None:
                            if isinstance(step.symbol, PlaybookStep):
                                if (step.symbol.skill == symbol_name or
                                        step.symbol.tool == symbol_name or
                                        step.symbol.playbook == symbol_name):
                                    caller_item = self._to_call_hierarchy_item(sym)
                                    if caller_item is not None:
                                        from_ranges = self._step_ranges(step.symbol)
                                        incoming.append(CallHierarchyIncomingCall(
                                            from_=caller_item,
                                            from_ranges=from_ranges,
                                        ))

                elif isinstance(sym, Skill):
                    if symbol_name in getattr(sym, "tools", []):
                        caller_item = self._to_call_hierarchy_item(sym)
                        if caller_item is not None:
                            from_ranges = [getattr(sym, "selection_range", None) or getattr(sym, "full_range", Range(start=Position(0, 0), end=Position(0, 0)))]
                            incoming.append(CallHierarchyIncomingCall(
                                from_=caller_item,
                                from_ranges=from_ranges,
                            ))

                elif isinstance(sym, PlaybookStep):
                    if sym.skill == symbol_name or sym.tool == symbol_name:
                        caller_item = self._to_call_hierarchy_item(sym)
                        if caller_item is not None:
                            from_ranges = self._step_ranges(sym)
                            incoming.append(CallHierarchyIncomingCall(
                                from_=caller_item,
                                from_ranges=from_ranges,
                            ))

            return incoming if incoming else None

    def provide_outgoing_calls(self, params: CallHierarchyOutgoingCallsParams) -> list[CallHierarchyOutgoingCall] | None:
        item = params.item
        symbol_uri = item.uri

        with self._lock:
            outgoing: list[CallHierarchyOutgoingCall] = []

            for sym in self._semantic_model.symbol_table.all_symbols():
                source_uri = getattr(sym, "source_uri", "")
                if source_uri != symbol_uri:
                    continue

                if isinstance(sym, Playbook):
                    for step_id in sym.steps:
                        step = self._semantic_model.resolver.resolve_by_id(step_id)
                        if step.resolved and step.symbol is not None and isinstance(step.symbol, PlaybookStep):
                            target = self._resolve_step_target(step.symbol)
                            if target is not None:
                                from_ranges = self._step_ranges(step.symbol)
                                outgoing.append(CallHierarchyOutgoingCall(
                                    to=target,
                                    from_ranges=from_ranges,
                                ))

                elif isinstance(sym, Skill):
                    for tool_id in sym.tools:
                        tool = self._semantic_model.resolver.resolve_by_id(tool_id)
                        if tool.resolved and tool.symbol is not None:
                            target = self._to_call_hierarchy_item(tool.symbol)
                            if target is not None:
                                outgoing.append(CallHierarchyOutgoingCall(
                                    to=target,
                                    from_ranges=[getattr(sym, "selection_range", None) or getattr(sym, "full_range", Range(start=Position(0, 0), end=Position(0, 0)))],
                                ))

                elif isinstance(sym, PlaybookStep):
                    target = self._resolve_step_target(sym)
                    if target is not None:
                        from_ranges = self._step_ranges(sym)
                        outgoing.append(CallHierarchyOutgoingCall(
                            to=target,
                            from_ranges=from_ranges,
                        ))

            return outgoing if outgoing else None

    def _resolve_step_target(self, step: PlaybookStep) -> CallHierarchyItem | None:
        if step.skill:
            skill = self._semantic_model.resolver.resolve_by_name(step.skill, SymbolKind.SKILL)
            if skill.resolved and skill.symbol is not None:
                return self._to_call_hierarchy_item(skill.symbol)
        if step.tool:
            tool = self._semantic_model.resolver.resolve_by_name(step.tool, SymbolKind.TOOL)
            if tool.resolved and tool.symbol is not None:
                return self._to_call_hierarchy_item(tool.symbol)
        if step.playbook:
            pb = self._semantic_model.resolver.resolve_by_name(step.playbook, SymbolKind.PLAYBOOK)
            if pb.resolved and pb.symbol is not None:
                return self._to_call_hierarchy_item(pb.symbol)
        return None

    def _to_call_hierarchy_item(self, symbol: Any) -> CallHierarchyItem | None:
        name = getattr(symbol, "name", symbol.stable_id)
        kind = self._get_kind(symbol)
        lsp_kind = _KIND_MAPPING.get(kind, LspSymbolKind.Function)
        uri = getattr(symbol, "source_uri", "")
        sr = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
        if sr is None:
            return None

        detail = f"({kind.value}) {getattr(symbol, 'stable_id', '')}"

        return CallHierarchyItem(
            name=str(name),
            kind=lsp_kind,
            tags=None,
            detail=detail,
            uri=uri,
            range=getattr(symbol, "full_range", sr) or sr,
            selection_range=sr,
        )

    def _step_ranges(self, step: PlaybookStep) -> list[Range]:
        sr = getattr(step, "selection_range", None) or getattr(step, "full_range", None)
        return [sr] if sr else [Range(start=Position(0, 0), end=Position(0, 0))]

    @staticmethod
    def _get_kind(symbol: Any) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN
