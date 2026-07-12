from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import (
    Agent,
    Permission,
    Playbook,
    PlaybookStep,
    Skill,
    SymbolKind,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class MissingPermissionRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0015",
        name="missing-permission",
        description="Detects operations that reference permissions not defined in the workspace",
        severity=DiagnosticSeverity.Error,
        category="permissions",
        version="1.0.0",
        tags=("permissions", "security"),
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

        permissions = semantic_model.get_symbols_by_kind(SymbolKind.PERMISSION)
        permission_names: set[str] = {getattr(p, "name", "") for p in permissions}

        symbols = semantic_model.get_symbols_by_uri(document_uri)

        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, Agent):
                for layer in sym.layers:
                    for skill_ref in layer.skills:
                        skill_result = semantic_model.resolver.resolve_by_name(skill_ref, SymbolKind.SKILL)
                        if skill_result.resolved and skill_result.symbol:
                            skill = skill_result.symbol
                            if hasattr(skill, "requires_permission") and skill.requires_permission:
                                perm_name = skill.requires_permission
                                if perm_name not in permission_names:
                                    diagnostics.append(Diagnostic(
                                        range=Range(
                                            start=Position(line=0, character=0),
                                            end=Position(line=0, character=1),
                                        ),
                                        severity=DiagnosticSeverity.Warning,
                                        code=self.metadata.code,
                                        message=f"AEOS0015: Agent '{sym.name}' references permission '{perm_name}' which is not defined",
                                        source="aeos-lsp",
                                    ))

            elif isinstance(sym, PlaybookStep):
                if sym.approval:
                    approval_perms = [p for p in permissions if "approval" in p.name.lower()]
                    if not approval_perms:
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=0, character=0),
                                end=Position(line=0, character=1),
                            ),
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0015: Step '{sym.name}' requires approval but no approval permission is defined",
                            source="aeos-lsp",
                        ))

        return diagnostics


class IncompatiblePermissionRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0016",
        name="incompatible-permission",
        description="Detects permission configurations that are incompatible or conflict",
        severity=DiagnosticSeverity.Warning,
        category="permissions",
        version="1.0.0",
        tags=("permissions", "compatibility"),
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

        permissions = semantic_model.get_symbols_by_uri(document_uri)
        permission_list = [p for p in permissions if isinstance(p, Permission)]

        for i, perm_a in enumerate(permission_list):
            if cancellation_token and cancellation_token.cancelled:
                break

            for j, perm_b in enumerate(permission_list):
                if j <= i:
                    continue

                a_scopes = set(getattr(perm_a, "scopes", []))
                b_scopes = set(getattr(perm_b, "scopes", []))
                a_caps = set(getattr(perm_a, "capabilities", []))
                b_caps = set(getattr(perm_b, "capabilities", []))

                # Check for scope overlap with conflicting capabilities
                if a_scopes & b_scopes:
                    conflicting_caps = a_caps & b_caps
                    if conflicting_caps:
                        sr_a = getattr(perm_a, "selection_range", None)
                        if sr_a is not None:
                            diagnostics.append(Diagnostic(
                                range=sr_a,
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0016: Permission '{perm_a.name}' may conflict with '{perm_b.name}' on scopes {a_scopes & b_scopes} and capabilities {conflicting_caps}",
                                source="aeos-lsp",
                            ))

        return diagnostics
