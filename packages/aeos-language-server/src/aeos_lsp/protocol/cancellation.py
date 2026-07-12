from __future__ import annotations

import asyncio
import logging
import threading
from typing import Any, Callable

from lsprotocol import types
from pygls.lsp.server import LanguageServer

logger = logging.getLogger(__name__)


class CancellationToken:
    def __init__(self) -> None:
        self._cancelled = threading.Event()
        self._callbacks: list[Callable[[], None]] = []

    def cancel(self) -> None:
        self._cancelled.set()
        for cb in self._callbacks:
            try:
                cb()
            except Exception:
                logger.exception("Cancellation callback failed")

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set()

    def on_cancel(self, callback: Callable[[], None]) -> None:
        if self._cancelled.is_set():
            callback()
            return
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        try:
            self._callbacks.remove(callback)
        except ValueError:
            pass

    def reset(self) -> None:
        self._cancelled.clear()
        self._callbacks.clear()

    async def wait(self) -> None:
        while not self._cancelled.is_set():
            await asyncio.sleep(0.05)


class CancellationManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._operations: dict[str, CancellationToken] = {}
        self._cleanup_interval: float = 300.0
        self._last_cleanup: float = 0.0

    def register(
        self,
        operation_id: str,
    ) -> CancellationToken:
        token = CancellationToken()
        with self._lock:
            self._operations[operation_id] = token
        logger.debug("Registered cancellable operation: %s", operation_id)
        return token

    def cancel(self, operation_id: str) -> bool:
        token: CancellationToken | None = None
        with self._lock:
            token = self._operations.get(operation_id)
        if token is None:
            logger.warning("No operation found to cancel: %s", operation_id)
            return False
        token.cancel()
        logger.info("Cancelled operation: %s", operation_id)
        return True

    def cancel_all(self) -> None:
        with self._lock:
            ops = list(self._operations.items())
            self._operations.clear()
        for op_id, token in ops:
            token.cancel()
        logger.info("Cancelled all %d operations", len(ops))

    def unregister(self, operation_id: str) -> None:
        with self._lock:
            self._operations.pop(operation_id, None)
        logger.debug("Unregistered operation: %s", operation_id)

    def get_token(self, operation_id: str) -> CancellationToken | None:
        with self._lock:
            return self._operations.get(operation_id)

    def cleanup_stale(self, max_age: float = 300.0) -> None:
        import time

        now = time.monotonic()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        self._last_cleanup = now
        logger.debug("Running cancellation cleanup")


cancellation_manager: CancellationManager = CancellationManager()


def _handle_cancel_request(
    ls: LanguageServer,
    params: types.CancelParams,
) -> None:
    operation_id = str(params.id)
    cancelled = cancellation_manager.cancel(operation_id)
    if cancelled:
        logger.info("Cancellation request handled for: %s", operation_id)
    else:
        logger.debug("Cancellation request for unknown operation: %s", operation_id)


def register_cancellation_handlers(ls: LanguageServer) -> None:
    ls.protocol.fm.add_builtin_feature(
        types.CANCEL_REQUEST,
        _handle_cancel_request,
    )
    logger.debug("Cancellation handlers registered")
