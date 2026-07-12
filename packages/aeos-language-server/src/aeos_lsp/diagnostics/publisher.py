from __future__ import annotations

import asyncio
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticTag, PublishDiagnosticsParams

from aeos_lsp.configuration import LSPClientConfig

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PublishResult:
    uri: str
    version: int | None
    diagnostics_count: int
    published: bool


@dataclass
class DocumentDiagnosticState:
    version: int
    diagnostics: list[Diagnostic]
    result_id: str | None = None
    last_publish_time: float = 0.0
    pending: bool = False


class DiagnosticPublisher:
    def __init__(
        self,
        send_notification: Any | None = None,
        debounce_ms: int = 300,
    ) -> None:
        self._lock = threading.Lock()
        self._states: dict[str, DocumentDiagnosticState] = {}
        self._debounce_timers: dict[str, threading.Timer] = {}
        self._send_notification = send_notification
        self._debounce_ms = debounce_ms
        self._supports_pull_diagnostics: bool = False
        self._client_supports_diagnostic_tags: bool = True

    def set_send_notification(self, send_notification: Any) -> None:
        self._send_notification = send_notification

    def set_supports_pull_diagnostics(self, supported: bool) -> None:
        self._supports_pull_diagnostics = supported

    def set_client_supports_diagnostic_tags(self, supported: bool) -> None:
        self._client_supports_diagnostic_tags = supported

    def publish(
        self,
        uri: str,
        diagnostics: list[Diagnostic],
        version: int | None = None,
        force: bool = False,
    ) -> PublishResult:
        with self._lock:
            prev = self._states.get(uri)
            if prev is not None and prev.version >= (version or 0) and not force:
                result_id = prev.result_id
            else:
                result_id = self._generate_result_id(uri, version or 0)

            self._states[uri] = DocumentDiagnosticState(
                version=version or 0,
                diagnostics=diagnostics,
                result_id=result_id,
                last_publish_time=time.monotonic(),
            )

        self._debounce_publish(uri, diagnostics, version)
        return PublishResult(
            uri=uri,
            version=version,
            diagnostics_count=len(diagnostics),
            published=True,
        )

    def publish_document_diagnostics(
        self,
        uri: str,
        diagnostics: list[Diagnostic],
        version: int | None = None,
    ) -> PublishResult:
        return self.publish(uri, diagnostics, version)

    def _debounce_publish(
        self,
        uri: str,
        diagnostics: list[Diagnostic],
        version: int | None,
    ) -> None:
        if uri in self._debounce_timers:
            self._debounce_timers[uri].cancel()

        def _do_publish() -> None:
            with self._lock:
                state = self._states.get(uri)
                if state is None:
                    return
                state.pending = False
                final_diags = state.diagnostics
                final_version = state.version
                result_id = state.result_id
                self._debounce_timers.pop(uri, None)

            if self._send_notification is not None:
                try:
                    params = PublishDiagnosticsParams(
                        uri=uri,
                        diagnostics=final_diags,
                        version=final_version,
                    )
                    if self._supports_pull_diagnostics:
                        extra: dict[str, Any] = {}
                        if result_id is not None:
                            extra["resultId"] = result_id
                        params = PublishDiagnosticsParams(
                            uri=uri,
                            diagnostics=final_diags,
                            version=final_version,
                        )
                    self._send_notification(params)
                except Exception:
                    logger.exception("Failed to publish diagnostics for %s", uri)

        timer = threading.Timer(self._debounce_ms / 1000.0, _do_publish)
        timer.daemon = True
        self._debounce_timers[uri] = timer
        timer.start()

    def get_diagnostics(self, uri: str) -> list[Diagnostic]:
        with self._lock:
            state = self._states.get(uri)
            if state is None:
                return []
            return list(state.diagnostics)

    def get_result_id(self, uri: str) -> str | None:
        with self._lock:
            state = self._states.get(uri)
            return state.result_id if state is not None else None

    def get_document_state(self, uri: str) -> DocumentDiagnosticState | None:
        with self._lock:
            state = self._states.get(uri)
            if state is None:
                return None
            return DocumentDiagnosticState(
                version=state.version,
                diagnostics=list(state.diagnostics),
                result_id=state.result_id,
            )

    def remove(self, uri: str) -> None:
        with self._lock:
            self._states.pop(uri, None)
            timer = self._debounce_timers.pop(uri, None)
            if timer is not None:
                timer.cancel()

    def clear(self) -> None:
        with self._lock:
            self._states.clear()
            for timer in self._debounce_timers.values():
                timer.cancel()
            self._debounce_timers.clear()

    def update_config(self, config: LSPClientConfig) -> None:
        self._debounce_ms = config.debounce_milliseconds

    @staticmethod
    def _generate_result_id(uri: str, version: int) -> str:
        import hashlib
        raw = f"{uri}:{version}:{time.monotonic_ns()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
