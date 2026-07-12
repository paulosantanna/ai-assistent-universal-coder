from __future__ import annotations

import asyncio
import logging
import signal
import threading
import time
from pathlib import Path
from typing import Any, Callable

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DECLARATION,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_DOCUMENT_HIGHLIGHT,
    TEXT_DOCUMENT_DOCUMENT_LINK,
    TEXT_DOCUMENT_DOCUMENT_SYMBOL,
    TEXT_DOCUMENT_FOLDING_RANGE,
    TEXT_DOCUMENT_FORMATTING,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_IMPLEMENTATION,
    TEXT_DOCUMENT_INLAY_HINT,
    INLAY_HINT_RESOLVE,
    TEXT_DOCUMENT_ON_TYPE_FORMATTING,
    TEXT_DOCUMENT_PREPARE_RENAME,
    TEXT_DOCUMENT_RANGE_FORMATTING,
    TEXT_DOCUMENT_REFERENCES,
    TEXT_DOCUMENT_RENAME,
    TEXT_DOCUMENT_SELECTION_RANGE,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL_DELTA,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_RANGE,
    TEXT_DOCUMENT_SIGNATURE_HELP,
    TEXT_DOCUMENT_CODE_ACTION,
    CODE_ACTION_RESOLVE,
    TEXT_DOCUMENT_CODE_LENS,
    CODE_LENS_RESOLVE,
    COMPLETION_ITEM_RESOLVE,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_WILL_SAVE,
    DOCUMENT_LINK_RESOLVE,
    TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS,
    WORKSPACE_DID_CHANGE_CONFIGURATION,
    WORKSPACE_DID_CHANGE_WATCHED_FILES,
    WORKSPACE_DID_CHANGE_WORKSPACE_FOLDERS,
    WORKSPACE_EXECUTE_COMMAND,
    WORKSPACE_SYMBOL,
    WINDOW_LOG_MESSAGE,
    WINDOW_SHOW_MESSAGE,
    WINDOW_WORK_DONE_PROGRESS_CANCEL,
    CallHierarchyIncomingCallsParams,
    CallHierarchyOutgoingCallsParams,
    CallHierarchyPrepareParams,
    CodeActionParams,
    CodeLensParams,
    CompletionParams,
    DeclarationParams,
    DefinitionParams,
    DidChangeTextDocumentParams,
    DidChangeWatchedFilesParams,
    DidChangeWorkspaceFoldersParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentFormattingParams,
    DocumentHighlightParams,
    DocumentLinkParams,
    DocumentOnTypeFormattingParams,
    DocumentRangeFormattingParams,
    DocumentSymbolParams,
    ExecuteCommandParams,
    FoldingRangeParams,
    HoverParams,
    ImplementationParams,
    InlayHintParams,
    PrepareRenameParams,
    ReferenceParams,
    RenameParams,
    SelectionRangeParams,
    SemanticTokensDeltaParams,
    SemanticTokensParams,
    SemanticTokensRangeParams,
    SignatureHelpParams,
    TypeHierarchySupertypesParams,
    TypeHierarchySubtypesParams,
    WillSaveTextDocumentParams,
    WorkspaceSymbolParams,
    SaveOptions,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.capabilities import build_server_capabilities
from aeos_lsp.configuration import LSPClientConfig, merge_config
from aeos_lsp.constants import (
    BACKGROUND_INDEXING_DEFAULT,
    DEBOUNCE_MILLISECONDS_DEFAULT,
    EXIT_SUCCESS,
    INDEXING_CONCURRENCY_DEFAULT,
    SERVER_NAME,
    SERVER_VERSION,
)
from aeos_lsp.logging_config import get_logger

logger = get_logger(__name__)

_server_instance: AEOSLanguageServer | None = None
_instance_lock = threading.Lock()


def get_server() -> AEOSLanguageServer:
    global _server_instance
    if _server_instance is None:
        raise RuntimeError("AEOSLanguageServer not yet initialized")
    return _server_instance


