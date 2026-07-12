from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

from aeos_lsp.semantic.models import (
    Agent,
    AgentLayer,
    Playbook,
    PlaybookStep,
    Registry,
    Skill,
    SymbolKind,
    Tool,
    Variable,
)
from aeos_lsp.semantic.symbols import SemanticSymbol, SymbolTable


class AmbiguousReference(Exception):
    def __init__(self, message: str, candidates: list[SemanticSymbol]) -> None:
        self.candidates = candidates
        super().__init__(message)


class UnresolvedReference(Exception):
    pass


@dataclass(frozen=True)
class ResolutionResult:
    resolved: bool
    symbol: SemanticSymbol | None = None
    candidates: list[SemanticSymbol] = field(default_factory=list)
    error: str | None = None


class CrossReferenceResolver:
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._lock = threading.RLock()
        self._resolve_cache: dict[str, ResolutionResult] = {}
        self._cache_limit: int = 4096

    @property
    def symbol_table(self) -> SymbolTable:
        return self._symbol_table

    def resolve_by_name(self, name: str, kind: SymbolKind | None = None) -> ResolutionResult:
        with self._lock:
            cache_key = f"name:{name}:{kind.value if kind else '*'}"
            cached = self._resolve_cache.get(cache_key)
            if cached is not None:
                return cached

            if kind is not None:
                candidates = self._symbol_table.get_by_name_and_kind(name, kind)
            else:
                candidates = self._symbol_table.get_by_name(name)

            if len(candidates) == 0:
                result = ResolutionResult(resolved=False, error=f"Unresolved symbol: {name}")
            elif len(candidates) == 1:
                result = ResolutionResult(resolved=True, symbol=candidates[0])
            else:
                result = ResolutionResult(
                    resolved=True,
                    candidates=candidates,
                    error=f"Ambiguous reference: {name} has {len(candidates)} candidates",
                )

            if len(self._resolve_cache) >= self._cache_limit:
                self._resolve_cache.clear()
            self._resolve_cache[cache_key] = result
            return result

    def resolve_by_id(self, stable_id: str) -> ResolutionResult:
        with self._lock:
            cache_key = f"id:{stable_id}"
            cached = self._resolve_cache.get(cache_key)
            if cached is not None:
                return cached

            symbol = self._symbol_table.get(stable_id)
            if symbol is None:
                result = ResolutionResult(resolved=False, error=f"Unresolved stable_id: {stable_id}")
            else:
                result = ResolutionResult(resolved=True, symbol=symbol)

            if len(self._resolve_cache) >= self._cache_limit:
                self._resolve_cache.clear()
            self._resolve_cache[cache_key] = result
            return result

    def resolve_agent_parent(self, agent: Agent) -> ResolutionResult:
        if agent.parent_id is None:
            return ResolutionResult(resolved=False, error="Agent has no parent")
        return self.resolve_by_id(agent.parent_id)

    def resolve_agent_inheritance_chain(self, agent: Agent) -> list[Agent]:
        chain: list[Agent] = [agent]
        current = agent
        seen: set[str] = set()
        while current.parent_id is not None:
            if current.parent_id in seen:
                break
            seen.add(current.parent_id)
            result = self.resolve_by_id(current.parent_id)
            if result.resolved and isinstance(result.symbol, Agent):
                current = result.symbol
                chain.append(current)
            else:
                break
        return chain

    def resolve_agent_skills(self, agent: Agent) -> list[Skill]:
        resolved: list[Skill] = []
        for skill_id in agent.skills:
            result = self.resolve_by_id(skill_id)
            if result.resolved and isinstance(result.symbol, Skill):
                resolved.append(result.symbol)
        return resolved

    def resolve_agent_layers(self, agent: Agent) -> list[AgentLayer]:
        return list(agent.layers)

    def resolve_playbook_skills(self, playbook: Playbook) -> list[Skill]:
        resolved: list[Skill] = []
        for step_id in playbook.steps:
            result = self.resolve_by_id(step_id)
            if result.resolved and isinstance(result.symbol, PlaybookStep):
                step = result.symbol
                if step.skill is not None:
                    skill_result = self.resolve_by_name(step.skill, SymbolKind.SKILL)
                    if skill_result.resolved and isinstance(skill_result.symbol, Skill):
                        resolved.append(skill_result.symbol)
        return resolved

    def resolve_step_tool_chain(self, step: PlaybookStep) -> list[ResolutionResult]:
        results: list[ResolutionResult] = []
        if step.tool is not None:
            results.append(self.resolve_by_name(step.tool, SymbolKind.TOOL))
        if step.skill is not None:
            skill_result = self.resolve_by_name(step.skill, SymbolKind.SKILL)
            results.append(skill_result)
            if skill_result.resolved and isinstance(skill_result.symbol, Skill):
                skill = skill_result.symbol
                for tool_id in skill.tools:
                    results.append(self.resolve_by_id(tool_id))
        if step.playbook is not None:
            results.append(self.resolve_by_name(step.playbook, SymbolKind.PLAYBOOK))
        return results

    def resolve_playbook_tool_chain(self, playbook: Playbook) -> list[ResolutionResult]:
        results: list[ResolutionResult] = []
        for step_id in playbook.steps:
            result = self.resolve_by_id(step_id)
            if result.resolved and isinstance(result.symbol, PlaybookStep):
                chain = self.resolve_step_tool_chain(result.symbol)
                results.extend(chain)
        return results

    def resolve_registry_entry(self, registry: Registry, entry_name: str) -> ResolutionResult:
        if entry_name not in registry.entries:
            return ResolutionResult(resolved=False, error=f"Entry '{entry_name}' not found in registry '{registry.name}'")
        entry_val = registry.entries[entry_name]
        if isinstance(entry_val, dict):
            ref = entry_val.get("ref") or entry_val.get("$ref") or entry_val.get("implementation")
            if ref:
                return self.resolve_by_name(str(ref))
        return self.resolve_by_name(entry_name)

    def resolve_registry_entries(self, registry: Registry) -> list[ResolutionResult]:
        results: list[ResolutionResult] = []
        for entry_name in registry.entries:
            results.append(self.resolve_registry_entry(registry, entry_name))
        return results

    def resolve_variable_reference(self, var_name: str, scope_symbols: list[SemanticSymbol]) -> ResolutionResult:
        candidates = [
            s for s in scope_symbols
            if isinstance(s, Variable) and s.name == var_name
        ]
        if len(candidates) == 0:
            by_name = self._symbol_table.get_by_name(var_name)
            candidates = [s for s in by_name if isinstance(s, Variable)]
        if len(candidates) == 0:
            return ResolutionResult(resolved=False, error=f"Unresolved variable: {var_name}")
        if len(candidates) == 1:
            return ResolutionResult(resolved=True, symbol=candidates[0])
        return ResolutionResult(
            resolved=True,
            candidates=candidates,
            error=f"Ambiguous variable: {var_name}",
        )

    def resolve_output_to_producer(self, output_name: str, playbook: Playbook) -> ResolutionResult:
        candidates: list[SemanticSymbol] = []
        for step_id in playbook.steps:
            result = self.resolve_by_id(step_id)
            if result.resolved and isinstance(result.symbol, PlaybookStep):
                step = result.symbol
                if output_name in step.outputs:
                    candidates.append(result.symbol)
        if len(candidates) == 0:
            return ResolutionResult(resolved=False, error=f"No producer found for output: {output_name}")
        if len(candidates) == 1:
            return ResolutionResult(resolved=True, symbol=candidates[0])
        return ResolutionResult(
            resolved=True,
            candidates=candidates,
            error=f"Multiple producers for output: {output_name}",
        )

    def resolve_overlay_original(self, overlay_symbol: SemanticSymbol) -> ResolutionResult:
        stable_id = overlay_symbol.stable_id
        base_id = self._strip_overlay_suffix(stable_id)
        if base_id == stable_id:
            return ResolutionResult(resolved=False, error="Not an overlay symbol")
        return self.resolve_by_id(base_id)

    def invalidate_cache(self, stable_id: str | None = None) -> None:
        with self._lock:
            if stable_id is not None:
                self._resolve_cache = {
                    k: v for k, v in self._resolve_cache.items()
                    if stable_id not in k
                }
            else:
                self._resolve_cache.clear()

    def invalidate_for_uri(self, uri: str) -> None:
        with self._lock:
            self._resolve_cache = {
                k: v for k, v in self._resolve_cache.items()
                if uri not in k
            }

    @staticmethod
    def _strip_overlay_suffix(stable_id: str) -> str:
        overlay_prefixes = ("overlay:", "overlay.", "overlay/")
        for prefix in overlay_prefixes:
            if stable_id.startswith(prefix):
                return stable_id[len(prefix):]
        idx = stable_id.rfind("__overlay")
        if idx != -1:
            return stable_id[:idx]
        return stable_id

    def clear_cache(self) -> None:
        with self._lock:
            self._resolve_cache.clear()
