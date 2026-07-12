from __future__ import annotations

from collections import Counter

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Registry, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class DuplicateRegistryRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0043",
        name="duplicate-registry",
        description="Detects duplicate registrations in the same registry",
        severity=DiagnosticSeverity.Warning,
        category="registries",
        version="1.0.0",
        tags=("registries", "duplicates"),
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
        registries = [s for s in symbols if isinstance(s, Registry)]

        for reg in registries:
            if cancellation_token and cancellation_token.cancelled:
                break

            entries = getattr(reg, "entries", {})
            if isinstance(entries, dict):
                entry_names: Counter[str] = Counter(entries.keys())
                for entry_name, count in entry_names.items():
                    if count > 1:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0043: Registry '{reg.name}' has duplicate entry '{entry_name}' ({count} occurrences)",
                            source="aeos-lsp",
                        ))

                # Check for duplicate refs within the same registry
                seen_refs: set[str] = set()
                for entry_key, entry_val in entries.items():
                    if isinstance(entry_val, dict):
                        ref = entry_val.get("ref") or entry_val.get("$ref") or entry_val.get("implementation", "")
                        if ref:
                            if ref in seen_refs:
                                diagnostics.append(Diagnostic(
                                    range=Range(
                                        start=Position(line=0, character=0),
                                        end=Position(line=0, character=1),
                                    ),
                                    severity=DiagnosticSeverity.Warning,
                                    code=self.metadata.code,
                                    message=f"AEOS0043: Registry '{reg.name}' has duplicate reference '{ref}' in entries",
                                    source="aeos-lsp",
                                ))
                            seen_refs.add(ref)

        return diagnostics

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        all_registries = semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)

        registry_type_groups: dict[str, list[Registry]] = {}
        for reg in all_registries:
            if isinstance(reg, Registry):
                reg_type = getattr(reg, "registry_type", "unknown")
                if reg_type not in registry_type_groups:
                    registry_type_groups[reg_type] = []
                registry_type_groups[reg_type].append(reg)

        for reg_type, regs in registry_type_groups.items():
            if cancellation_token and cancellation_token.cancelled:
                break

            if len(regs) <= 1:
                continue

            all_entry_names: set[str] = set()
            for reg in regs:
                entries = getattr(reg, "entries", {})
                if isinstance(entries, dict):
                    for entry_name in entries:
                        if entry_name in all_entry_names:
                            for r in regs:
                                sr = getattr(r, "selection_range", None)
                                if sr is not None:
                                    diagnostics.append(Diagnostic(
                                        range=sr,
                                        severity=DiagnosticSeverity.Warning,
                                        code=self.metadata.code,
                                        message=f"AEOS0043: Duplicate entry '{entry_name}' across registry '{r.name}' and other registry of type '{reg_type}'",
                                        source="aeos-lsp",
                                    ))
                        all_entry_names.add(entry_name)

        return diagnostics


class MultipleSourcesOfTruthRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0044",
        name="multiple-sources-of-truth",
        description="Detects conflicting definitions across multiple registries or sources",
        severity=DiagnosticSeverity.Error,
        category="registries",
        version="1.0.0",
        check_workspace=True,
        tags=("registries", "conflicts"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        all_registries = semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)

        # Group registries by type (agents, skills, playbooks, etc.)
        registry_groups: dict[str, list[Registry]] = {}
        for reg in all_registries:
            if isinstance(reg, Registry):
                reg_type = getattr(reg, "registry_type", "unknown").lower()
                if reg_type not in registry_groups:
                    registry_groups[reg_type] = []
                registry_groups[reg_type].append(reg)

        # Check for conflicting definitions of the same entity across registries
        for reg_type, regs in registry_groups.items():
            if cancellation_token and cancellation_token.cancelled:
                break

            if len(regs) < 2:
                continue

            all_definitions: dict[str, list[tuple[str, str]]] = {}  # name -> [(ref, source_registry_name)]

            for reg in regs:
                entries = getattr(reg, "entries", {})
                if isinstance(entries, dict):
                    for entry_name, entry_val in entries.items():
                        ref = entry_name
                        if isinstance(entry_val, dict):
                            ref = entry_val.get("ref") or entry_val.get("$ref") or entry_val.get("implementation", entry_name)
                        if entry_name not in all_definitions:
                            all_definitions[entry_name] = []
                        all_definitions[entry_name].append((ref, getattr(reg, "name", "unknown")))

            for entry_name, defs in all_definitions.items():
                if len(defs) > 1:
                    unique_refs = set(d[0] for d in defs)
                    if len(unique_refs) > 1:
                        for reg in regs:
                            sr = getattr(reg, "selection_range", None)
                            if sr is not None:
                                srcs = ", ".join(f"'{s}'" for _, s in defs)
                                diagnostics.append(Diagnostic(
                                    range=sr,
                                    severity=DiagnosticSeverity.Error,
                                    code=self.metadata.code,
                                    message=f"AEOS0044: Multiple sources of truth for '{entry_name}' in registries: {srcs}",
                                    source="aeos-lsp",
                                ))

        return diagnostics

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        return []
