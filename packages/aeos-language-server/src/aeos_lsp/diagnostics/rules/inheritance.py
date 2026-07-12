from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Agent, Skill
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.symbols import SemanticSymbol


class InvalidInheritanceRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0010",
        name="invalid-inheritance",
        description="Detects invalid inheritance relationships (root without parent, child without valid parent, etc.)",
        severity=DiagnosticSeverity.Error,
        category="inheritance",
        version="1.0.0",
        tags=("inheritance", "agents"),
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

            if isinstance(sym, Agent):
                parent_id = sym.parent_id

                # Agent with parent that does not exist
                if parent_id:
                    parent_sym = semantic_model.get_symbol_by_id(parent_id)
                    if parent_sym is None:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0010: Agent '{sym.name}' extends non-existent parent '{parent_id}'",
                            source="aeos-lsp",
                        ))
                    elif not isinstance(parent_sym, Agent):
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0010: Agent '{sym.name}' extends '{parent_id}' which is not an Agent",
                            source="aeos-lsp",
                        ))
                    else:
                        # Check for self-inheritance
                        if parent_id == sym.stable_id:
                            sr = sym.selection_range
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Error,
                                code=self.metadata.code,
                                message=f"AEOS0010: Agent '{sym.name}' cannot extend itself",
                                source="aeos-lsp",
                            ))

                        # Check for deep inheritance chains
                        chain = semantic_model.resolver.resolve_agent_inheritance_chain(sym)
                        if len(chain) > 10:
                            sr = sym.selection_range
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0010: Agent '{sym.name}' has a deep inheritance chain ({len(chain)} levels)",
                                source="aeos-lsp",
                            ))

                # Agent with both parent and layers may indicate ambiguous structure
                if parent_id and sym.layers:
                    sr = sym.selection_range
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0010: Agent '{sym.name}' defines both parent and layers which may conflict",
                        source="aeos-lsp",
                    ))

        return diagnostics
