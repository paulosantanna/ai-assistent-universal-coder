from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, DiagnosticTag, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import (
    Agent,
    DeprecationStatus,
    Playbook,
    PlaybookStep,
    Skill,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class DeprecatedFieldRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0045",
        name="deprecated-field",
        description="Detects usage of deprecated fields in AEOS configurations",
        severity=DiagnosticSeverity.Warning,
        category="deprecations",
        version="1.0.0",
        tags=("deprecations", "migrations"),
    )

    DEPRECATED_FIELD_PATTERNS: dict[str, list[str]] = {
        "agent": [
            "model",
            "model_name",
            "temperature",
            "max_tokens_old",
        ],
        "skill": [
            "model",
            "temperature",
        ],
        "step": [
            "timeout_seconds",
            "retry_count",
            "step_type_old",
        ],
    }

    OLD_TO_NEW: dict[str, str] = {
        "model": "model_profile",
        "model_name": "model_profile",
        "temperature": "model_profile.temperature",
        "max_tokens_old": "max_tokens",
        "timeout_seconds": "timeout",
        "retry_count": "retry",
        "step_type_old": "step_type",
    }

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        # Check for deprecated fields in raw document text
        lines = document_text.splitlines()
        deprecated_fields = set()
        for pattern_list in self.DEPRECATED_FIELD_PATTERNS.values():
            deprecated_fields.update(pattern_list)

        for line_idx, line_text in enumerate(lines):
            if cancellation_token and cancellation_token.cancelled:
                break

            stripped = line_text.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            for dep_field in deprecated_fields:
                # Match key: deprecated_field or "deprecated_field":
                import re
                m = re.search(
                    rf'^\s*{re.escape(dep_field)}\s*:',
                    stripped,
                )
                if m:
                    new_name = self.OLD_TO_NEW.get(dep_field, dep_field + "_new")
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line_idx, character=m.start()),
                            end=Position(line=line_idx, character=m.end()),
                        ),
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0045: Field '{dep_field}' is deprecated; use '{new_name}' instead",
                        source="aeos-lsp",
                        tags=[DiagnosticTag.Deprecated],
                    ))

        # Check semantic symbols for deprecated status
        symbols = semantic_model.get_symbols_by_uri(document_uri)
        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            deprecation = getattr(sym, "deprecation", None)
            if deprecation is not None and deprecation == DeprecationStatus.DEPRECATED:
                sr = getattr(sym, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0045: Symbol '{getattr(sym, 'name', sym.stable_id)}' is marked as deprecated",
                        source="aeos-lsp",
                        tags=[DiagnosticTag.Deprecated],
                    ))

            # Check references to deprecated symbols
            if isinstance(sym, (Agent, Skill, Playbook, PlaybookStep)):
                references = getattr(sym, "references", [])
                if references:
                    for ref in references:
                        ref_sym = semantic_model.get_symbol_by_id(ref)
                        if ref_sym is not None:
                            ref_dep = getattr(ref_sym, "deprecation", None)
                            if ref_dep is not None and ref_dep == DeprecationStatus.DEPRECATED:
                                sr = getattr(sym, "selection_range", None)
                                if sr is not None:
                                    diagnostics.append(Diagnostic(
                                        range=sr,
                                        severity=DiagnosticSeverity.Info,
                                        code=self.metadata.code,
                                        message=f"AEOS0045: '{getattr(sym, 'name', sym.stable_id)}' references deprecated symbol '{getattr(ref_sym, 'name', ref)}'",
                                        source="aeos-lsp",
                                        tags=[DiagnosticTag.Deprecated],
                                    ))

        return diagnostics
