from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Agent, Playbook, PlaybookStep, Skill, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class ArchitectureViolationRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0034",
        name="architecture-violation",
        description="Detects violations of AEOS architecture conventions",
        severity=DiagnosticSeverity.Warning,
        category="architecture",
        version="1.0.0",
        tags=("architecture", "conventions"),
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
                sr = getattr(sym, "selection_range", None)

                # Agent without any skills or layers
                skills = getattr(sym, "skills", [])
                layers = getattr(sym, "layers", [])
                if not skills and not layers:
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0034: Agent '{sym.name}' has no skills or layers defined",
                            source="aeos-lsp",
                        ))

                # Agent with too many direct skills
                if len(skills) > 10:
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0034: Agent '{sym.name}' has {len(skills)} direct skills; consider using layers for organization",
                            source="aeos-lsp",
                        ))

                # Private agents with references
                visibility = getattr(sym, "visibility", None)
                if visibility is not None:
                    vis_str = str(visibility.value if hasattr(visibility, "value") else visibility)
                    if vis_str == "private":
                        referrers = semantic_model.reference_table.get_incoming(document_uri)
                        if referrers:
                            if sr is not None:
                                diagnostics.append(Diagnostic(
                                    range=sr,
                                    severity=DiagnosticSeverity.Hint,
                                    code=self.metadata.code,
                                    message=f"AEOS0034: Private agent '{sym.name}' is referenced from other documents",
                                    source="aeos-lsp",
                                ))

            elif isinstance(sym, Skill):
                sr = getattr(sym, "selection_range", None)
                tools = getattr(sym, "tools", [])

                # Skill without tools
                if not tools:
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0034: Skill '{sym.name}' has no tools defined",
                            source="aeos-lsp",
                        ))

                # Skill with too many tools
                if len(tools) > 20:
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Hint,
                            code=self.metadata.code,
                            message=f"AEOS0034: Skill '{sym.name}' has {len(tools)} tools; consider splitting into smaller skills",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, Playbook):
                sr = getattr(sym, "selection_range", None)
                steps = getattr(sym, "steps", [])

                # Playbook with too many steps
                if len(steps) > 30:
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Hint,
                            code=self.metadata.code,
                            message=f"AEOS0034: Playbook '{sym.name}' has {len(steps)} steps; consider splitting into multiple playbooks",
                            source="aeos-lsp",
                        ))

            elif isinstance(sym, PlaybookStep):
                step_type = getattr(sym, "step_type", "")
                conditions = getattr(sym, "conditions", [])

                # Step with too many conditions
                if len(conditions) > 5:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=1),
                        ),
                        severity=DiagnosticSeverity.Hint,
                        code=self.metadata.code,
                        message=f"AEOS0034: Step '{sym.name}' has {len(conditions)} conditions; consider simplifying the logic",
                        source="aeos-lsp",
                    ))

        return diagnostics
