from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import ModelProfile, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class ModelCompatibilityRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0030",
        name="model-compatibility",
        description="Detects model-related configuration issues",
        severity=DiagnosticSeverity.Warning,
        category="models",
        version="1.0.0",
        tags=("models", "compatibility"),
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
        models = [s for s in symbols if isinstance(s, ModelProfile)]
        all_models = semantic_model.get_symbols_by_kind(SymbolKind.MODEL_PROFILE)
        model_names: set[str] = {getattr(m, "name", "") for m in all_models}

        for model in models:
            if cancellation_token and cancellation_token.cancelled:
                break

            provider = getattr(model, "provider", "")
            context_window = getattr(model, "context_window", 0)
            max_tokens = getattr(model, "max_tokens", 0)
            cost = getattr(model, "cost", 0.0)

            sr = getattr(model, "selection_range", None)

            if not provider:
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AE0030: Model profile '{model.name}' has no provider specified",
                        source="aeos-lsp",
                    ))

            if context_window <= 0:
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AE0030: Model profile '{model.name}' has invalid context_window ({context_window})",
                        source="aeos-lsp",
                    ))

            if max_tokens <= 0:
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AE0030: Model profile '{model.name}' has invalid max_tokens ({max_tokens})",
                        source="aeos-lsp",
                    ))

            if max_tokens > context_window and context_window > 0:
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Error,
                        code=self.metadata.code,
                        message=f"AE0030: Model profile '{model.name}' max_tokens ({max_tokens}) exceeds context_window ({context_window})",
                        source="aeos-lsp",
                    ))

            if cost < 0:
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AE0030: Model profile '{model.name}' has negative cost ({cost})",
                        source="aeos-lsp",
                    ))

        return diagnostics
