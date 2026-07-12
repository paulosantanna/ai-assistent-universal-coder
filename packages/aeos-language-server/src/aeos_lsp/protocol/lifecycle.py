from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from aeos_lsp.constants import (
    BACKGROUND_INDEXING_DEFAULT,
    DEBOUNCE_MILLISECONDS_DEFAULT,
    ENABLE_EXPERIMENTAL_FEATURES_DEFAULT,
    SERVER_NAME,
    SERVER_PROTOCOL_VERSION,
    SERVER_VERSION,
)
from aeos_lsp.protocol.cancellation import cancellation_manager
from aeos_lsp.protocol.errors import register_error_handlers
from aeos_lsp.protocol.progress import ProgressManager
from aeos_lsp.protocol.text_sync import PositionEncoding, TextSynchronizer

logger = logging.getLogger(__name__)


@dataclass
class AEOSInitializeResult:
    server_info: types.ServerInfo
    capabilities: types.ServerCapabilities
    position_encoding: PositionEncoding = PositionEncoding.UTF16
    experimental_features: dict[str, Any] = field(default_factory=dict)
    initialization_options: dict[str, Any] = field(default_factory=dict)


class AEOSLifecycleManager:
    def __init__(
        self,
        ls: LanguageServer,
    ) -> None:
        self._ls = ls
        self._lock = threading.Lock()
        self._initialized = threading.Event()
        self._shutting_down = False
        self._shutdown_complete = threading.Event()
        self._background_tasks: list[threading.Thread] = []
        self._resource_cleanup: list[Callable[[], None]] = []
        self._experimental_enabled: bool = ENABLE_EXPERIMENTAL_FEATURES_DEFAULT
        self._position_encoding: PositionEncoding = PositionEncoding.UTF16
        self._root_uri: str | None = None
        self._workspace_folders: list[types.WorkspaceFolder] = []
        self._client_info: types.ClientInfo | None = None
        self._on_initialized_callbacks: list[Callable[[], None]] = []
        self._text_sync: TextSynchronizer | None = None

    @property
    def initialized(self) -> bool:
        return self._initialized.is_set()

    @property
    def shutting_down(self) -> bool:
        return self._shutting_down

    @property
    def position_encoding(self) -> PositionEncoding:
        return self._position_encoding

    @property
    def root_uri(self) -> str | None:
        return self._root_uri

    @property
    def workspace_folders(self) -> list[types.WorkspaceFolder]:
        with self._lock:
            return list(self._workspace_folders)

    @property
    def experimental_enabled(self) -> bool:
        return self._experimental_enabled

    @property
    def client_info(self) -> types.ClientInfo | None:
        return self._client_info

    def on_initialized(self, callback: Callable[[], None]) -> None:
        if self._initialized.is_set():
            try:
                callback()
            except Exception:
                logger.exception("Deferred initialization callback failed")
            return
        self._on_initialized_callbacks.append(callback)

    def handle_initialize(
        self,
        params: types.InitializeParams,
    ) -> AEOSInitializeResult:
        logger.info(
            "Initializing server: %s v%s (protocol: %s)",
            SERVER_NAME,
            SERVER_VERSION,
            SERVER_PROTOCOL_VERSION,
        )

        self._client_info = params.client_info
        self._root_uri = params.root_uri

        if params.workspace_folders is not None:
            with self._lock:
                self._workspace_folders = list(params.workspace_folders)

        client_capabilities = params.capabilities
        self._position_encoding = PositionEncoding.negotiate(client_capabilities)

        initialization_options = params.initialization_options or {}
        self._experimental_enabled = initialization_options.get(
            "enableExperimentalFeatures",
            ENABLE_EXPERIMENTAL_FEATURES_DEFAULT,
        )

        text_sync_kind = types.TextDocumentSyncKind.Incremental
        debounce_ms = initialization_options.get(
            "debounceMilliseconds",
            DEBOUNCE_MILLISECONDS_DEFAULT,
        )
        self._text_sync = TextSynchronizer(
            self._ls,
            debounce_ms=debounce_ms,
        )

        server_capabilities = types.ServerCapabilities()
        server_capabilities.text_document_sync = types.TextDocumentSyncOptions(
            open_close=True,
            change=text_sync_kind,
            will_save=True,
            will_save_wait_until=False,
            save=types.SaveOptions(include_text=True),
        )
        server_capabilities.position_encoding = self._position_encoding.to_lsp_type()

        workspace_cap = types.WorkspaceOptions(
            workspace_folders=types.WorkspaceFoldersServerCapabilities(
                supported=True,
                change_notifications=True,
            ),
        )
        server_capabilities.workspace = workspace_cap

        server_capabilities.completion_provider = types.CompletionOptions(
            trigger_characters=[".", "/", "@", "$", ":", "\"", "'"],
            resolve_provider=True,
        )
        server_capabilities.hover_provider = True
        server_capabilities.definition_provider = True
        server_capabilities.declaration_provider = True
        server_capabilities.implementation_provider = True
        server_capabilities.references_provider = True
        server_capabilities.document_highlight_provider = True
        server_capabilities.document_symbol_provider = True
        server_capabilities.workspace_symbol_provider = True
        server_capabilities.rename_provider = types.RenameOptions(prepare_provider=True)
        server_capabilities.code_action_provider = True
        server_capabilities.code_lens_provider = types.CodeLensOptions(resolve_provider=True)
        server_capabilities.document_link_provider = types.DocumentLinkOptions(resolve_provider=True)
        server_capabilities.inlay_hint_provider = True
        server_capabilities.signature_help_provider = types.SignatureHelpOptions(trigger_characters=["(", ","])
        server_capabilities.semantic_tokens_provider = types.SemanticTokensOptions(
            legend=types.SemanticTokensLegend(token_types=[], token_modifiers=[]),
            full=True,
            range=True,
        )
        server_capabilities.folding_range_provider = True
        server_capabilities.selection_range_provider = True
        server_capabilities.document_formatting_provider = True
        server_capabilities.document_range_formatting_provider = True
        server_capabilities.document_on_type_formatting_provider = types.DocumentOnTypeFormattingOptions(first_trigger_character="\n")
        server_capabilities.call_hierarchy_provider = True
        server_capabilities.type_hierarchy_provider = True

        server_capabilities.execute_command_provider = types.ExecuteCommandOptions(
            commands=[],
        )

        experimental: dict[str, Any] = {}
        if self._experimental_enabled:
            experimental = {
                "enhancedDiagnostics": True,
                "incrementalIndexing": True,
                "realTimeGovernance": True,
                "capabilityNegotiation": True,
            }

        server_capabilities.experimental = experimental if experimental else None

        result = AEOSInitializeResult(
            server_info=types.ServerInfo(
                name=SERVER_NAME,
                version=SERVER_VERSION,
            ),
            capabilities=server_capabilities,
            position_encoding=self._position_encoding,
            experimental_features=experimental,
            initialization_options=initialization_options,
        )

        logger.info(
            "Server capabilities: textSync=%s, positionEncoding=%s, experimental=%s",
            text_sync_kind,
            self._position_encoding.value,
            self._experimental_enabled,
        )

        return result

    def handle_initialized(self) -> None:
        logger.info("Server fully initialized")

        self._initialized.set()

        if BACKGROUND_INDEXING_DEFAULT:
            self._start_background_indexing()

        for callback in self._on_initialized_callbacks:
            try:
                callback()
            except Exception:
                logger.exception("Initialization callback failed")
        self._on_initialized_callbacks.clear()

    def _start_background_indexing(self) -> None:
        def _index_task() -> None:
            logger.info("Background indexing started")
            start = time.monotonic()
            try:
                duration = time.monotonic() - start
                logger.info("Background indexing completed in %.2fs", duration)
            except Exception:
                logger.exception("Background indexing failed")

        index_thread = threading.Thread(
            target=_index_task,
            name="aeos-background-index",
            daemon=True,
        )
        index_thread.start()
        self._background_tasks.append(index_thread)

    def register_cleanup(self, cleanup: Callable[[], None]) -> None:
        with self._lock:
            self._resource_cleanup.append(cleanup)

    def handle_shutdown(self) -> None:
        logger.info("Server shutdown requested")
        self._shutting_down = True

        cancellation_manager.cancel_all()

        with self._lock:
            cleanup_tasks = list(self._resource_cleanup)
            self._resource_cleanup.clear()
        for cleanup in cleanup_tasks:
            try:
                cleanup()
            except Exception:
                logger.exception("Cleanup task failed")

        if self._text_sync is not None:
            self._text_sync.reset()

        self._shutdown_complete.set()
        logger.info("Server shutdown complete")

    def handle_exit(self) -> None:
        logger.info("Server exit")
        self._shutting_down = True
        cancellation_manager.cancel_all()
        if not self._shutdown_complete.is_set():
            self.handle_shutdown()

    def wait_for_shutdown(self, timeout: float = 10.0) -> bool:
        return self._shutdown_complete.wait(timeout=timeout)

    def handle_workspace_did_change_configuration(
        self,
        params: types.DidChangeConfigurationParams,
    ) -> None:
        settings = params.settings or {}
        if isinstance(settings, dict):
            self._experimental_enabled = settings.get(
                "enableExperimentalFeatures",
                self._experimental_enabled,
            )
        logger.debug("Workspace configuration changed: %s", settings)

    def handle_workspace_did_change_watched_files(
        self,
        params: types.DidChangeWatchedFilesParams,
    ) -> None:
        for change in params.changes:
            logger.debug(
                "File %s changed (type=%s)",
                change.uri,
                change.type,
            )

    def handle_workspace_did_change_workspace_folders(
        self,
        params: types.DidChangeWorkspaceFoldersParams,
    ) -> None:
        with self._lock:
            for removed in params.event.removed:
                self._workspace_folders = [
                    wf
                    for wf in self._workspace_folders
                    if wf.uri != removed.uri
                ]
                logger.info("Workspace folder removed: %s", removed.uri)
            for added in params.event.added:
                self._workspace_folders.append(added)
                logger.info("Workspace folder added: %s (%s)", added.name, added.uri)


