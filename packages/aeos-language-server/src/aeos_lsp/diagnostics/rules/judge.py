from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import JudgeRule, QualityGate, SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel


class InconsistentJudgeRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0022",
        name="inconsistent-judge",
        description="Detects inconsistent judge configurations (e.g., conflicting conditions or actions)",
        severity=DiagnosticSeverity.Warning,
        category="judge",
        version="1.0.0",
        tags=("judge", "quality"),
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
        judge_rules = [s for s in symbols if isinstance(s, JudgeRule)]

        for rule in judge_rules:
            if cancellation_token and cancellation_token.cancelled:
                break

            condition = getattr(rule, "condition", "")
            action = getattr(rule, "action", "")

            if condition and action:
                # Check for opposing conditions
                if condition.lower() in ("always", "all", "every") and action.lower() in ("skip", "ignore"):
                    sr = getattr(rule, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0022: Judge rule '{rule.name}' has inconsistent condition '{condition}' and action '{action}'",
                            source="aeos-lsp",
                        ))

                # Check for contradictory conditions in multiple rules
                for other in judge_rules:
                    if other is rule:
                        continue
                    if _conditions_contradict(condition, getattr(other, "condition", "")):
                        sr = getattr(rule, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0022: Judge rule '{rule.name}' has condition '{condition}' which contradicts rule '{other.name}'",
                                source="aeos-lsp",
                            ))

        return diagnostics


class ImpossibleScoreRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0023",
        name="impossible-score",
        description="Detects quality gates or judge rules with impossible score thresholds",
        severity=DiagnosticSeverity.Error,
        category="judge",
        version="1.0.0",
        tags=("judge", "scoring"),
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

            if isinstance(sym, QualityGate):
                min_score = getattr(sym, "min_score", None)
                if min_score is not None:
                    if min_score < 0.0:
                        sr = getattr(sym, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Error,
                                code=self.metadata.code,
                                message=f"AEOS0023: Quality gate '{sym.name}' has impossible minimum score {min_score} (below 0.0)",
                                source="aeos-lsp",
                            ))
                    elif min_score > 10.0:
                        sr = getattr(sym, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Error,
                                code=self.metadata.code,
                                message=f"AEOS0023: Quality gate '{sym.name}' has impossible minimum score {min_score} (above 10.0)",
                                source="aeos-lsp",
                            ))

            elif isinstance(sym, JudgeRule):
                min_score = getattr(sym, "min_score", None)
                if min_score is not None:
                    if min_score < 0.0:
                        sr = getattr(sym, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Error,
                                code=self.metadata.code,
                                message=f"AEOS0023: Judge rule '{sym.name}' has impossible minimum score {min_score} (below 0.0)",
                                source="aeos-lsp",
                            ))
                    elif min_score > 10.0:
                        sr = getattr(sym, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Error,
                                code=self.metadata.code,
                                message=f"AEOS0023: Judge rule '{sym.name}' has impossible minimum score {min_score} (above 10.0)",
                                source="aeos-lsp",
                            ))

        return diagnostics


def _conditions_contradict(cond_a: str, cond_b: str) -> bool:
    a = cond_a.lower().strip()
    b = cond_b.lower().strip()
    contradict_pairs = [
        ("always_pass", "always_fail"),
        ("pass", "fail"),
        ("allow", "deny"),
        ("approve", "reject"),
        ("include", "exclude"),
    ]
    for pair in contradict_pairs:
        if (a == pair[0] and b == pair[1]) or (a == pair[1] and b == pair[0]):
            return True
    return False
