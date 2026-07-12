from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import PlaybookStep, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class ToolNotRegisteredRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0013",
        name="tool-not-registered",
        description="Detects tool references that are not registered",
        severity=DiagnosticSeverity.Error,
        category="registrations",
        version="1.0.0",
        tags=("tools", "registry"),
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

        all_tools = semantic_model.get_symbols_by_kind(SymbolKind.TOOL)
        tool_names: set[str] = {getattr(t, "name", "") for t in all_tools}
        tool_ids: set[str] = {getattr(t, "stable_id", "") for t in all_tools}

        symbols = semantic_model.get_symbols_by_uri(document_uri)

        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, Skill):
                for tool_ref in sym.tools:
                    if tool_ref not in tool_names and tool_ref not in tool_ids:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0013: Skill '{sym.name}' references tool '{tool_ref}' which is not registered",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, PlaybookStep):
                if sym.tool:
                    if sym.tool not in tool_names and sym.tool not in tool_ids:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0013: Step '{sym.name}' references tool '{sym.tool}' which is not registered",
                            source="aeos-lsp",
                        ))

        return diagnostics
