from __future__ import annotations

from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel


class InvalidSchemaRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0002",
        name="invalid-schema",
        description="Detects invalid schema structures in AEOS documents",
        severity=DiagnosticSeverity.Error,
        category="schema",
        version="1.0.0",
        tags=("validation", "schema"),
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
        if not symbols:
            return diagnostics

        for sym in symbols:
            kind = type(sym).__name__
            raw_data = {}
            if hasattr(sym, "source_uri"):
                pass

            # Check for required fields based on symbol type
            errors = _validate_symbol_schema(sym, document_text)
            for err in errors:
                diagnostics.append(err)

            if cancellation_token and cancellation_token.cancelled:
                return diagnostics

        return diagnostics


def _validate_symbol_schema(sym: Any, text: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    sym_type = type(sym).__name__

    if sym_type == "Agent":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Agent is missing required 'name' field",
                source="aeos-lsp",
            ))
        skills = getattr(sym, "skills", [])
        if not skills and not getattr(sym, "layers", []):
            pass  # Skills are optional if layers are specified

    elif sym_type == "Skill":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Skill is missing required 'name' field",
                source="aeos-lsp",
            ))

    elif sym_type == "Playbook":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Playbook is missing required 'name' field",
                source="aeos-lsp",
            ))
        steps = getattr(sym, "steps", [])
        if not steps:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Warning,
                code="AEOS0002",
                message="AEOS0002: Playbook has no steps defined",
                source="aeos-lsp",
            ))

    elif sym_type == "PlaybookStep":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Step is missing required 'name' field",
                source="aeos-lsp",
            ))
        step_type = getattr(sym, "step_type", "")
        if not step_type:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Step is missing required 'type' field",
                source="aeos-lsp",
            ))

    elif sym_type == "Permission":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Permission is missing required 'name' field",
                source="aeos-lsp",
            ))

    elif sym_type == "Policy":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: Policy is missing required 'name' field",
                source="aeos-lsp",
            ))

    elif sym_type == "TokenBudget":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: TokenBudget is missing required 'name' field",
                source="aeos-lsp",
            ))

    elif sym_type == "ModelProfile":
        name = getattr(sym, "name", "")
        if not name:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                severity=DiagnosticSeverity.Error,
                code="AEOS0002",
                message="AEOS0002: ModelProfile is missing required 'name' field",
                source="aeos-lsp",
            ))

    return diagnostics
