from __future__ import annotations

from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Agent, Playbook, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class AgentInheritanceCycleRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0006",
        name="agent-inheritance-cycle",
        description="Detects circular inheritance in agent hierarchies",
        severity=DiagnosticSeverity.Error,
        category="cycles",
        version="1.0.0",
        check_workspace=True,
        tags=("cycles", "inheritance", "agents"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        cycles = semantic_model.inheritance_graph.find_cycles()
        if not cycles:
            return diagnostics

        for cycle in cycles:
            if cancellation_token and cancellation_token.cancelled:
                break
            cycle_str = " -> ".join(cycle)
            for node_id in cycle:
                symbol = semantic_model.get_symbol_by_id(node_id)
                if symbol is not None:
                    sr = getattr(symbol, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0006: Circular inheritance detected: {cycle_str}",
                            source="aeos-lsp",
                        ))

        return diagnostics


class PlaybookCycleRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0007",
        name="playbook-cycle",
        description="Detects circular dependencies between playbooks",
        severity=DiagnosticSeverity.Error,
        category="cycles",
        version="1.0.0",
        check_workspace=True,
        tags=("cycles", "playbooks"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        cycles = semantic_model.dependency_graph.find_cycles()
        if not cycles:
            return diagnostics

        playbook_ids = _get_ids_by_kind(semantic_model, SymbolKind.PLAYBOOK)
        step_ids = _get_ids_by_kind(semantic_model, SymbolKind.PLAYBOOK_STEP)

        for cycle in cycles:
            if cancellation_token and cancellation_token.cancelled:
                break
            cycle_set = set(cycle)
            if not any(cid in playbook_ids for cid in cycle_set):
                if not any(cid in step_ids for cid in cycle_set):
                    continue

            cycle_str = " -> ".join(cycle)
            for node_id in cycle:
                symbol = semantic_model.get_symbol_by_id(node_id)
                if symbol is not None:
                    sr = getattr(symbol, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0007: Circular playbook dependency detected: {cycle_str}",
                            source="aeos-lsp",
                        ))

        return diagnostics


class SkillCycleRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0008",
        name="skill-dependency-cycle",
        description="Detects circular dependencies between skills",
        severity=DiagnosticSeverity.Error,
        category="cycles",
        version="1.0.0",
        check_workspace=True,
        tags=("cycles", "skills"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        skill_ids = _get_ids_by_kind(semantic_model, SymbolKind.SKILL)
        cycles = semantic_model.dependency_graph.find_cycles()

        for cycle in cycles:
            if cancellation_token and cancellation_token.cancelled:
                break
            cycle_set = set(cycle)
            if not any(cid in skill_ids for cid in cycle_set):
                continue

            cycle_str = " -> ".join(cycle)
            for node_id in cycle:
                symbol = semantic_model.get_symbol_by_id(node_id)
                if symbol is not None:
                    sr = getattr(symbol, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0008: Circular skill dependency detected: {cycle_str}",
                            source="aeos-lsp",
                        ))

        return diagnostics


class DependencyCycleRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0009",
        name="general-dependency-cycle",
        description="Detects general circular dependencies in the dependency graph",
        severity=DiagnosticSeverity.Error,
        category="cycles",
        version="1.0.0",
        check_workspace=True,
        tags=("cycles", "dependencies"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        if not semantic_model.has_cycles():
            return diagnostics

        cycles = semantic_model.dependency_graph.find_cycles()
        for cycle in cycles:
            if cancellation_token and cancellation_token.cancelled:
                break

            cycle_str = " -> ".join(cycle)
            for node_id in cycle:
                symbol = semantic_model.get_symbol_by_id(node_id)
                if symbol is not None:
                    sr = getattr(symbol, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0009: Circular dependency detected: {cycle_str}",
                            source="aeos-lsp",
                        ))

        return diagnostics


def _get_ids_by_kind(semantic_model: SemanticModel, kind: SymbolKind) -> set[str]:
    ids: set[str] = set()
    symbols = semantic_model.get_symbols_by_kind(kind)
    for sym in symbols:
        sid = getattr(sym, "stable_id", "")
        if sid:
            ids.add(sid)
    return ids
