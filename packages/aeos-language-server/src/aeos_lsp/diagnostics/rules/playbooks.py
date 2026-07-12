from __future__ import annotations

from collections import Counter

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Playbook, PlaybookStep, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class PlaybookNotRegisteredRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0014",
        name="playbook-not-registered",
        description="Detects playbook references that are not registered in the playbook registry",
        severity=DiagnosticSeverity.Warning,
        category="registrations",
        version="1.0.0",
        check_workspace=True,
        tags=("playbooks", "registry"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        playbooks = semantic_model.get_symbols_by_kind(SymbolKind.PLAYBOOK)
        registries = semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)

        registered_names: set[str] = set()
        registered_ids: set[str] = set()
        for reg in registries:
            if hasattr(reg, "registry_type") and "playbook" in reg.registry_type.lower():
                entries = getattr(reg, "entries", {})
                if isinstance(entries, dict):
                    registered_names.update(entries.keys())
                    for val in entries.values():
                        if isinstance(val, dict):
                            ref = val.get("ref") or val.get("$ref") or val.get("implementation", "")
                            if ref:
                                registered_ids.add(ref)

        for pb in playbooks:
            if cancellation_token and cancellation_token.cancelled:
                break

            pb_name = getattr(pb, "name", "")
            pb_id = getattr(pb, "stable_id", "")

            if pb_name not in registered_names and pb_id not in registered_ids:
                sr = getattr(pb, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0014: Playbook '{pb_name}' is not registered in any playbook registry",
                        source="aeos-lsp",
                    ))

        return diagnostics

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        return []


class UnreachableStepRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0038",
        name="unreachable-step",
        description="Detects playbook steps that are unreachable due to conditions or flow control",
        severity=DiagnosticSeverity.Warning,
        category="playbooks",
        version="1.0.0",
        tags=("playbooks", "steps", "reachability"),
    )

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        symbols = semantic_model.get_symbols_by_uri(document_uri)
        playbook_steps: list[PlaybookStep] = [s for s in symbols if isinstance(s, PlaybookStep)]
        playbooks_list: list[Playbook] = [s for s in symbols if isinstance(s, Playbook)]

        # Find steps that follow a step with no conditions in a playbook flow
        for pb in playbooks_list:
            steps_in_pb = [s for s in playbook_steps if pb.stable_id in getattr(s, "stable_id", "")]
            condition_after_counter = 0
            consecutive_conditional = 0

            for i, step in enumerate(steps_in_pb):
                if cancellation_token and cancellation_token.cancelled:
                    break

                if i > 0:
                    prev_step = steps_in_pb[i - 1]
                    prev_conditions = prev_step.conditions
                    prev_has_return = any("return" in c.lower() for c in prev_conditions)
                    prev_has_exit = any("exit" in c.lower() for c in prev_conditions)
                    prev_has_fail = any("fail" in c.lower() for c in prev_conditions)

                    if prev_has_return or prev_has_exit or prev_has_fail:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0038: Step '{step.name}' may be unreachable: previous step '{prev_step.name}' has a terminal condition",
                            source="aeos-lsp",
                        ))

        return diagnostics


class StepWithoutExecutorRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0039",
        name="step-without-executor",
        description="Detects playbook steps that lack a required executor",
        severity=DiagnosticSeverity.Error,
        category="playbooks",
        version="1.0.0",
        tags=("playbooks", "steps", "executor"),
    )

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        symbols = semantic_model.get_symbols_by_uri(document_uri)
        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, PlaybookStep):
                if not sym.executor:
                    if sym.step_type and sym.step_type not in ("noop", "wait", "sleep", "manual"):
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0039: Step '{sym.name}' is missing a required executor",
                            source="aeos-lsp",
                        ))

                # Check if executor is resolvable
                if sym.executor:
                    result = semantic_model.resolver.resolve_by_name(sym.executor)
                    if not result.resolved:
                        result = semantic_model.resolver.resolve_by_id(sym.executor)
                        if not result.resolved:
                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=0, character=0),
                                    end=Position(line=0, character=1),
                                ),
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0039: Step '{sym.name}' references executor '{sym.executor}' which could not be resolved",
                                source="aeos-lsp",
                            ))

        return diagnostics
