from __future__ import annotations

import re
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel


class InvalidSyntaxRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0001",
        name="invalid-syntax",
        description="Detects invalid YAML/JSON syntax in AEOS documents",
        severity=DiagnosticSeverity.Error,
        category="syntax",
        version="1.0.0",
        tags=("parsing", "yaml", "json"),
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

        doc = _get_parse_result(document_uri, semantic_model)
        if doc is None:
            return diagnostics

        parse_errors = _get_parse_errors(document_uri, semantic_model)
        for err in parse_errors:
            d = Diagnostic(
                range=err.range,
                severity=self.metadata.severity,
                code=self.metadata.code,
                message=f"AEOS0001: {err.message}",
                source="aeos-lsp",
            )
            diagnostics.append(d)

        # Check for unbalanced quotes
        lines = document_text.splitlines()
        for line_idx, line_text in enumerate(lines):
            stripped = line_text.strip()
            if stripped.startswith("#"):
                continue
            if stripped.count('"') % 2 != 0:
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=line_idx, character=0),
                        end=Position(line=line_idx, character=len(line_text)),
                    ),
                    severity=DiagnosticSeverity.Error,
                    code=self.metadata.code,
                    message="AEOS0001: Unbalanced double quotes",
                    source="aeos-lsp",
                ))
            if stripped.count("'") % 2 != 0:
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=line_idx, character=0),
                        end=Position(line=line_idx, character=len(line_text)),
                    ),
                    severity=DiagnosticSeverity.Error,
                    code=self.metadata.code,
                    message="AEOS0001: Unbalanced single quotes",
                    source="aeos-lsp",
                ))

        # Check for tab characters
        for line_idx, line_text in enumerate(lines):
            if "\t" in line_text and not line_text.strip().startswith("#"):
                tab_pos = line_text.index("\t")
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=line_idx, character=tab_pos),
                        end=Position(line=line_idx, character=tab_pos + 1),
                    ),
                    severity=DiagnosticSeverity.Warning,
                    code=self.metadata.code,
                    message="AEOS0001: Tab characters are not allowed in YAML; use spaces for indentation",
                    source="aeos-lsp",
                ))

        if cancellation_token and cancellation_token.cancelled:
            return diagnostics

        return _deduplicate_diagnostics(diagnostics)


def _get_parse_result(uri: str, semantic_model: SemanticModel) -> object | None:
    return None


def _get_parse_errors(uri: str, semantic_model: SemanticModel) -> list[Any]:
    return []


def _deduplicate_diagnostics(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple] = set()
    result: list[Diagnostic] = []
    for d in diagnostics:
        key = (d.range.start.line, d.range.start.character, d.code, d.message)
        if key not in seen:
            seen.add(key)
            result.append(d)
    return result