def _handle_initialize(
    ls: LanguageServer,
    params: types.InitializeParams,
) -> types.InitializeResult:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    result = manager.handle_initialize(params)

    # Create the workspace on the protocol.
    # Normally pygls's built-in lsp_initialize generator does this, but AEOS
    # replaces that handler with this function, so we must do it ourselves.
    from pygls.uris import from_fs_path
    from pygls.workspace import Workspace

    root_path = params.root_path
    root_uri = params.root_uri
    if root_path is not None and root_uri is None:
        root_uri = from_fs_path(root_path)
    workspace_folders = params.workspace_folders or []
    position_encoding = result.position_encoding.to_lsp_type()
    ls.protocol._workspace = Workspace(
        root_uri,
        ls._text_document_sync_kind,
        workspace_folders,
        position_encoding,
    )

    return types.InitializeResult(
        capabilities=result.capabilities,
        server_info=result.server_info,
    )


def _handle_initialized(
    ls: LanguageServer,
    params: types.InitializedParams,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_initialized()


def _handle_shutdown(
    ls: LanguageServer,
    params: None,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_shutdown()


def _handle_exit(
    ls: LanguageServer,
    params: None,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_exit()
    if hasattr(ls, "_stop_event"):
        ls._stop_event.set()


def _handle_workspace_did_change_configuration(
    ls: LanguageServer,
    params: types.DidChangeConfigurationParams,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_workspace_did_change_configuration(params)


def _handle_workspace_did_change_watched_files(
    ls: LanguageServer,
    params: types.DidChangeWatchedFilesParams,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_workspace_did_change_watched_files(params)


def _handle_workspace_did_change_workspace_folders(
    ls: LanguageServer,
    params: types.DidChangeWorkspaceFoldersParams,
) -> None:
    manager: AEOSLifecycleManager = ls.protocol._aeos_lifecycle  # type: ignore[attr-defined]
    manager.handle_workspace_did_change_workspace_folders(params)


def register_lifecycle_handlers(
    ls: LanguageServer,
    manager: AEOSLifecycleManager,
) -> None:
    ls.protocol._aeos_lifecycle = manager  # type: ignore[attr-defined]

    register_error_handlers(ls)

    from functools import partial

    ls.protocol.fm.add_builtin_feature(
        types.INITIALIZE,
        partial(_handle_initialize, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.INITIALIZED,
        partial(_handle_initialized, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.SHUTDOWN,
        partial(_handle_shutdown, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.EXIT,
        partial(_handle_exit, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.WORKSPACE_DID_CHANGE_CONFIGURATION,
        partial(_handle_workspace_did_change_configuration, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.WORKSPACE_DID_CHANGE_WATCHED_FILES,
        partial(_handle_workspace_did_change_watched_files, ls),
    )
    ls.protocol.fm.add_builtin_feature(
        types.WORKSPACE_DID_CHANGE_WORKSPACE_FOLDERS,
        partial(_handle_workspace_did_change_workspace_folders, ls),
    )

    logger.debug("Lifecycle handlers registered")
