from __future__ import annotations

import asyncio
import logging
import threading
import time
from typing import Any, Callable

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from aeos_lsp.protocol.cancellation import CancellationToken, cancellation_manager

logger = logging.getLogger(__name__)


class ProgressReporter:
    def __init__(
        self,
        ls: LanguageServer,
        token: types.ProgressToken,
        title: str,
        message: str = "",
        percentage: int = 0,
        cancellable: bool = False,
    ) -> None:
        self._ls = ls
        self._token = token
        self._title = title
        self._message = message
        self._percentage = percentage
        self._cancellable = cancellable
        self._ended = False
        self._cancel_token: CancellationToken | None = None
        self._lock = threading.Lock()

    def begin(
        self,
        message: str | None = None,
        percentage: int = 0,
    ) -> None:
        value = types.WorkDoneProgressBegin(
            kind="begin",
            title=self._title,
            message=message or self._message,
            percentage=percentage,
            cancellable=self._cancellable,
        )
        self._ls.progress.begin(self._token, value)
        logger.debug("Progress began: %s", self._title)

    def report(
        self,
        message: str | None = None,
        percentage: int | None = None,
    ) -> None:
        with self._lock:
            if self._ended:
                return
            if message is not None:
                self._message = message
            if percentage is not None:
                self._percentage = percentage
            value = types.WorkDoneProgressReport(
                kind="report",
                message=self._message,
                percentage=self._percentage,
            )
            self._ls.progress.report(self._token, value)

    def end(self, message: str | None = None) -> None:
        with self._lock:
            if self._ended:
                return
            self._ended = True
        value = types.WorkDoneProgressEnd(
            kind="end",
            message=message,
        )
        self._ls.progress.end(self._token, value)
        logger.debug("Progress ended: %s", self._title)

    @property
    def cancelled(self) -> bool:
        if self._cancel_token is None:
            return False
        return self._cancel_token.cancelled

    def attach_cancellation(self, operation_id: str) -> None:
        self._cancel_token = cancellation_manager.register(operation_id)
        self._cancel_token.on_cancel(self._on_cancelled)

    def _on_cancelled(self) -> None:
        self.end(message="Operation cancelled")


class ProgressManager:
    def __init__(self, ls: LanguageServer) -> None:
        self._ls = ls
        self._lock = threading.Lock()
        self._active: dict[types.ProgressToken, ProgressReporter] = {}
        self._creation_lock = threading.Lock()

    def create(
        self,
        token: types.ProgressToken,
        title: str,
        message: str = "",
        percentage: int = 0,
        cancellable: bool = False,
    ) -> ProgressReporter:
        reporter = ProgressReporter(
            ls=self._ls,
            token=token,
            title=title,
            message=message,
            percentage=percentage,
            cancellable=cancellable,
        )
        with self._lock:
            self._active[token] = reporter
        return reporter

    def create_and_begin(
        self,
        token: types.ProgressToken,
        title: str,
        message: str = "",
        percentage: int = 0,
        cancellable: bool = False,
    ) -> ProgressReporter:
        reporter = self.create(
            token=token,
            title=title,
            message=message,
            percentage=percentage,
            cancellable=cancellable,
        )
        reporter.begin()
        return reporter

    def get(self, token: types.ProgressToken) -> ProgressReporter | None:
        with self._lock:
            return self._active.get(token)

    def end(self, token: types.ProgressToken, message: str | None = None) -> None:
        reporter = self.get(token)
        if reporter is not None:
            reporter.end(message=message)
            with self._lock:
                self._active.pop(token, None)

    def end_all(self, message: str | None = None) -> None:
        with self._lock:
            tokens = list(self._active.keys())
        for token in tokens:
            self.end(token, message=message)

    async def create_async(
        self,
        token: types.ProgressToken,
        title: str,
        cancellable: bool = False,
    ) -> ProgressReporter:
        reporter = self.create(
            token=token,
            title=title,
            cancellable=cancellable,
        )
        await self._ls.window_work_done_progress_create_async(
            types.WorkDoneProgressCreateParams(token=token)
        )
        reporter.begin()
        return reporter


def _handle_work_done_progress_cancel(
    ls: LanguageServer,
    params: types.WorkDoneProgressCancelParams,
) -> None:
    token = params.token
    logger.info("Work done progress cancel received for token: %s", token)


def register_progress_handlers(ls: LanguageServer) -> None:
    ls.protocol.fm.add_builtin_feature(
        types.WINDOW_WORK_DONE_PROGRESS_CANCEL,
        _handle_work_done_progress_cancel,
    )
    logger.debug("Progress handlers registered")
