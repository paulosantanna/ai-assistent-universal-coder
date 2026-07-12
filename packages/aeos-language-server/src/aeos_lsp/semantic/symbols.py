from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Union

from aeos_lsp.semantic.models import (
    Agent,
    AgentLayer,
    ApprovalRequirement,
    Artifact,
    Command,
    Dependency,
    EvidenceRequirement,
    ExecutionTarget,
    Input,
    JudgeRule,
    ModelProfile,
    Output,
    Permission,
    Playbook,
    PlaybookStep,
    Policy,
    QualityGate,
    Registry,
    Repository,
    RollbackDefinition,
    Skill,
    SymbolKind,
    TokenBudget,
    Tool,
    Variable,
    Workspace,
)

SemanticSymbol = Union[
    Workspace,
    Repository,
    Agent,
    AgentLayer,
    Skill,
    Playbook,
    PlaybookStep,
    Tool,
    Command,
    Policy,
    Permission,
    Registry,
    ModelProfile,
    TokenBudget,
    QualityGate,
    JudgeRule,
    EvidenceRequirement,
    Artifact,
    Variable,
    Input,
    Output,
    Dependency,
    ExecutionTarget,
    ApprovalRequirement,
    RollbackDefinition,
]


def _symbol_name(sym: SemanticSymbol) -> str:
    return getattr(sym, "name", str(sym.stable_id))


def _symbol_kind(sym: SemanticSymbol) -> SymbolKind:
    if hasattr(sym, "symbol_kind"):
        return sym.symbol_kind
    if hasattr(sym, "kind"):
        return sym.kind
    return SymbolKind.UNKNOWN


def _symbol_uri(sym: SemanticSymbol) -> str:
    return getattr(sym, "source_uri", "")


class SymbolVisitor(ABC):
    @abstractmethod
    def visit_workspace(self, symbol: Workspace) -> Any: ...
    @abstractmethod
    def visit_repository(self, symbol: Repository) -> Any: ...
    @abstractmethod
    def visit_agent(self, symbol: Agent) -> Any: ...
    @abstractmethod
    def visit_agent_layer(self, symbol: AgentLayer) -> Any: ...
    @abstractmethod
    def visit_skill(self, symbol: Skill) -> Any: ...
    @abstractmethod
    def visit_playbook(self, symbol: Playbook) -> Any: ...
    @abstractmethod
    def visit_playbook_step(self, symbol: PlaybookStep) -> Any: ...
    @abstractmethod
    def visit_tool(self, symbol: Tool) -> Any: ...
    @abstractmethod
    def visit_command(self, symbol: Command) -> Any: ...
    @abstractmethod
    def visit_policy(self, symbol: Policy) -> Any: ...
    @abstractmethod
    def visit_permission(self, symbol: Permission) -> Any: ...
    @abstractmethod
    def visit_registry(self, symbol: Registry) -> Any: ...
    @abstractmethod
    def visit_model_profile(self, symbol: ModelProfile) -> Any: ...
    @abstractmethod
    def visit_token_budget(self, symbol: TokenBudget) -> Any: ...
    @abstractmethod
    def visit_quality_gate(self, symbol: QualityGate) -> Any: ...
    @abstractmethod
    def visit_judge_rule(self, symbol: JudgeRule) -> Any: ...
    @abstractmethod
    def visit_evidence_requirement(self, symbol: EvidenceRequirement) -> Any: ...
    @abstractmethod
    def visit_artifact(self, symbol: Artifact) -> Any: ...
    @abstractmethod
    def visit_variable(self, symbol: Variable) -> Any: ...
    @abstractmethod
    def visit_input(self, symbol: Input) -> Any: ...
    @abstractmethod
    def visit_output(self, symbol: Output) -> Any: ...
    @abstractmethod
    def visit_dependency(self, symbol: Dependency) -> Any: ...
    @abstractmethod
    def visit_execution_target(self, symbol: ExecutionTarget) -> Any: ...
    @abstractmethod
    def visit_approval_requirement(self, symbol: ApprovalRequirement) -> Any: ...
    @abstractmethod
    def visit_rollback_definition(self, symbol: RollbackDefinition) -> Any: ...


