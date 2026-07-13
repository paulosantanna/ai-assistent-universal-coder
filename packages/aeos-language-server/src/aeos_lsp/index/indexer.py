from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from aeos_lsp.index.content_hash import (
    hash_content,
    hash_document,
    hash_file,
    compare_hashes,
)
from aeos_lsp.index.reference_index import ReferenceIndex
from aeos_lsp.index.sqlite_store import SqliteStore
from aeos_lsp.index.symbol_index import SymbolIndex
from aeos_lsp.parsing.base import ParseResult
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.workspace.manager import WorkspaceManager

logger = logging.getLogger(__name__)

_DEFAULT_DEBOUNCE_MS = 300
_MAX_BACKGROUND_WORKERS = 4
_PROGRESS_INTERVAL_SEC = 0.5


class IndexingStatus(Enum):
    UNINDEXED = "unindexed"
    QUEUED = "queued"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"
    STALE = "stale"


@dataclass
class DocumentIndexState:
    uri: str
    status: IndexingStatus = IndexingStatus.UNINDEXED
    content_hash: str = ""
    version: int = 0
    error: str = ""
    last_indexed: float = 0.0
    last_attempt: float = 0.0
    retry_count: int = 0


@dataclass
class ProgressReport:
    total: int = 0
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    current_uri: str = ""
    elapsed_seconds: float = 0.0


ProgressCallback = Callable[[ProgressReport], None]


