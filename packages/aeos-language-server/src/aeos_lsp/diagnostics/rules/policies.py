from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Agent, PlaybookStep, Policy, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class PolicyDeniesOperationRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0017",
        name="policy-denies-operation",
        description="Detects operations that are denied by workspace policies",
        severity=DiagnosticSeverity.Error,
        category="policies",
        version="1.0.0",
        tags=("policies", "compliance"),
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

        policies = semantic_model.get_symbols_by_kind(SymbolKind.POLICY)
        symbols = semantic_model.get_symbols_by_uri(document_uri)

        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, (Agent, Skill)):
                visibility = getattr(sym, "visibility", None)
                if visibility is not None:
                    vis_str = str(visibility.value if hasattr(visibility, "value") else visibility)
                    for policy in policies:
                        if isinstance(policy, Policy):
                            policy_rules = getattr(policy, "rules", {})
                            if isinstance(policy_rules, dict):
                                denial = self._check_policy_denial(
                                    policy_rules, "visibility", vis_str, type(sym).__name__.lower()
                                )
                                if denial:
                                    sr = getattr(sym, "selection_range", None)
                                    if sr is not None:
                                        diagnostics.append(Diagnostic(
                                            range=sr,
                                            severity=DiagnosticSeverity.Error,
                                            code=self.metadata.code,
                                            message=f"AEOS0017: Policy '{policy.name}' denies {type(sym).__name__.lower()} '{sym.name}' with visibility '{vis_str}'",
                                            source="aeos-lsp",
                                        ))

            elif isinstance(sym, PlaybookStep):
                step_type = getattr(sym, "step_type", "")
                for policy in policies:
                    if isinstance(policy, Policy):
                        policy_rules = getattr(policy, "rules", {})
                        if isinstance(policy_rules, dict):
                            denial = self._check_policy_denial(
                                policy_rules, "step_type", step_type, "step"
                            )
                            if denial:
                                diagnostics.append(Diagnostic(
                                    range=Range(
                                        start=Position(line=0, character=0),
                                        end=Position(line=0, character=1),
                                    ),
                                    severity=DiagnosticSeverity.Error,
                                    code=self.metadata.code,
                                    message=f"AEOS0017: Policy '{policy.name}' denies step type '{step_type}' in step '{sym.name}'",
                                    source="aeos-lsp",
                                ))

        return diagnostics

    @staticmethod
    def _check_policy_denial(
        rules: dict,
        field: str,
        value: str,
        resource_type: str,
    ) -> bool:
        denials = rules.get("deny", rules.get("denied", rules.get("denies", [])))
        if isinstance(denials, list):
            for denial in denials:
                if isinstance(denial, dict):
                    if denial.get("field") == field and denial.get("value") == value:
                        return True
                    if denial.get("resource") == resource_type and denial.get("field") == field and denial.get("value") == value:
                        return True
        elif isinstance(denials, dict):
            if denials.get(field) == value:
                return True
            resource_denials = denials.get(resource_type, {})
            if isinstance(resource_denials, dict) and resource_denials.get(field) == value:
                return True
        return False
