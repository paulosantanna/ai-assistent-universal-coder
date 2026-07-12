from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    DefinitionParams,
    Location,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
    Tool,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class DefinitionFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_definition(self, params: DefinitionParams) -> list[Location] | Location | None:
        uri = params.text_document.uri
        pos = params.position

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            locations: list[Location] = []

            if isinstance(symbol, Agent):
                if symbol.parent_id:
                    parent = self._semantic_model.resolver.resolve_by_id(symbol.parent_id)
                    if parent.resolved and parent.symbol is not None:
                        locations.append(self._to_location(parent.symbol))

                for skill_id in symbol.skills:
                    skill = self._semantic_model.resolver.resolve_by_id(skill_id)
                    if skill.resolved and skill.symbol is not None:
                        locations.append(self._to_location(skill.symbol))

                locations.insert(0, self._to_location(symbol))

            elif isinstance(symbol, Skill):
                for tool_id in symbol.tools:
                    tool = self._semantic_model.resolver.resolve_by_id(tool_id)
                    if tool.resolved and tool.symbol is not None:
                        locations.append(self._to_location(tool.symbol))

                if not locations:
                    locations.append(self._to_location(symbol))

            elif isinstance(symbol, Playbook):
                for step_id in symbol.steps:
                    step = self._semantic_model.resolver.resolve_by_id(step_id)
                    if step.resolved and step.symbol is not None:
                        locations.append(self._to_location(step.symbol))

                if not locations:
                    locations.append(self._to_location(symbol))

            elif isinstance(symbol, PlaybookStep):
                if symbol.tool:
                    tool = self._semantic_model.resolver.resolve_by_name(symbol.tool, SymbolKind.TOOL)
                    if tool.resolved and tool.symbol is not None:
                        locations.append(self._to_location(tool.symbol))
                if symbol.skill:
                    skill = self._semantic_model.resolver.resolve_by_name(symbol.skill, SymbolKind.SKILL)
                    if skill.resolved and skill.symbol is not None:
                        locations.append(self._to_location(skill.symbol))
                if symbol.playbook:
                    pb = self._semantic_model.resolver.resolve_by_name(symbol.playbook, SymbolKind.PLAYBOOK)
                    if pb.resolved and pb.symbol is not None:
                        locations.append(self._to_location(pb.symbol))

                if not locations:
                    locations.append(self._to_location(symbol))

            else:
                locations.append(self._to_location(symbol))

            if len(locations) == 1:
                return locations[0]

            return locations if locations else None

    def _to_location(self, symbol: Any) -> Location:
        uri = getattr(symbol, "source_uri", "")
        range_ = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
        if range_ is None:
            range_ = Range(start=Position(line=0, character=0), end=Position(line=0, character=0))
        return Location(uri=uri, range=range_)
