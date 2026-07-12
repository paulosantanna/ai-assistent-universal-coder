from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import PlaybookStep, Tool
from aeos_lsp.semantic.semantic_model import SemanticModel


class MissingTimeoutRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0028",
        name="missing-timeout",
        description="Detects operations that are missing a timeout configuration",
        severity=DiagnosticSeverity.Warning,
        category="execution",
        version="1.0.0",
        tags=("execution", "timeout", "safety"),
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
                timeout = getattr(sym, "timeout", None)
                step_type = getattr(sym, "step_type", "")

                # Required timeout for certain step types
                timeout_required_types = {"exec", "shell", "command", "http", "api",
                                          "deploy", "build", "test", "pipeline",
                                          "container", "docker", "k8s", "kubernetes"}

                if timeout is None or timeout <= 0:
                    if step_type.lower() in timeout_required_types:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0028: Step '{sym.name}' of type '{step_type}' has no timeout configured",
                            source="aeos-lsp",
                        ))

                # Check for very short timeouts that may cause premature failure
                if timeout is not None and 0 < timeout < 1:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=1),
                        ),
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0028: Step '{sym.name}' has a very short timeout ({timeout}s) that may cause premature failure",
                        source="aeos-lsp",
                    ))

            elif isinstance(sym, Tool):
                timeout = getattr(sym, "timeout", None)
                command = getattr(sym, "command", "")
                mutating = getattr(sym, "mutating", False)

                if timeout is None and mutating:
                    sr = getattr(sym, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0028: Mutating tool '{sym.name}' has no timeout configured",
                            source="aeos-lsp",
                        ))

        return diagnostics
