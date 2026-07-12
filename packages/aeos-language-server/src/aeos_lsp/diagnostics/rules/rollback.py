from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import PlaybookStep, Tool
from aeos_lsp.semantic.semantic_model import SemanticModel


class MutatingStepWithoutRollbackRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0019",
        name="mutating-step-without-rollback",
        description="Detects mutating operations that lack a rollback definition",
        severity=DiagnosticSeverity.Warning,
        category="rollback",
        version="1.0.0",
        tags=("rollback", "safety", "mutating"),
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
        tools = {getattr(t, "name", ""): t for t in semantic_model.get_symbols_by_uri(document_uri) if isinstance(t, Tool)}

        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, PlaybookStep):
                step_type = getattr(sym, "step_type", "")
                has_rollback = getattr(sym, "rollback", None) is not None
                tool_name = getattr(sym, "tool", None)

                # Check if step references a mutating tool
                is_mutating = False
                if tool_name:
                    tool = tools.get(tool_name)
                    if tool is not None:
                        is_mutating = getattr(tool, "mutating", False)
                    else:
                        # Try resolving tool
                        result = semantic_model.resolver.resolve_by_name(tool_name)
                        if result.resolved and result.symbol:
                            tool = result.symbol
                            if isinstance(tool, Tool):
                                is_mutating = getattr(tool, "mutating", False)

                if is_mutating and not has_rollback:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=1),
                        ),
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0019: Step '{sym.name}' uses mutating tool '{tool_name}' but has no rollback defined",
                        source="aeos-lsp",
                    ))

                # Check if step type is inherently mutating
                mutating_types = {"write", "create", "update", "delete", "modify",
                                  "patch", "put", "post", "deploy", "publish",
                                  "upload", "send", "transfer"}
                if step_type.lower() in mutating_types and not has_rollback:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=1),
                        ),
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0019: Step '{sym.name}' has mutating type '{step_type}' but has no rollback defined",
                        source="aeos-lsp",
                    ))

        return diagnostics