class AEOSLanguageServer(LanguageServer):
    def __init__(
        self,
        config: LSPClientConfig | None = None,
    ) -> None:
        super().__init__(
            name=SERVER_NAME,
            version=SERVER_VERSION,
        )

        global _server_instance
        with _instance_lock:
            _server_instance = self

        self._config = config or LSPClientConfig()
        self._lazy_initialized = False
        self._shutdown_initiated = False
        self._shutdown_lock = threading.RLock()
        self._background_tasks: list[threading.Thread] = []
        self._component_lock = threading.RLock()

        self._workspace_manager = None
        self._parsers = None
        self._semantic_model = None
        self._indexer = None
        self._diagnostics_engine = None
        self._schema_registry = None
        self._command_registry = None

        self._completion_feature = None
        self._completion_resolve_feature = None
        self._hover_feature = None
        self._definition_feature = None
        self._declaration_feature = None
        self._implementation_feature = None
        self._references_feature = None
        self._document_highlight_feature = None
        self._document_symbols_feature = None
        self._workspace_symbols_feature = None
        self._prepare_rename_feature = None
        self._rename_feature = None
        self._code_actions_feature = None
        self._code_action_resolve_feature = None
        self._code_lens_feature = None
        self._code_lens_resolve_feature = None
        self._semantic_tokens_feature = None
        self._folding_feature = None
        self._selection_range_feature = None
        self._formatting_feature = None
        self._range_formatting_feature = None
        self._on_type_formatting_feature = None
        self._document_links_feature = None
        self._inlay_hints_feature = None
        self._signature_help_feature = None
        self._call_hierarchy_feature = None
        self._type_hierarchy_feature = None

    @property
    def aeos_config(self) -> LSPClientConfig:
        return self._config

    @property
    def workspace_manager(self):
        if self._workspace_manager is None:
            self._lazy_init()
        return self._workspace_manager

    @property
    def parsers(self):
        if self._parsers is None:
            self._lazy_init()
        return self._parsers

    @property
    def semantic_model(self):
        if self._semantic_model is None:
            self._lazy_init()
        return self._semantic_model

    @property
    def indexer(self):
        if self._indexer is None:
            self._lazy_init()
        return self._indexer

    @property
    def diagnostics_engine(self):
        if self._diagnostics_engine is None:
            self._lazy_init()
        return self._diagnostics_engine

    @property
    def schema_registry(self):
        if self._schema_registry is None:
            self._lazy_init()
        return self._schema_registry

    @property
    def command_registry(self):
        if self._command_registry is None:
            self._lazy_init()
        return self._command_registry

    def _lazy_init(self) -> None:
        with self._component_lock:
            if self._lazy_initialized:
                return
            logger.info("Performing lazy initialization of all components")
            self._init_workspace_manager()
            self._init_parsers()
            self._init_semantic_model()
            self._init_indexer()
            self._init_diagnostics_engine()
            self._init_schema_registry()
            self._init_command_registry()
            self._init_features()
            self._register_lifecycle_handlers()
            self._register_text_sync_handlers()
            self._register_feature_handlers()
            self._register_command_handlers()
            self._lazy_initialized = True
            logger.info("Lazy initialization complete")

    def _init_workspace_manager(self) -> None:
        from aeos_lsp.workspace import WorkspaceManager
        self._workspace_manager = WorkspaceManager()
        self._workspace_manager.update_config(self._config)
        logger.debug("WorkspaceManager initialized")

    def _init_parsers(self) -> None:
        from aeos_lsp.parsing import ParserDispatcher
        self._parsers = ParserDispatcher()
        logger.debug("ParserDispatcher initialized")

    def _init_semantic_model(self) -> None:
        from aeos_lsp.semantic import SemanticModel
        self._semantic_model = SemanticModel()
        logger.debug("SemanticModel initialized")

    def _init_indexer(self) -> None:
        from aeos_lsp.index import WorkspaceIndexer, SqliteStore
        store = SqliteStore(
            workspace_root=self._workspace_manager.root_uri or Path.cwd(),
        )
        self._indexer = WorkspaceIndexer(
            workspace_manager=self._workspace_manager,
            semantic_model=self._semantic_model,
            store=store,
            debounce_ms=self._config.debounce_milliseconds,
            max_workers=self._config.indexing_concurrency,
        )
        logger.debug("WorkspaceIndexer initialized")

    def _init_diagnostics_engine(self) -> None:
        from aeos_lsp.diagnostics import DiagnosticsEngine, DiagnosticRuleRegistry, DiagnosticPublisher, SuppressionManager, DiagnosticSeverityMapper
        from aeos_lsp.output import DiagnosticFormatter, OutputLimiter, OutputCompactor
        from aeos_lsp.diagnostics.registry import DiagnosticRuleRegistry
        registry = DiagnosticRuleRegistry()
        registry.register_defaults()
        self._diagnostics_engine = DiagnosticsEngine(
            registry=registry,
            publisher=DiagnosticPublisher(),
            suppression_manager=SuppressionManager(),
            severity_mapper=DiagnosticSeverityMapper(),
        )
        logger.debug("DiagnosticsEngine initialized")

    def _init_schema_registry(self) -> None:
        from aeos_lsp.schemas import SchemaRegistry, SchemaLoader, SchemaValidator
        from aeos_lsp.workspace import detect_aeos_root
        root = None
        if self._workspace_manager.root_uri:
            root = detect_aeos_root(self._workspace_manager.root_uri)
        loader = SchemaLoader(schema_dirs=[root] if root else None)
        self._schema_registry = SchemaRegistry(loader=loader)
        logger.debug("SchemaRegistry initialized")

    def _init_command_registry(self) -> None:
        from aeos_lsp.commands import CommandRegistry
        self._command_registry = CommandRegistry()
        self._command_registry.register_defaults()
        logger.debug("CommandRegistry initialized")

    def _init_features(self) -> None:
        from aeos_lsp.features import (
            CompletionFeature,
            CompletionResolveFeature,
            HoverFeature,
            DefinitionFeature,
            DeclarationFeature,
            ImplementationFeature,
            ReferencesFeature,
            DocumentHighlightFeature,
            DocumentSymbolsFeature,
            WorkspaceSymbolsFeature,
            PrepareRenameFeature,
            RenameFeature,
            CodeActionsFeature,
            CodeActionResolveFeature,
            CodeLensFeature,
            CodeLensResolveFeature,
            SemanticTokensFeature,
            FoldingFeature,
            SelectionRangeFeature,
            FormattingFeature,
            RangeFormattingFeature,
            DocumentLinksFeature,
            InlayHintsFeature,
            SignatureHelpFeature,
            CallHierarchyFeature,
            TypeHierarchyFeature,
        )
        self._completion_feature = CompletionFeature(self, self._semantic_model)
        self._completion_resolve_feature = CompletionResolveFeature(self, self._semantic_model)
        self._hover_feature = HoverFeature(self, self._semantic_model)
        self._definition_feature = DefinitionFeature(self, self._semantic_model)
        self._declaration_feature = DeclarationFeature(self, self._semantic_model)
        self._implementation_feature = ImplementationFeature(self, self._semantic_model)
        self._references_feature = ReferencesFeature(self, self._semantic_model)
        self._document_highlight_feature = DocumentHighlightFeature(self, self._semantic_model)
        self._document_symbols_feature = DocumentSymbolsFeature(self, self._semantic_model)
        self._workspace_symbols_feature = WorkspaceSymbolsFeature(self, self._semantic_model)
        self._prepare_rename_feature = PrepareRenameFeature(self, self._semantic_model)
        self._rename_feature = RenameFeature(self, self._semantic_model)
        self._code_actions_feature = CodeActionsFeature(self, self._semantic_model)
        self._code_action_resolve_feature = CodeActionResolveFeature(self, self._semantic_model)
        self._code_lens_feature = CodeLensFeature(self, self._semantic_model)
        self._code_lens_resolve_feature = CodeLensResolveFeature(self, self._semantic_model)
        self._semantic_tokens_feature = SemanticTokensFeature(self, self._semantic_model)
        self._folding_feature = FoldingFeature(self)
        self._selection_range_feature = SelectionRangeFeature(self, self._semantic_model)
        self._formatting_feature = FormattingFeature(self)
        self._range_formatting_feature = RangeFormattingFeature(self)
        self._document_links_feature = DocumentLinksFeature(self)
        self._inlay_hints_feature = InlayHintsFeature(self, self._semantic_model)
        self._signature_help_feature = SignatureHelpFeature(self, self._semantic_model)
        self._call_hierarchy_feature = CallHierarchyFeature(self, self._semantic_model)
        self._type_hierarchy_feature = TypeHierarchyFeature(self, self._semantic_model)
        logger.debug("All feature instances created")

    def _register_lifecycle_handlers(self) -> None:
        from aeos_lsp.protocol import register_lifecycle_handlers, AEOSLifecycleManager, register_cancellation_handlers, register_progress_handlers
        self._lifecycle_manager = AEOSLifecycleManager(self)
        register_lifecycle_handlers(self, self._lifecycle_manager)
        register_cancellation_handlers(self)
        register_progress_handlers(self)
        logger.debug("Lifecycle handlers registered")

    def _register_text_sync_handlers(self) -> None:
        from aeos_lsp.protocol import TextSynchronizer, register_text_sync_handlers
        self._text_sync = TextSynchronizer(
            self,
            debounce_ms=self._config.debounce_milliseconds,
        )
        register_text_sync_handlers(self, self._text_sync)
        logger.debug("Text sync handlers registered")

    def _register_feature_handlers(self) -> None:
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_COMPLETION,
            self._completion_feature.provide_completions,
        )
        self.protocol.fm.add_builtin_feature(
            COMPLETION_ITEM_RESOLVE,
            self._completion_resolve_feature.resolve_completion,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_HOVER,
            self._hover_feature.provide_hover,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DEFINITION,
            self._definition_feature.provide_definition,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DECLARATION,
            self._declaration_feature.provide_declaration,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_IMPLEMENTATION,
            self._implementation_feature.provide_implementation,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_REFERENCES,
            self._references_feature.provide_references,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DOCUMENT_HIGHLIGHT,
            self._document_highlight_feature.provide_highlight,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DOCUMENT_SYMBOL,
            self._document_symbols_feature.provide_symbols,
        )
        self.protocol.fm.add_builtin_feature(
            WORKSPACE_SYMBOL,
            self._workspace_symbols_feature.provide_workspace_symbols,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_PREPARE_RENAME,
            self._prepare_rename_feature.prepare_rename,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_RENAME,
            self._rename_feature.rename,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_CODE_ACTION,
            self._code_actions_feature.provide_code_actions,
        )
        self.protocol.fm.add_builtin_feature(
            CODE_ACTION_RESOLVE,
            self._code_action_resolve_feature.resolve_code_action,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_CODE_LENS,
            self._code_lens_feature.provide_code_lenses,
        )
        self.protocol.fm.add_builtin_feature(
            CODE_LENS_RESOLVE,
            self._code_lens_resolve_feature.resolve_code_lens,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
            self._semantic_tokens_feature.provide_semantic_tokens,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL_DELTA,
            self._semantic_tokens_feature.provide_semantic_tokens_delta,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_SEMANTIC_TOKENS_RANGE,
            self._semantic_tokens_feature.provide_semantic_tokens_range,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_FOLDING_RANGE,
            self._folding_feature.provide_folding_ranges,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_SELECTION_RANGE,
            self._selection_range_feature.provide_selection_ranges,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_FORMATTING,
            self._formatting_feature.provide_formatting,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_RANGE_FORMATTING,
            self._range_formatting_feature.provide_range_formatting,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_ON_TYPE_FORMATTING,
            self._on_type_formatting_handler,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DOCUMENT_LINK,
            self._document_links_feature.provide_document_links,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_INLAY_HINT,
            self._inlay_hints_feature.provide_inlay_hints,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_SIGNATURE_HELP,
            self._signature_help_feature.provide_signature_help,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DID_OPEN,
            self._on_did_open_text_document,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DID_CHANGE,
            self._on_did_change_text_document,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DID_SAVE,
            self._on_did_save_text_document,
        )
        self.protocol.fm.add_builtin_feature(
            TEXT_DOCUMENT_DID_CLOSE,
            self._on_did_close_text_document,
        )
        self.protocol.fm.add_builtin_feature(
            WORKSPACE_EXECUTE_COMMAND,
            self._on_execute_command,
        )

        logger.debug("Feature handlers registered")

    def _register_command_handlers(self) -> None:
        from lsprotocol.types import WORKSPACE_EXECUTE_COMMAND
        self.protocol.fm.add_builtin_feature(
            WORKSPACE_EXECUTE_COMMAND,
            self._on_execute_command,
        )
        logger.debug("Command handlers registered")

    def _on_did_open_text_document(self, params: DidOpenTextDocumentParams) -> None:
        self.text_sync.handle_open(params)
        # Register document in the pygls workspace so get_document works
        # (normally done by pygls's built-in lsp_text_document__did_open,
        #  but that handler is replaced by this one)
        if self.workspace:
            self.workspace.put_text_document(params.text_document)
        self._schedule_diagnostics(params.text_document.uri)

    def _on_did_change_text_document(self, params: DidChangeTextDocumentParams) -> None:
        self.text_sync.handle_change(params)
        # Keep the pygls workspace in sync
        if self.workspace:
            for change in params.content_changes:
                self.workspace.update_text_document(params.text_document, change)
        self.debounce_change(
            params.text_document.uri,
            lambda: self._schedule_diagnostics(params.text_document.uri),
        )

    def _on_did_save_text_document(self, params: DidSaveTextDocumentParams) -> None:
        self.text_sync.handle_save(params)
        self._schedule_diagnostics(params.text_document.uri)

    def _on_did_close_text_document(self, params: DidCloseTextDocumentParams) -> None:
        self.text_sync.handle_close(params)
        uri = params.text_document.uri
        # Keep the pygls workspace in sync
        if self.workspace:
            self.workspace.remove_text_document(uri)
        if self._semantic_model is not None:
            self._semantic_model.remove_document(uri)

    def _on_execute_command(self, params: ExecuteCommandParams) -> Any:
        command = params.command
        args = params.arguments or {}
        if not isinstance(args, dict):
            args = {}
        from aeos_lsp.commands import CommandNotFoundError, CommandValidationError
        try:
            return self._command_registry.dispatch(command, self, args)
        except CommandNotFoundError:
            logger.warning("Unknown command: %s", command)
            return None
        except CommandValidationError as e:
            logger.warning("Command validation failed: %s", e.message)
            return None

    def _schedule_diagnostics(self, uri: str) -> None:
        if self._diagnostics_engine is None:
            return
        try:
            from lsprotocol.types import Diagnostic
            doc_text = ""
            if self.workspace:
                doc = self.workspace.get_text_document(uri)
                if doc:
                    doc_text = doc.source
            if self._parsers is not None:
                parse_result = self._parsers.parse(uri, doc_text)
            else:
                parse_result = None
            if self._semantic_model is not None and parse_result is not None:
                self._semantic_model.update_for_document(uri, parse_result)
            result = self._diagnostics_engine.run_document_diagnostics(
                uri, doc_text, self._semantic_model, self._config,
                workspace=self._workspace_manager,
            )
            self._publish_diagnostics(uri, result.diagnostics.get(uri, []))
        except Exception:
            logger.exception("Failed to compute diagnostics for %s", uri)

    def _publish_diagnostics(self, uri: str, diagnostics: list) -> None:
        from lsprotocol.types import PublishDiagnosticsParams
        self.protocol.notify(
            TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS,
            PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics),
        )

    @property
    def text_sync(self):
        if not hasattr(self, "_text_sync") or self._text_sync is None:
            from aeos_lsp.protocol import TextSynchronizer
            self._text_sync = TextSynchronizer(
                self,
                debounce_ms=self._config.debounce_milliseconds,
            )
        return self._text_sync

    @property
    def lifecycle_manager(self):
        if not hasattr(self, "_lifecycle_manager") or self._lifecycle_manager is None:
            from aeos_lsp.protocol import AEOSLifecycleManager
            self._lifecycle_manager = AEOSLifecycleManager(self)
        return self._lifecycle_manager

    def _on_type_formatting_handler(self, params: DocumentOnTypeFormattingParams) -> None:
        pass

    def debounce_change(self, uri: str, callback: Callable[[], None]) -> None:
        self.text_sync.debounce_change(uri, callback)

    def start_background_indexing(self) -> None:
        if self._indexer is None:
            return
        thread = threading.Thread(
            target=self._background_index_task,
            name="aeos-bg-indexer",
            daemon=True,
        )
        thread.start()
        self._background_tasks.append(thread)
        logger.info("Background indexing started")

    def _background_index_task(self) -> None:
        try:
            from aeos_lsp.index import ProgressReport
            def progress_callback(report: ProgressReport) -> None:
                if report.total > 0:
                    percentage = int((report.completed / report.total) * 100)
                    message = f"Indexing: {report.completed}/{report.total} ({percentage}%)"
                    self._lifecycle_manager._progress = message

            self._indexer.index_workspace(
                progress_callback=progress_callback,
            )
            logger.info("Background indexing complete")
        except Exception:
            logger.exception("Background indexing failed")

    def rebuild_index(self) -> None:
        if self._indexer is None:
            self._lazy_init()
        if self._semantic_model is not None:
            self._semantic_model.clear()
        if self._indexer is not None:
            self._indexer.clear_index()
        self.start_background_indexing()

    def shutdown(self) -> None:
        with self._shutdown_lock:
            if self._shutdown_initiated:
                return
            self._shutdown_initiated = True

        logger.info("Shutting down AEOS Language Server")

        if self._lifecycle_manager is not None:
            self._lifecycle_manager.handle_shutdown()

        for thread in self._background_tasks:
            if thread.is_alive():
                thread.join(timeout=5)

        if self._indexer is not None:
            try:
                self._indexer.close()
            except Exception:
                logger.exception("Error closing indexer")

        if self._workspace_manager is not None and self._workspace_manager.file_watcher is not None:
            try:
                self._workspace_manager.file_watcher.stop()
            except Exception:
                logger.exception("Error stopping file watcher")

        if self._semantic_model is not None:
            self._semantic_model.clear()

        with _instance_lock:
            global _server_instance
            _server_instance = None

        logger.info("AEOS Language Server shutdown complete")

    def start_tcp(self, host: str = "127.0.0.1", port: int = 2087) -> None:
        self._lazy_init()
        logger.info("Starting TCP server on %s:%d", host, port)
        self.start_ws(host=host, port=port)

    def start_stdio(self) -> None:
        self._lazy_init()
        logger.info("Starting stdio server")
        self.start_io()

    def __repr__(self) -> str:
        return f"AEOSLanguageServer(initialized={self._lazy_initialized}, shutdown={self._shutdown_initiated})"