class WorkspaceIndexer:
    def __init__(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
        store: SqliteStore | None = None,
        debounce_ms: int = _DEFAULT_DEBOUNCE_MS,
        max_workers: int = _MAX_BACKGROUND_WORKERS,
        follow_symlinks: bool = False,
    ) -> None:
        self._workspace_manager = workspace_manager
        self._semantic_model = semantic_model
        self._store = store or SqliteStore(
            workspace_root=workspace_manager.root_uri or Path.cwd(),
        )
        self._symbol_index = SymbolIndex(self._store)
        self._reference_index = ReferenceIndex(self._store)
        self._debounce_ms = debounce_ms
        self._max_workers = max_workers
        self._follow_symlinks = follow_symlinks
        self._lock = threading.RLock()
        self._doc_states: dict[str, DocumentIndexState] = {}
        self._debounce_timers: dict[str, float] = {}
        self._pending_uris: set[str] = set()
        self._cancel_flag = threading.Event()
        self._background_thread: threading.Thread | None = None
        self._progress_callback: ProgressCallback | None = None
        self._indexing_in_progress = False

    # ── properties ──────────────────────────────────────────────────

    @property
    def store(self) -> SqliteStore:
        return self._store

    @property
    def symbol_index(self) -> SymbolIndex:
        return self._symbol_index

    @property
    def reference_index(self) -> ReferenceIndex:
        return self._reference_index

    # ── progress reporting ─────────────────────────────────────────

    def set_progress_callback(self, callback: ProgressCallback | None) -> None:
        self._progress_callback = callback

    def _report_progress(self, report: ProgressReport) -> None:
        cb = self._progress_callback
        if cb is not None:
            try:
                cb(report)
            except Exception:
                logger.exception("Progress callback raised an exception")

    # ── document status ────────────────────────────────────────────

    def get_indexing_status(self, uri: str) -> IndexingStatus:
        with self._lock:
            state = self._doc_states.get(uri)
            if state is None:
                return IndexingStatus.UNINDEXED
            return state.status

    def get_indexing_statuses(self) -> dict[str, IndexingStatus]:
        with self._lock:
            return {uri: state.status for uri, state in self._doc_states.items()}

    def get_indexed_count(self) -> int:
        with self._lock:
            return sum(
                1 for s in self._doc_states.values()
                if s.status == IndexingStatus.INDEXED
            )

    def get_failed_count(self) -> int:
        with self._lock:
            return sum(
                1 for s in self._doc_states.values()
                if s.status == IndexingStatus.FAILED
            )

    # ── full index build ───────────────────────────────────────────

    def build_full_index(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
        on_progress: ProgressCallback | None = None,
    ) -> None:
        self._cancel_flag.clear()
        self._indexing_in_progress = True

        if on_progress is not None:
            self.set_progress_callback(on_progress)

        try:
            start_time = time.monotonic()

            with self._lock:
                self._doc_states.clear()
                self._pending_uris.clear()
                self._debounce_timers.clear()

            with self._store.transaction():
                self._store.clear_all()
                semantic_model.build_from_workspace(workspace_manager)

            uris_to_index = self._collect_uris(workspace_manager)
            total = len(uris_to_index)

            report = ProgressReport(total=total, elapsed_seconds=0.0)
            self._report_progress(report)

            for i, uri in enumerate(uris_to_index):
                if self._cancel_flag.is_set():
                    logger.info("Full index build cancelled after %d/%d documents", i, total)
                    break

                try:
                    self._set_status(uri, IndexingStatus.QUEUED)
                    self._index_single_document(uri, workspace_manager, semantic_model)
                except Exception:
                    logger.exception("Failed to index %s during full build", uri)
                    self._set_status(uri, IndexingStatus.FAILED, error=str(sys.exc_info()[1]))

                elapsed = time.monotonic() - start_time
                report = ProgressReport(
                    total=total,
                    completed=i + 1,
                    failed=self.get_failed_count(),
                    current_uri=uri,
                    elapsed_seconds=elapsed,
                )
                self._report_progress(report)

            self._store.commit()
            elapsed = time.monotonic() - start_time
            logger.info(
                "Full index build completed: %d documents in %.2fs",
                self.get_indexed_count(), elapsed,
            )

        finally:
            self._indexing_in_progress = False

    def _collect_uris(self, workspace_manager: WorkspaceManager) -> list[str]:
        uris: list[str] = []
        seen: set[str] = set()
        exclusions = workspace_manager.exclusions

        for folder in workspace_manager.workspace_folders:
            folder_path = folder.path
            if not folder_path.is_dir():
                continue

            for root, dirs, files in os.walk(
                str(folder_path),
                followlinks=self._follow_symlinks,
                topdown=True,
            ):
                root_path = Path(root)

                dirs[:] = [
                    d for d in dirs
                    if not exclusions.matches_exclusion(root_path / d)
                ]

                for file_name in files:
                    file_path = root_path / file_name
                    if exclusions.matches_exclusion(file_path):
                        continue

                    uri = file_path.as_uri()
                    norm = uri.lower()
                    if norm not in seen:
                        seen.add(norm)
                        uris.append(uri)

        return uris

    # ── incremental update ─────────────────────────────────────────

    def update_index_for_document(
        self,
        uri: str,
        parse_result: ParseResult[Any],
    ) -> None:
        try:
            self._set_status(uri, IndexingStatus.INDEXING)

            content_hash = hash_document(uri, str(parse_result.ast))

            with self._store.transaction():
                self._store.delete_references_for_uri(uri)
                self._store.delete_symbols_by_uri(uri)
                self._store.delete_diagnostics(uri)

                self._semantic_model.update_for_document(uri, parse_result)

                symbols = self._semantic_model.get_symbols_by_uri(uri)
                symbol_rows = []
                for sym in symbols:
                    metadata = getattr(sym, "metadata", {})
                    selection_range = self._range_to_json(
                        getattr(sym, "selection_range", None)
                    )
                    full_range = self._range_to_json(
                        getattr(sym, "full_range", None)
                    )
                    symbol_rows.append({
                        "stable_id": sym.stable_id,
                        "kind": getattr(sym, "kind", sym.symbol_kind).value
                            if hasattr(getattr(sym, "kind", sym.symbol_kind), "value")
                            else str(getattr(sym, "kind", "unknown")),
                        "name": getattr(sym, "name", sym.stable_id),
                        "uri": uri,
                        "selection_range": selection_range,
                        "full_range": full_range,
                        "content_hash": content_hash,
                        "metadata": metadata,
                    })

                self._store.upsert_symbols_batch(symbol_rows)

                refs = self._semantic_model.reference_table.get_for_uri(uri)
                ref_rows = []
                for ref in refs:
                    ref_rows.append({
                        "source_uri": ref.source_uri,
                        "source_range": self._range_to_json(ref.source_range),
                        "target_uri": ref.target_uri,
                        "target_range": self._range_to_json(ref.target_range),
                        "kind": ref.kind.value if hasattr(ref.kind, "value") else str(ref.kind),
                        "role": ref.role.value if hasattr(ref.role, "value") else str(ref.role),
                    })
                self._store.insert_references_batch(ref_rows)

                parse_errors = [
                    {
                        "message": e.message,
                        "range": self._range_to_json(e.range),
                        "severity": e.severity.value,
                        "code": e.code,
                    }
                    for e in parse_result.errors
                ]
                self._store.upsert_document(
                    uri=uri,
                    content_hash=content_hash,
                    version=self._get_doc_version(uri) + 1,
                    last_indexed=_now_iso(),
                    parse_errors=parse_errors,
                )

                diagnostic_rows = []
                for err in parse_result.errors:
                    diagnostic_rows.append({
                        "uri": uri,
                        "code": err.code,
                        "message": err.message,
                        "range_json": self._range_to_json(err.range),
                        "severity": err.severity.value,
                    })
                if diagnostic_rows:
                    self._store.insert_diagnostics_batch(diagnostic_rows)

            self._set_status(uri, IndexingStatus.INDEXED)

        except Exception:
            logger.exception("Failed to update index for %s", uri)
            self._set_status(uri, IndexingStatus.FAILED, error=str(sys.exc_info()[1]))
            raise

    # ── removal ─────────────────────────────────────────────────────

    def remove_document_from_index(self, uri: str) -> None:
        try:
            with self._lock:
                self._pending_uris.discard(uri)
                self._debounce_timers.pop(uri, None)
                self._doc_states.pop(uri, None)

            with self._store.transaction():
                self._store.delete_references_for_uri(uri)
                self._store.delete_symbols_by_uri(uri)
                self._store.delete_diagnostics(uri)
                self._store.delete_document(uri)

            self._semantic_model.remove_document(uri)
            logger.info("Removed %s from index", uri)

        except Exception:
            logger.exception("Failed to remove %s from index", uri)
            raise

    # ── debounced reindexing ───────────────────────────────────────

    def schedule_reindex(self, uri: str) -> None:
        with self._lock:
            self._debounce_timers[uri] = time.monotonic()
            self._pending_uris.add(uri)

    def _process_debounced(self) -> None:
        now = time.monotonic()
        with self._lock:
            ready = [
                uri for uri, ts in self._debounce_timers.items()
                if (now - ts) * 1000 >= self._debounce_ms
            ]
            for uri in ready:
                self._debounce_timers.pop(uri, None)
                self._pending_uris.discard(uri)
        return ready

    def flush_pending_updates(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
    ) -> int:
        ready = self._process_debounced()
        for uri in ready:
            try:
                doc = workspace_manager.document_store.get(uri)
                if doc is None:
                    continue
                parse_result = self._parse_document(uri, doc.text, workspace_manager)
                if parse_result is not None:
                    self.update_index_for_document(uri, parse_result)
            except Exception:
                logger.exception("Failed to flush update for %s", uri)
        return len(ready)

    def cancel_pending_updates(self) -> None:
        with self._lock:
            self._pending_uris.clear()
            self._debounce_timers.clear()

    # ── background indexing ────────────────────────────────────────

    def start_background_indexing(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
    ) -> None:
        if self._background_thread is not None and self._background_thread.is_alive():
            logger.warning("Background indexing is already running")
            return

        self._cancel_flag.clear()
        self._background_thread = threading.Thread(
            target=self._background_worker,
            args=(workspace_manager, semantic_model),
            name="aeos-indexer",
            daemon=True,
        )
        self._background_thread.start()
        logger.info("Background indexing started")

    def stop_background_indexing(self, wait: bool = True) -> None:
        self._cancel_flag.set()
        if self._background_thread is not None and wait:
            self._background_thread.join(timeout=30)
            logger.info("Background indexing stopped")

    def _background_worker(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
    ) -> None:
        while not self._cancel_flag.is_set():
            try:
                ready = self._process_debounced()
                for uri in ready:
                    if self._cancel_flag.is_set():
                        return
                    try:
                        doc = workspace_manager.document_store.get(uri)
                        if doc is None:
                            continue
                        parse_result = self._parse_document(uri, doc.text, workspace_manager)
                        if parse_result is not None:
                            self.update_index_for_document(uri, parse_result)
                    except Exception:
                        logger.exception("Background index failed for %s", uri)

                if not ready:
                    time.sleep(0.1)

            except Exception:
                logger.exception("Error in background indexing worker")
                time.sleep(1.0)

    # ── cache invalidation by content hash ─────────────────────────

    def invalidate_by_content_hash(self, content_hash: str) -> list[str]:
        invalidated: list[str] = []
        with self._store.transaction():
            uris = self._store.conn.execute(
                "SELECT uri FROM documents WHERE content_hash = ?", (content_hash,)
            ).fetchall()
            for (uri,) in uris:
                self._store.delete_references_for_uri(uri)
                self._store.delete_symbols_by_uri(uri)
                self._store.delete_diagnostics(uri)
                self._store.delete_document(uri)
                invalidated.append(uri)
                self._semantic_model.remove_document(uri)
                self._set_status(uri, IndexingStatus.STALE)
        return invalidated

    def has_content_changed(self, uri: str, new_content: str) -> bool:
        old_hash = self._store.get_document_content_hash(uri)
        if old_hash is None:
            return True
        new_hash = hash_document(uri, new_content)
        return not compare_hashes(old_hash, new_hash)

    # ── corruption recovery ────────────────────────────────────────

    def check_integrity(self) -> bool:
        try:
            results = self._store.integrity_check()
            ok = all(r == "ok" for r in results)
            if not ok:
                logger.warning("Database integrity check failed: %s", results)
            return ok
        except Exception:
            logger.exception("Integrity check raised an exception")
            return False

    def recover_from_corruption(
        self,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
    ) -> None:
        logger.warning("Attempting recovery from possible index corruption")
        try:
            self._store.close()
            db_path = self._store.db_path
            if db_path.exists():
                backup = db_path.with_suffix(".sqlite.corrupted")
                import shutil
                shutil.copy2(str(db_path), str(backup))
                db_path.unlink()
                logger.info("Backed up corrupted database to %s", backup)

            self._store = SqliteStore(db_path=db_path)
            self._symbol_index = SymbolIndex(self._store)
            self._reference_index = ReferenceIndex(self._store)

            self.build_full_index(workspace_manager, semantic_model)
            logger.info("Index rebuilt from scratch after corruption recovery")

        except Exception:
            logger.exception("Failed to recover from corruption")
            raise

    # ── helpers ────────────────────────────────────────────────────

    def _set_status(
        self,
        uri: str,
        status: IndexingStatus,
        error: str = "",
    ) -> None:
        with self._lock:
            state = self._doc_states.get(uri)
            if state is None:
                state = DocumentIndexState(uri=uri)
                self._doc_states[uri] = state
            state.status = status
            state.last_attempt = time.monotonic()
            if status == IndexingStatus.INDEXED:
                state.last_indexed = time.monotonic()
                state.retry_count = 0
                state.error = ""
            elif status == IndexingStatus.FAILED:
                state.error = error
                state.retry_count += 1

    def _index_single_document(
        self,
        uri: str,
        workspace_manager: WorkspaceManager,
        semantic_model: SemanticModel,
    ) -> None:
        doc = workspace_manager.document_store.get(uri)
        if doc is None:
            file_path = self._uri_to_path(uri)
            if file_path is None or not file_path.is_file():
                self._set_status(uri, IndexingStatus.FAILED, error="File not found")
                return
            text = file_path.read_text(encoding="utf-8", errors="replace")
        else:
            text = doc.text

        parse_result = self._parse_document(uri, text, workspace_manager)
        if parse_result is None:
            self._set_status(uri, IndexingStatus.FAILED, error="No parser found")
            return

        self.update_index_for_document(uri, parse_result)

    def _parse_document(
        self,
        uri: str,
        text: str,
        workspace_manager: WorkspaceManager,
    ) -> ParseResult[Any] | None:
        dispatcher = getattr(workspace_manager, "dispatcher", None)
        if dispatcher is None:
            try:
                from aeos_lsp.parsing.dispatcher import ParserDispatcher
                dispatcher = ParserDispatcher()
            except ImportError:
                logger.warning("ParserDispatcher not available, using fallback")
                return None
        return dispatcher.parse(text, uri)

    def _get_doc_version(self, uri: str) -> int:
        doc = self._store.get_document(uri)
        if doc is None:
            return 0
        return doc.get("version", 0)

    @staticmethod
    def _range_to_json(range_obj: Any) -> str:
        if range_obj is None:
            return json.dumps({"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}})
        if isinstance(range_obj, dict):
            return json.dumps(range_obj)
        try:
            return json.dumps({
                "start": {"line": range_obj.start.line, "character": range_obj.start.character},
                "end": {"line": range_obj.end.line, "character": range_obj.end.character},
            })
        except AttributeError:
            return json.dumps({"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}})

    @staticmethod
    def _uri_to_path(uri: str) -> Path | None:
        if uri.startswith("file://"):
            from urllib.parse import unquote
            path_str = unquote(uri[7:])
            if path_str.startswith("/") and len(path_str) > 2 and path_str[2] == ":":
                path_str = path_str[1:]
            return Path(path_str)
        return Path(uri) if uri else None

    def close(self) -> None:
        self.stop_background_indexing(wait=True)
        self._store.close()

    def __enter__(self) -> WorkspaceIndexer:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


import sys


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
