from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import PlaybookStep
from aeos_lsp.semantic.semantic_model import SemanticModel


class UnlimitedRetryRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0027",
        name="unlimited-retry",
        description="Detects operations with unlimited or excessive retry configurations",
        severity=DiagnosticSeverity.Warning,
        category="execution",
        version="1.0.0",
        tags=("execution", "retry", "safety"),
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
                retry = getattr(sym, "retry", None)

                if retry is not None:
                    if retry < 0:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0027: Step '{sym.name}' has negative retry count ({retry})",
                            source="aeos-lsp",
                        ))
                    elif retry == 0:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0027: Step '{sym.name}' has retry=0 which disables retries",
                            source="aeos-lsp",
                        ))
                    elif retry > 10:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0027: Step '{sym.name}' has excessive retry count ({retry}) which may cause runaway execution",
                            source="aeos-lsp",
                        ))

        return diagnostics
