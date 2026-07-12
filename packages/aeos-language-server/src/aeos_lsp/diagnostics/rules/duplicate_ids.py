from __future__ import annotations

from collections import Counter

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel


class DuplicateIdRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0003",
        name="duplicate-id",
        description="Detects duplicate stable IDs across the workspace",
        severity=DiagnosticSeverity.Error,
        category="identity",
        version="1.0.0",
        tags=("identity", "uniqueness"),
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

        # Check for duplicate IDs within the same document
        symbols = semantic_model.get_symbols_by_uri(document_uri)
        id_counts: Counter[str] = Counter()
        id_symbols: dict[str, list] = {}

        for sym in symbols:
            sid = getattr(sym, "stable_id", "")
            if sid:
                id_counts[sid] += 1
                if sid not in id_symbols:
                    id_symbols[sid] = []
                id_symbols[sid].append(sym)

        for sid, count in id_counts.items():
            if count > 1:
                for sym in id_symbols.get(sid, []):
                    sr = getattr(sym, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0003: Duplicate stable ID '{sid}' found {count} times in this document",
                            source="aeos-lsp",
                        ))

        if cancellation_token and cancellation_token.cancelled:
            return diagnostics

        return diagnostics

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        id_counts: Counter[str] = Counter()
        id_symbols: dict[str, list] = {}

        all_symbols = semantic_model.symbol_table.all_symbols()
        for sym in all_symbols:
            sid = getattr(sym, "stable_id", "")
            if sid:
                id_counts[sid] += 1
                if sid not in id_symbols:
                    id_symbols[sid] = []
                id_symbols[sid].append(sym)

        for sid, count in id_counts.items():
            if count > 1:
                if cancellation_token and cancellation_token.cancelled:
                    break
                seen_uris: set[str] = set()
                for sym in id_symbols.get(sid, []):
                    uri = getattr(sym, "source_uri", "")
                    if uri in seen_uris:
                        continue
                    seen_uris.add(uri)
                    sr = getattr(sym, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0003: Duplicate stable ID '{sid}' found {count} times across workspace",
                            source="aeos-lsp",
                        ))

        return diagnostics
