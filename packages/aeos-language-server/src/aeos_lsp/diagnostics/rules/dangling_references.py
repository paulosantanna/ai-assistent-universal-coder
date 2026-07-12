from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import (
    Agent,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class DanglingReferenceRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0004",
        name="dangling-reference",
        description="Detects references to non-existent symbols",
        severity=DiagnosticSeverity.Error,
        category="references",
        version="1.0.0",
        tags=("references", "resolution"),
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
                # Check parent reference
                parent_id = sym.parent_id
                if parent_id:
                    result = semantic_model.resolver.resolve_by_id(parent_id)
                    if not result.resolved:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0004: Agent '{sym.name}' references non-existent parent '{parent_id}'",
                            source="aeos-lsp",
                        ))

                # Check skill references
                for skill_ref in sym.skills:
                    result = semantic_model.resolver.resolve_by_name(skill_ref, SymbolKind.SKILL)
                    if not result.resolved:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0004: Agent '{sym.name}' references non-existent skill '{skill_ref}'",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, PlaybookStep):
                if sym.tool:
                    result = semantic_model.resolver.resolve_by_name(sym.tool, SymbolKind.TOOL)
                    if not result.resolved:
                        result = semantic_model.resolver.resolve_by_id(sym.tool)
                    if not result.resolved:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0004: Step '{sym.name}' references non-existent tool '{sym.tool}'",
                            source="aeos-lsp",
                        ))

                if sym.skill:
                    result = semantic_model.resolver.resolve_by_name(sym.skill, SymbolKind.SKILL)
                    if not result.resolved:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0004: Step '{sym.name}' references non-existent skill '{sym.skill}'",
                            source="aeos-lsp",
                        ))

                if sym.playbook:
                    result = semantic_model.resolver.resolve_by_name(sym.playbook, SymbolKind.PLAYBOOK)
                    if not result.resolved:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0004: Step '{sym.name}' references non-existent playbook '{sym.playbook}'",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, Skill):
                for tool_ref in sym.tools:
                    result = semantic_model.resolver.resolve_by_name(tool_ref, SymbolKind.TOOL)
                    if not result.resolved:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0004: Skill '{sym.name}' references non-existent tool '{tool_ref}'",
                            source="aeos-lsp",
                        ))

        return diagnostics


class AmbiguousReferenceRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0005",
        name="ambiguous-reference",
        description="Detects references that resolve to multiple candidates",
        severity=DiagnosticSeverity.Warning,
        category="references",
        version="1.0.0",
        tags=("references", "resolution", "ambiguity"),
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
                for skill_ref in sym.skills:
                    result = semantic_model.resolver.resolve_by_name(skill_ref, SymbolKind.SKILL)
                    if result.resolved and result.candidates and not result.symbol:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0005: Agent '{sym.name}' has ambiguous reference to skill '{skill_ref}' ({len(result.candidates)} candidates)",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, PlaybookStep):
                if sym.skill:
                    result = semantic_model.resolver.resolve_by_name(sym.skill, SymbolKind.SKILL)
                    if result.resolved and result.candidates and not result.symbol:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0005: Step '{sym.name}' has ambiguous reference to skill '{sym.skill}' ({len(result.candidates)} candidates)",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, Skill):
                for tool_ref in sym.tools:
                    result = semantic_model.resolver.resolve_by_name(tool_ref, SymbolKind.TOOL)
                    if result.resolved and result.candidates and not result.symbol:
                        sr = sym.selection_range
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0005: Skill '{sym.name}' has ambiguous reference to tool '{tool_ref}' ({len(result.candidates)} candidates)",
                            source="aeos-lsp",
                        ))

        return diagnostics
