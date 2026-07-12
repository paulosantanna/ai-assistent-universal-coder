from __future__ import annotations

from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import ModelProfile, SymbolKind, TokenBudget
from aeos_lsp.semantic.semantic_model import SemanticModel


class InvalidBudgetRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0024",
        name="invalid-budget",
        description="Detects token budget configurations with invalid values",
        severity=DiagnosticSeverity.Error,
        category="token-budget",
        version="1.0.0",
        tags=("budget", "tokens"),
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
        budgets = [s for s in symbols if isinstance(s, TokenBudget)]

        for budget in budgets:
            if cancellation_token and cancellation_token.cancelled:
                break

            max_input = getattr(budget, "max_input_tokens", 0)
            max_output = getattr(budget, "max_output_tokens", 0)
            max_total = getattr(budget, "max_total_tokens", 0)

            if max_input < 0:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Error,
                        code=self.metadata.code,
                        message=f"AEOS0024: Token budget '{budget.name}' has negative max_input_tokens ({max_input})",
                        source="aeos-lsp",
                    ))

            if max_output < 0:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Error,
                        code=self.metadata.code,
                        message=f"AEOS0024: Token budget '{budget.name}' has negative max_output_tokens ({max_output})",
                        source="aeos-lsp",
                    ))

            if max_total < 0:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Error,
                        code=self.metadata.code,
                        message=f"AEOS0024: Token budget '{budget.name}' has negative max_total_tokens ({max_total})",
                        source="aeos-lsp",
                    ))

            if max_total > 0 and max_input + max_output > max_total:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0024: Token budget '{budget.name}' input+output ({max_input}+{max_output}) exceeds total ({max_total})",
                        source="aeos-lsp",
                    ))

        return diagnostics


class EstimateAboveBudgetRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0025",
        name="estimate-above-budget",
        description="Detects estimated token usage that exceeds the defined budget",
        severity=DiagnosticSeverity.Warning,
        category="token-budget",
        version="1.0.0",
        tags=("budget", "estimation"),
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
        budgets = [s for s in symbols if isinstance(s, TokenBudget)]

        # Estimate document token count
        estimated_tokens = _estimate_tokens(document_text)

        for budget in budgets:
            if cancellation_token and cancellation_token.cancelled:
                break

            max_input = getattr(budget, "max_input_tokens", 0)
            max_total = getattr(budget, "max_total_tokens", 0)

            if max_input > 0 and estimated_tokens > max_input:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0025: Estimated tokens ({estimated_tokens}) exceed max_input_tokens ({max_input}) for budget '{budget.name}'",
                        source="aeos-lsp",
                    ))

            if max_total > 0 and estimated_tokens * 2 > max_total:
                sr = getattr(budget, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0025: Estimated total tokens ({estimated_tokens * 2}) may exceed max_total_tokens ({max_total}) for budget '{budget.name}'",
                        source="aeos-lsp",
                    ))

        return diagnostics


class ContextWindowIncompatibleRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0026",
        name="context-window-incompatible",
        description="Detects token budgets that are incompatible with the referenced model's context window",
        severity=DiagnosticSeverity.Error,
        category="token-budget",
        version="1.0.0",
        tags=("budget", "models", "context"),
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
        budgets = [s for s in symbols if isinstance(s, TokenBudget)]
        models = {getattr(m, "name", ""): m for m in semantic_model.get_symbols_by_kind(SymbolKind.MODEL_PROFILE) if isinstance(m, ModelProfile)}

        for budget in budgets:
            if cancellation_token and cancellation_token.cancelled:
                break

            budget_name = getattr(budget, "name", "")
            max_total = getattr(budget, "max_total_tokens", 0)

            # Try to find a matching model
            matching_model = models.get(budget_name)
            if matching_model is None:
                matching_model = models.get(budget_name.lower())
            if matching_model is None:
                for m_name, m_sym in models.items():
                    if budget_name in m_name or m_name in budget_name:
                        matching_model = m_sym
                        break

            if matching_model is not None:
                context_window = getattr(matching_model, "context_window", 0)
                if context_window > 0 and max_total > context_window:
                    sr = getattr(budget, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0026: Token budget '{budget.name}' max_total ({max_total}) exceeds model '{matching_model.name}' context window ({context_window})",
                            source="aeos-lsp",
                        ))

        return diagnostics


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text.split()) // 2)