def accept_visitor(symbol: SemanticSymbol, visitor: SymbolVisitor) -> Any:
    dispatch = {
        Workspace: visitor.visit_workspace,
        Repository: visitor.visit_repository,
        Agent: visitor.visit_agent,
        AgentLayer: visitor.visit_agent_layer,
        Skill: visitor.visit_skill,
        Playbook: visitor.visit_playbook,
        PlaybookStep: visitor.visit_playbook_step,
        Tool: visitor.visit_tool,
        Command: visitor.visit_command,
        Policy: visitor.visit_policy,
        Permission: visitor.visit_permission,
        Registry: visitor.visit_registry,
        ModelProfile: visitor.visit_model_profile,
        TokenBudget: visitor.visit_token_budget,
        QualityGate: visitor.visit_quality_gate,
        JudgeRule: visitor.visit_judge_rule,
        EvidenceRequirement: visitor.visit_evidence_requirement,
        Artifact: visitor.visit_artifact,
        Variable: visitor.visit_variable,
        Input: visitor.visit_input,
        Output: visitor.visit_output,
        Dependency: visitor.visit_dependency,
        ExecutionTarget: visitor.visit_execution_target,
        ApprovalRequirement: visitor.visit_approval_requirement,
        RollbackDefinition: visitor.visit_rollback_definition,
    }
    handler = dispatch.get(type(symbol))
    if handler is not None:
        return handler(symbol)
    msg = f"No visitor method for {type(symbol).__name__}"
    raise TypeError(msg)


@dataclass
class SymbolTable:
    _lock: threading.RLock = field(default_factory=threading.RLock)
    _by_id: dict[str, SemanticSymbol] = field(default_factory=dict)
    _by_kind: dict[SymbolKind, list[SemanticSymbol]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _by_uri: dict[str, list[SemanticSymbol]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _by_name: dict[str, list[SemanticSymbol]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add(self, symbol: SemanticSymbol) -> None:
        with self._lock:
            sid = symbol.stable_id
            self._by_id[sid] = symbol
            kind = _symbol_kind(symbol)
            self._by_kind[kind].append(symbol)
            uri = _symbol_uri(symbol)
            if uri:
                self._by_uri[uri].append(symbol)
            name = _symbol_name(symbol)
            self._by_name[name].append(symbol)

    def remove(self, stable_id: str) -> bool:
        with self._lock:
            symbol = self._by_id.pop(stable_id, None)
            if symbol is None:
                return False
            kind = _symbol_kind(symbol)
            uri = _symbol_uri(symbol)
            name = _symbol_name(symbol)
            self._remove_from_list(self._by_kind[kind], symbol)
            if uri:
                self._remove_from_list(self._by_uri[uri], symbol)
            self._remove_from_list(self._by_name[name], symbol)
            return True

    def remove_by_uri(self, uri: str) -> int:
        with self._lock:
            symbols = list(self._by_uri.get(uri, []))
            count = 0
            for sym in symbols:
                if self.remove(sym.stable_id):
                    count += 1
            return count

    def get(self, stable_id: str) -> SemanticSymbol | None:
        with self._lock:
            return self._by_id.get(stable_id)

    def get_by_kind(self, kind: SymbolKind) -> list[SemanticSymbol]:
        with self._lock:
            return list(self._by_kind.get(kind, []))

    def get_by_uri(self, uri: str) -> list[SemanticSymbol]:
        with self._lock:
            return list(self._by_uri.get(uri, []))

    def get_by_name(self, name: str) -> list[SemanticSymbol]:
        with self._lock:
            return list(self._by_name.get(name, []))

    def get_by_name_and_kind(self, name: str, kind: SymbolKind) -> list[SemanticSymbol]:
        with self._lock:
            return [s for s in self._by_name.get(name, []) if _symbol_kind(s) == kind]

    def has_id(self, stable_id: str) -> bool:
        with self._lock:
            return stable_id in self._by_id

    def all_symbols(self) -> list[SemanticSymbol]:
        with self._lock:
            return list(self._by_id.values())

    def count(self) -> int:
        with self._lock:
            return len(self._by_id)

    def clear(self) -> None:
        with self._lock:
            self._by_id.clear()
            self._by_kind.clear()
            self._by_uri.clear()
            self._by_name.clear()

    def get_uris(self) -> list[str]:
        with self._lock:
            return list(self._by_uri.keys())

    @staticmethod
    def _remove_from_list(lst: list[SemanticSymbol], symbol: SemanticSymbol) -> None:
        try:
            lst.remove(symbol)
        except ValueError:
            pass
