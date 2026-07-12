from __future__ import annotations

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import (
    Playbook,
    PlaybookStep,
    QualityGate,
    SymbolKind,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class EvidenceGateRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0020",
        name="gate-without-evidence",
        description="Detects quality gates that are configured without required evidence",
        severity=DiagnosticSeverity.Warning,
        category="evidence",
        version="1.0.0",
        tags=("evidence", "quality-gates"),
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
        gates = [s for s in symbols if isinstance(s, QualityGate)]

        for gate in gates:
            if cancellation_token and cancellation_token.cancelled:
                break

            rules = getattr(gate, "rules", [])
            has_evidence_rule = False

            if isinstance(rules, list):
                for rule in rules:
                    if isinstance(rule, dict):
                        rule_type = rule.get("type", rule.get("kind", ""))
                        if "evidence" in rule_type.lower():
                            has_evidence_rule = True
                            break

            if not has_evidence_rule:
                sr = getattr(gate, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0020: Quality gate '{gate.name}' has no evidence requirement defined",
                        source="aeos-lsp",
                    ))

        return diagnostics


class PassWithoutEvidenceRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0021",
        name="pass-allowed-without-evidence",
        description="Detects configurations where PASS is allowed without evidence",
        severity=DiagnosticSeverity.Warning,
        category="evidence",
        version="1.0.0",
        tags=("evidence", "quality-gates"),
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
        gates = [s for s in symbols if isinstance(s, QualityGate)]

        for gate in gates:
            if cancellation_token and cancellation_token.cancelled:
                break

            rules = getattr(gate, "rules", [])
            if isinstance(rules, list):
                has_evidence_requirement = False
                has_pass_without_evidence = True  # default: assume pass is allowed

                for rule in rules:
                    if isinstance(rule, dict):
                        rule_type = rule.get("type", rule.get("kind", ""))
                        if "evidence" in rule_type.lower():
                            has_evidence_requirement = True
                            action = rule.get("action", rule.get("on_failure", ""))
                            if "fail" in action.lower() or "block" in action.lower():
                                has_pass_without_evidence = False

                if not has_evidence_requirement or has_pass_without_evidence:
                    sr = getattr(gate, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0021: Quality gate '{gate.name}' allows PASS without evidence verification",
                            source="aeos-lsp",
                        ))

        return diagnostics


class ArtifactProvenanceRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0040",
        name="artifact-without-provenance",
        description="Detects artifacts defined without provenance metadata",
        severity=DiagnosticSeverity.Warning,
        category="evidence",
        version="1.0.0",
        tags=("evidence", "artifacts", "provenance"),
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

            kind = type(sym).__name__
            if kind == "Artifact":
                metadata = getattr(sym, "metadata", {})
                if not metadata or not isinstance(metadata, dict):
                    sr = getattr(sym, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Warning,
                            code=self.metadata.code,
                            message=f"AEOS0040: Artifact '{getattr(sym, 'name', '')}' has no provenance metadata",
                            source="aeos-lsp",
                        ))
                else:
                    has_provenance = any(
                        key in ("source", "origin", "provenance", "generated_by", "created_by")
                        for key in metadata
                    )
                    if not has_provenance:
                        sr = getattr(sym, "selection_range", None)
                        if sr is not None:
                            diagnostics.append(Diagnostic(
                                range=sr,
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0040: Artifact '{getattr(sym, 'name', '')}' has no provenance in metadata",
                                source="aeos-lsp",
                            ))

        return diagnostics


class EvidenceHashRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0041",
        name="evidence-hash-missing",
        description="Detects evidence configurations where content hash is missing or invalid",
        severity=DiagnosticSeverity.Error,
        category="evidence",
        version="1.0.0",
        tags=("evidence", "integrity", "hashing"),
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

            content_hash = getattr(sym, "content_hash", "")
            if hasattr(sym, "content_hash") and not content_hash:
                sr = getattr(sym, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0041: Symbol '{getattr(sym, 'name', sym.stable_id)}' is missing content hash",
                        source="aeos-lsp",
                    ))
            elif content_hash and len(content_hash) < 8:
                sr = getattr(sym, "selection_range", None)
                if sr is not None:
                    diagnostics.append(Diagnostic(
                        range=sr,
                        severity=DiagnosticSeverity.Warning,
                        code=self.metadata.code,
                        message=f"AEOS0041: Symbol '{getattr(sym, 'name', sym.stable_id)}' has suspiciously short content hash",
                        source="aeos-lsp",
                    ))

        # Check for hash mismatch patterns in documents with AEOS0042 code
        if "AEOS0042" in self.metadata.code or True:
            for sym in symbols:
                if cancellation_token and cancellation_token.cancelled:
                    break
                if hasattr(sym, "content_hash"):
                    content_hash = getattr(sym, "content_hash", "")
                    stable_id = getattr(sym, "stable_id", "")
                    name = getattr(sym, "name", stable_id)
                    if content_hash:
                        import hashlib
                        if not _is_valid_hash(content_hash):
                            sr = getattr(sym, "selection_range", None)
                            if sr is not None:
                                diagnostics.append(Diagnostic(
                                    range=sr,
                                    severity=DiagnosticSeverity.Error,
                                    code="AEOS0042",
                                    message=f"AEOS0042: Symbol '{name}' has invalid content hash format: '{content_hash}'",
                                    source="aeos-lsp",
                                ))

        return diagnostics


def _is_valid_hash(hash_str: str) -> bool:
    if len(hash_str) != 64 and len(hash_str) != 40 and len(hash_str) != 32:
        if len(hash_str) >= 8 and all(c in "0123456789abcdefABCDEF" for c in hash_str):
            return True
        return False
    return all(c in "0123456789abcdefABCDEF" for c in hash_str)


class EvidenceHashInvalidRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0042",
        name="evidence-hash-invalid",
        description="Detects evidence with invalid or tampered content hashes",
        severity=DiagnosticSeverity.Error,
        category="evidence",
        version="1.0.0",
        tags=("evidence", "integrity", "tampering"),
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

            content_hash = getattr(sym, "content_hash", "")
            if content_hash:
                if not _is_valid_hash(content_hash):
                    sr = getattr(sym, "selection_range", None)
                    if sr is not None:
                        diagnostics.append(Diagnostic(
                            range=sr,
                            severity=DiagnosticSeverity.Error,
                            code=self.metadata.code,
                            message=f"AEOS0042: Symbol '{getattr(sym, 'name', sym.stable_id)}' has invalid content hash",
                            source="aeos-lsp",
                        ))

        return diagnostics
