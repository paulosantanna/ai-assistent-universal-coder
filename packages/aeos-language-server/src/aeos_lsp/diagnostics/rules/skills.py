from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class SkillNotRegisteredRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0012",
        name="skill-not-registered",
        description="Detects skill references that are not registered in the skill registry",
        severity=DiagnosticSeverity.Error,
        category="registrations",
        version="1.0.0",
        check_workspace=True,
        tags=("skills", "registry"),
    )

    def check_workspace(
        self,
        workspace: object,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        skills = semantic_model.get_symbols_by_kind(SymbolKind.SKILL)
        registries = semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)

        registered_names: set[str] = set()
        registered_ids: set[str] = set()
        for reg in registries:
            if hasattr(reg, "registry_type") and "skill" in reg.registry_type.lower():
                entries = getattr(reg, "entries", {})
                if isinstance(entries, dict):
                    registered_names.update(entries.keys())
                    for val in entries.values():
                        if isinstance(val, dict):
                            ref = val.get("ref") or val.get("$ref") or val.get("implementation", "")
                            if ref:
                                registered_ids.add(ref)

        for skill in skills:
            if cancellation_token and cancellation_token.cancelled:
                break

            skill_name = getattr(skill, "name", "")
            skill_id = getattr(skill, "stable_id", "")

            if skill_name not in registered_names and skill_id not in registered_ids:
                sr = getattr(skill, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0012: Skill '{skill_name}' is not registered in any skill registry",
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
