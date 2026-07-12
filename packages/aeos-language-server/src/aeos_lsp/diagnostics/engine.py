from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, DiagnosticTag

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.publisher import DiagnosticPublisher
from aeos_lsp.diagnostics.registry import DiagnosticRule, DiagnosticRuleRegistry
from aeos_lsp.diagnostics.severity import DiagnosticSeverityMapper
from aeos_lsp.diagnostics.suppression import SuppressionManager
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.workspace.manager import WorkspaceManager

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticsResult:
    diagnostics: dict[str, list[Diagnostic]] = field(default_factory=dict)
    total_count: int = 0
    errors_count: int = 0
    warnings_count: int = 0
    informations_count: int = 0
    hints_count: int = 0
    result_ids: dict[str, str] = field(default_factory=dict)
    cancelled: bool = False
    elapsed_ms: float = 0.0


class DiagnosticsEngine:
    def __init__(
        self,
        registry: DiagnosticRuleRegistry | None = None,
        publisher: DiagnosticPublisher | None = None,
        suppression_manager: SuppressionManager | None = None,
        severity_mapper: DiagnosticSeverityMapper | None = None,
    ) -> None:
        self._lock = threading.RLock()
        self._registry = registry or DiagnosticRuleRegistry()
        self._publisher = publisher or DiagnosticPublisher()
        self._suppression = suppression_manager or SuppressionManager()
        self._severity_mapper = severity_mapper or DiagnosticSeverityMapper()
        self._result_ids: dict[str, str] = {}

    @property
    def registry(self) -> DiagnosticRuleRegistry:
        return self._registry

    @property
    def publisher(self) -> DiagnosticPublisher:
        return self._publisher

    @property
    def suppression(self) -> SuppressionManager:
        return self._suppression

    @property
    def severity_mapper(self) -> DiagnosticSeverityMapper:
        return self._severity_mapper

    def run_document_diagnostics(
        self,
        uri: str,
        text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        workspace: WorkspaceManager | None = None,
        cancellation_token: CancellationToken | None = None,
        version: int | None = None,
    ) -> DiagnosticsResult:
        with self._lock:
            result = self._run_diagnostics(
                uri=uri,
                document_text=text,
                semantic_model=semantic_model,
                config=config,
                workspace=workspace,
                cancellation_token=cancellation_token,
                version=version,
                document_mode=True,
            )
            return result

    def run_workspace_diagnostics(
        self,
        workspace: WorkspaceManager,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> DiagnosticsResult:
        with self._lock:
            all_diagnostics: dict[str, list[Diagnostic]] = {}
            total_errors = 0
            total_warnings = 0
            total_infos = 0
            total_hints = 0
            cancelled = False
            total_count = 0

            rules = self._registry.get_enabled_rules_for_workspace()
            for rule in rules:
                if cancellation_token and cancellation_token.cancelled:
                    cancelled = True
                    break
                try:
                    rule_diags = rule.check_workspace(
                        workspace=workspace,
                        semantic_model=semantic_model,
                        config=config,
                        cancellation_token=cancellation_token,
                    )
                    for diag in rule_diags:
                        diag_uri = getattr(diag, "uri", "") or ""
                        if not diag_uri:
                            continue
                        if config.max_diagnostics_per_file > 0:
                            existing = all_diagnostics.get(diag_uri, [])
                            if len(existing) >= config.max_diagnostics_per_file:
                                continue

                        if self._suppression.is_suppressed_any(diag_uri, diag):
                            continue

                        mapped_severity = self._severity_mapper.map_severity(diag.severity)
                        diag = Diagnostic(
                            range=diag.range,
                            severity=mapped_severity,
                            code=diag.code,
                            code_description=diag.code_description,
                            source=diag.source,
                            message=diag.message,
                            tags=diag.tags,
                            related_information=diag.related_information,
                            data=diag.data,
                        )

                        if diag_uri not in all_diagnostics:
                            all_diagnostics[diag_uri] = []
                        all_diagnostics[diag_uri].append(diag)
                        total_count += 1
                        if mapped_severity == DiagnosticSeverity.Error:
                            total_errors += 1
                        elif mapped_severity == DiagnosticSeverity.Warning:
                            total_warnings += 1
                        elif mapped_severity == DiagnosticSeverity.Information:
                            total_infos += 1
                        elif mapped_severity == DiagnosticSeverity.Hint:
                            total_hints += 1
                except Exception:
                    logger.exception("Rule %s failed during workspace check", rule.metadata.code)

            # Sort and limit per file
            for uri in all_diagnostics:
                all_diagnostics[uri] = self._sort_and_limit(
                    all_diagnostics[uri],
                    config.max_diagnostics_per_file,
                )

            # Apply workspace cap
            flat = [(u, d) for u, diags in all_diagnostics.items() for d in diags]
            if config.max_workspace_diagnostics > 0 and len(flat) > config.max_workspace_diagnostics:
                flat = flat[: config.max_workspace_diagnostics]
                all_diagnostics.clear()
                for u, d in flat:
                    all_diagnostics.setdefault(u, []).append(d)

            result_ids: dict[str, str] = {}
            for u in all_diagnostics:
                rid = self._publisher.get_result_id(u) or ""
                result_ids[u] = rid

            return DiagnosticsResult(
                diagnostics=all_diagnostics,
                total_count=total_count,
                errors_count=total_errors,
                warnings_count=total_warnings,
                informations_count=total_infos,
                hints_count=total_hints,
                result_ids=result_ids,
                cancelled=cancelled,
            )

    def _run_diagnostics(
        self,
        uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        workspace: WorkspaceManager | None = None,
        cancellation_token: CancellationToken | None = None,
        version: int | None = None,
        document_mode: bool = True,
    ) -> DiagnosticsResult:
        all_diagnostics: list[Diagnostic] = []
        total_errors = 0
        total_warnings = 0
        total_infos = 0
        total_hints = 0
        cancelled = False

        rules = self._registry.get_enabled_rules_for_document() if document_mode else self._registry.get_enabled_rules()

        for rule in rules:
            if cancellation_token and cancellation_token.cancelled:
                cancelled = True
                break
            try:
                rule_diags = rule.check_document(
                    document_uri=uri,
                    document_text=document_text,
                    semantic_model=semantic_model,
                    config=config,
                    cancellation_token=cancellation_token,
                )
                for diag in rule_diags:
                    if self._suppression.is_suppressed_any(uri, diag, document_text):
                        continue
                    mapped_severity = self._severity_mapper.map_severity(diag.severity)
                    diag = Diagnostic(
                        range=diag.range,
                        severity=mapped_severity,
                        code=diag.code,
                        code_description=diag.code_description,
                        source=diag.source or "aeos-lsp",
                        message=diag.message,
                        tags=self._filter_tags(diag.tags),
                        related_information=diag.related_information,
                        data=diag.data,
                    )
                    all_diagnostics.append(diag)

                    if mapped_severity == DiagnosticSeverity.Error:
                        total_errors += 1
                    elif mapped_severity == DiagnosticSeverity.Warning:
                        total_warnings += 1
                    elif mapped_severity == DiagnosticSeverity.Information:
                        total_infos += 1
                    elif mapped_severity == DiagnosticSeverity.Hint:
                        total_hints += 1
            except Exception:
                logger.exception("Rule %s failed during document check for %s", rule.metadata.code, uri)

        all_diagnostics = self._sort_and_limit(all_diagnostics, config.max_diagnostics_per_file)
        result_id = self._generate_result_id(uri, all_diagnostics, version)

        doc_diagnostics = {uri: all_diagnostics}
        result_ids = {uri: result_id}

        return DiagnosticsResult(
            diagnostics=doc_diagnostics,
            total_count=len(all_diagnostics),
            errors_count=total_errors,
            warnings_count=total_warnings,
            informations_count=total_infos,
            hints_count=total_hints,
            result_ids=result_ids,
            cancelled=cancelled,
        )

    def publish_diagnostics(
        self,
        uri: str,
        diagnostics: list[Diagnostic],
        version: int | None = None,
        force: bool = False,
    ) -> None:
        self._publisher.publish(uri, diagnostics, version, force=force)

    def update_config(self, config: LSPClientConfig) -> None:
        self._severity_mapper.update_from_config(config)
        self._publisher.update_config(config)

    def clear_document(self, uri: str) -> None:
        self._publisher.remove(uri)
        self._suppression.invalidate(uri)
        self._result_ids.pop(uri, None)

    def clear(self) -> None:
        self._publisher.clear()
        self._suppression.clear()
        self._result_ids.clear()

    def get_result_id(self, uri: str) -> str | None:
        return self._result_ids.get(uri)

    def _filter_tags(self, tags: list[DiagnosticTag] | None) -> list[DiagnosticTag] | None:
        return tags if tags else None

    @staticmethod
    def _sort_and_limit(
        diagnostics: list[Diagnostic],
        max_count: int,
    ) -> list[Diagnostic]:
        severity_order = {
            DiagnosticSeverity.Error: 0,
            DiagnosticSeverity.Warning: 1,
            DiagnosticSeverity.Information: 2,
            DiagnosticSeverity.Hint: 3,
        }

        def sort_key(d: Diagnostic) -> tuple:
            sev = severity_order.get(d.severity, 99)
            r = d.range
            return (sev, r.start.line, r.start.character, r.end.line, r.end.character)

        sorted_diags = sorted(diagnostics, key=sort_key)
        if max_count > 0 and len(sorted_diags) > max_count:
            return sorted_diags[:max_count]
        return sorted_diags

    @staticmethod
    def _generate_result_id(uri: str, diagnostics: list[Diagnostic], version: int | None) -> str:
        import hashlib
        import json

        diag_sig = hashlib.sha256(
            json.dumps(
                [{"c": d.code, "l": d.range.start.line, "m": d.message[:50]} for d in diagnostics[:50]],
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:16]
        raw = f"{uri}:{version or 0}:{diag_sig}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
