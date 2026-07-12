from __future__ import annotations

import enum
import logging
import threading
import time
from typing import Any, Callable

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from aeos_lsp.protocol.errors import AEOSErrorCodes, JsonRpcError

logger = logging.getLogger(__name__)


class PositionEncoding(enum.Enum):
    UTF8 = types.PositionEncodingKind.Utf8
    UTF16 = types.PositionEncodingKind.Utf16
    UTF32 = types.PositionEncodingKind.Utf32

    @classmethod
    def negotiate(
        cls,
        client_capabilities: types.ClientCapabilities,
    ) -> PositionEncoding:
        general = client_capabilities.general
        if general is not None and general.position_encodings is not None:
            for enc in general.position_encodings:
                if enc == types.PositionEncodingKind.Utf8:
                    return cls.UTF8
                if enc == types.PositionEncodingKind.Utf32:
                    return cls.UTF32
                if enc == types.PositionEncodingKind.Utf16:
                    return cls.UTF16
        return cls.UTF16

    def to_lsp_type(self) -> types.PositionEncodingKind:
        return types.PositionEncodingKind(self.value)


class DebouncedChange:
    def __init__(
        self,
        delay_ms: float = 300.0,
    ) -> None:
        self._delay = delay_ms / 1000.0
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self._pending: dict[str, float] = {}
        self._last_fire: dict[str, float] = {}

    def debounce(
        self,
        uri: str,
        callback: Callable[[], None],
    ) -> None:
        with self._lock:
            self._pending[uri] = time.monotonic()

            if self._timer is not None and self._timer.is_alive():
                self._timer.cancel()

            timer = threading.Timer(self._delay, self._flush, args=[callback])
            timer.daemon = True
            self._timer = timer
            timer.start()

    def _flush(self, callback: Callable[[], None]) -> None:
        now = time.monotonic()
        with self._lock:
            pending = dict(self._pending)
            self._pending.clear()
        if not pending:
            return
        try:
            callback()
        except Exception:
            logger.exception("Debounced callback failed")

    def cancel_pending(self, uri: str | None = None) -> None:
        with self._lock:
            if uri is None:
                self._pending.clear()
            else:
                self._pending.pop(uri, None)
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

    @property
    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)


class TextSynchronizer:
    def __init__(
        self,
        ls: LanguageServer,
        debounce_ms: float = 300.0,
    ) -> None:
        self._ls = ls
        self._debouncer = DebouncedChange(delay_ms=debounce_ms)
        self._lock = threading.Lock()
        self._open_documents: dict[str, int] = {}

    def handle_open(
        self,
        params: types.DidOpenTextDocumentParams,
    ) -> None:
        uri = params.text_document.uri
        version = params.text_document.version

        with self._lock:
            self._open_documents[uri] = version

        logger.info("Document opened: %s (version %d)", uri, version)

    def handle_change(
        self,
        params: types.DidChangeTextDocumentParams,
    ) -> None:
        uri = params.text_document.uri
        new_version = params.text_document.version

        with self._lock:
            current_version = self._open_documents.get(uri)
            if current_version is not None and new_version is not None:
                if new_version < current_version:
                    raise JsonRpcError(
                        code=AEOSErrorCodes.DocumentVersionStale,
                        message=(
                            f"Stale document version {new_version} for {uri}; "
                            f"current is {current_version}"
                        ),
                        data={
                            "uri": uri,
                            "expected": current_version,
                            "received": new_version,
                        },
                    )
                self._open_documents[uri] = new_version

        content_changes = params.content_changes
        logger.debug(
            "Document changed: %s (version %d, %d change(s))",
            uri,
            new_version,
            len(content_changes),
        )

    def handle_save(
        self,
        params: types.DidSaveTextDocumentParams,
    ) -> None:
        uri = params.text_document.uri
        logger.info("Document saved: %s", uri)

    def handle_close(
        self,
        params: types.DidCloseTextDocumentParams,
    ) -> None:
        uri = params.text_document.uri
        with self._lock:
            self._open_documents.pop(uri, None)
        self._debouncer.cancel_pending(uri)
        logger.info("Document closed: %s", uri)

    def is_open(self, uri: str) -> bool:
        with self._lock:
            return uri in self._open_documents

    def get_version(self, uri: str) -> int | None:
        with self._lock:
            return self._open_documents.get(uri)

    def debounce_change(
        self,
        uri: str,
        callback: Callable[[], None],
    ) -> None:
        self._debouncer.debounce(uri, callback)

    def wait_for_debounce(self) -> None:
        while self._debouncer.pending_count > 0:
            time.sleep(0.01)

    def reset(self) -> None:
        with self._lock:
            self._open_documents.clear()
            self._debouncer.cancel_pending()


def _handle_did_open(
    ls: LanguageServer,
    params: types.DidOpenTextDocumentParams,
) -> None:
    sync: TextSynchronizer = ls.protocol._aeos_text_sync  # type: ignore[attr-defined]
    sync.handle_open(params)


def _handle_did_change(
    ls: LanguageServer,
    params: types.DidChangeTextDocumentParams,
) -> None:
    sync: TextSynchronizer = ls.protocol._aeos_text_sync  # type: ignore[attr-defined]
    sync.handle_change(params)


def _handle_did_save(
    ls: LanguageServer,
    params: types.DidSaveTextDocumentParams,
) -> None:
    sync: TextSynchronizer = ls.protocol._aeos_text_sync  # type: ignore[attr-defined]
    sync.handle_save(params)


def _handle_did_close(
    ls: LanguageServer,
    params: types.DidCloseTextDocumentParams,
) -> None:
    sync: TextSynchronizer = ls.protocol._aeos_text_sync  # type: ignore[attr-defined]
    sync.handle_close(params)


def register_text_sync_handlers(
    ls: LanguageServer,
    sync: TextSynchronizer,
) -> None:
    ls.protocol._aeos_text_sync = sync  # type: ignore[attr-defined]
    logger.debug("Text sync handlers registered")
