from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

from aeos_lsp.index.content_hash import hash_content as _compute_hash
from aeos_lsp.index.migrations import ensure_schema, CURRENT_SCHEMA_VERSION
from aeos_lsp.constants import CACHE_DIR_NAME, INDEX_DB_NAME

logger = logging.getLogger(__name__)

_REDACTED = "<REDACTED>"
_SENSITIVE_KEYS = frozenset({
    "secret", "password", "token", "key", "credential",
    "api_key", "apikey", "passwd", "auth",
})

_MAX_RETRIES = 3
_RETRY_DELAY_MS = 50


def _redact_value(value: object) -> object:
    if isinstance(value, dict):
        return {k: _redact_value(v) if k.lower() not in _SENSITIVE_KEYS else _REDACTED for k, v in value.items()}
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, str):
        for key in _SENSITIVE_KEYS:
            if key in value.lower():
                return _REDACTED
    return value


def _redact_json(data: str) -> str:
    try:
        parsed = json.loads(data)
        redacted = _redact_value(parsed)
        return json.dumps(redacted, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        return data


class SqliteStore:
    def __init__(
        self,
        workspace_root: Path | str | None = None,
        db_path: Path | str | None = None,
    ) -> None:
        self._lock = threading.RLock()
        self._conn: sqlite3.Connection | None = None
        self._ref_count = 0
        self._closed = False

        if db_path is not None:
            self._db_path = Path(db_path)
        elif workspace_root is not None:
            root = Path(workspace_root).resolve()
            self._db_path = root / ".aeos" / CACHE_DIR_NAME / INDEX_DB_NAME
        else:
            self._db_path = Path(".aeos") / CACHE_DIR_NAME / INDEX_DB_NAME

        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._connect()

    # ── connection management ──────────────────────────────────────

    def _connect(self) -> None:
        for attempt in range(_MAX_RETRIES):
            try:
                self._conn = sqlite3.connect(
                    str(self._db_path),
                    timeout=10.0,
                    check_same_thread=False,
                )
                self._conn.execute("PRAGMA journal_mode=WAL")
                self._conn.execute("PRAGMA synchronous=NORMAL")
                self._conn.execute("PRAGMA busy_timeout=5000")
                self._conn.execute("PRAGMA foreign_keys=ON")
                self._conn.execute("PRAGMA cache_size=-8000")
                self._conn.row_factory = sqlite3.Row

                if not ensure_schema(self._conn):
                    raise RuntimeError(
                        f"Failed to ensure schema at version {CURRENT_SCHEMA_VERSION}"
                    )
                return
            except sqlite3.Error:
                logger.exception(
                    "SQLite connect attempt %d/%d failed for %s",
                    attempt + 1, _MAX_RETRIES, self._db_path,
                )
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY_MS / 1000)
        raise RuntimeError(f"Could not connect to SQLite database at {self._db_path}")

    @property
    def db_path(self) -> Path:
        return self._db_path

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            raise RuntimeError("SqliteStore is not connected")
        return self._conn

    def acquire(self) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("SqliteStore is closed")
            self._ref_count += 1

    def release(self) -> None:
        with self._lock:
            self._ref_count -= 1
            if self._ref_count <= 0 and self._closed:
                self._close_connection()

    # ── transaction helpers ─────────────────────────────────────────

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    def begin(self) -> None:
        self.conn.execute("BEGIN IMMEDIATE")

    def commit(self) -> None:
        self.conn.commit()

    def rollback(self) -> None:
        self.conn.rollback()

    # ── symbols ─────────────────────────────────────────────────────

    _INSERT_SYMBOL = (
        "INSERT OR REPLACE INTO symbols "
        "(stable_id, kind, name, uri, selection_range, full_range, content_hash, metadata_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )

    def upsert_symbol(
        self,
        stable_id: str,
        kind: str,
        name: str,
        uri: str,
        selection_range: str,
        full_range: str,
        content_hash: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        meta_json = json.dumps(_redact_value(metadata or {}), ensure_ascii=False)
        self.conn.execute(
            self._INSERT_SYMBOL,
            (stable_id, kind, name, uri, selection_range, full_range, content_hash, meta_json),
        )

    def upsert_symbols_batch(self, symbols: list[dict[str, Any]]) -> None:
        rows = []
        for sym in symbols:
            meta_json = json.dumps(_redact_value(sym.get("metadata", {})), ensure_ascii=False)
            rows.append((
                sym["stable_id"], sym["kind"], sym["name"], sym["uri"],
                sym["selection_range"], sym["full_range"],
                sym.get("content_hash", ""), meta_json,
            ))
        self.conn.executemany(self._INSERT_SYMBOL, rows)

    def delete_symbol(self, stable_id: str) -> None:
        self.conn.execute("DELETE FROM symbols WHERE stable_id = ?", (stable_id,))

    def delete_symbols_by_uri(self, uri: str) -> int:
        cursor = self.conn.execute("DELETE FROM symbols WHERE uri = ?", (uri,))
        return cursor.rowcount

    def get_symbol(self, stable_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM symbols WHERE stable_id = ?", (stable_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_symbols_by_uri(self, uri: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM symbols WHERE uri = ? ORDER BY name", (uri,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── references ──────────────────────────────────────────────────

    _INSERT_REFERENCE = (
        "INSERT INTO references_ "
        "(source_uri, source_range, target_uri, target_range, kind, role) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )

    def insert_reference(
        self,
        source_uri: str,
        source_range: str,
        target_uri: str,
        target_range: str,
        kind: str = "usage",
        role: str = "reference",
    ) -> None:
        self.conn.execute(
            self._INSERT_REFERENCE,
            (source_uri, source_range, target_uri, target_range, kind, role),
        )

    def insert_references_batch(self, refs: list[dict[str, Any]]) -> None:
        rows = [
            (
                r["source_uri"], r["source_range"], r["target_uri"],
                r["target_range"], r.get("kind", "usage"), r.get("role", "reference"),
            )
            for r in refs
        ]
        self.conn.executemany(self._INSERT_REFERENCE, rows)

    def delete_references_by_source_uri(self, uri: str) -> int:
        cursor = self.conn.execute("DELETE FROM references_ WHERE source_uri = ?", (uri,))
        return cursor.rowcount

    def delete_references_by_target_uri(self, uri: str) -> int:
        cursor = self.conn.execute("DELETE FROM references_ WHERE target_uri = ?", (uri,))
        return cursor.rowcount

    def delete_references_for_uri(self, uri: str) -> None:
        self.conn.execute(
            "DELETE FROM references_ WHERE source_uri = ? OR target_uri = ?",
            (uri, uri),
        )

    # ── dependencies ────────────────────────────────────────────────

    _INSERT_DEPENDENCY = (
        "INSERT OR IGNORE INTO dependencies (source_id, target_id, kind) VALUES (?, ?, ?)"
    )

    def upsert_dependency(self, source_id: str, target_id: str, kind: str = "") -> None:
        self.conn.execute(self._INSERT_DEPENDENCY, (source_id, target_id, kind))

    def upsert_dependencies_batch(self, deps: list[dict[str, Any]]) -> None:
        rows = [(d["source_id"], d["target_id"], d.get("kind", "")) for d in deps]
        self.conn.executemany(self._INSERT_DEPENDENCY, rows)

    def delete_dependencies_by_source(self, source_id: str) -> int:
        cursor = self.conn.execute(
            "DELETE FROM dependencies WHERE source_id = ?", (source_id,)
        )
        return cursor.rowcount

    def delete_dependencies_by_target(self, target_id: str) -> int:
        cursor = self.conn.execute(
            "DELETE FROM dependencies WHERE target_id = ?", (target_id,)
        )
        return cursor.rowcount

    def clear_dependencies(self) -> None:
        self.conn.execute("DELETE FROM dependencies")

    # ── documents ──────────────────────────────────────────────────

    _UPSERT_DOCUMENT = (
        "INSERT OR REPLACE INTO documents "
        "(uri, content_hash, version, last_indexed, parse_errors_json) "
        "VALUES (?, ?, ?, ?, ?)"
    )

    def upsert_document(
        self,
        uri: str,
        content_hash: str,
        version: int = 0,
        last_indexed: str = "",
        parse_errors: list[dict[str, Any]] | None = None,
    ) -> None:
        errors_json = json.dumps(parse_errors or [], ensure_ascii=False)
        self.conn.execute(
            self._UPSERT_DOCUMENT,
            (uri, content_hash, version, last_indexed, errors_json),
        )

    def get_document(self, uri: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM documents WHERE uri = ?", (uri,)
        ).fetchone()
        return dict(row) if row else None

    def get_document_content_hash(self, uri: str) -> str | None:
        row = self.conn.execute(
            "SELECT content_hash FROM documents WHERE uri = ?", (uri,)
        ).fetchone()
        return row[0] if row else None

    def delete_document(self, uri: str) -> bool:
        cursor = self.conn.execute("DELETE FROM documents WHERE uri = ?", (uri,))
        return cursor.rowcount > 0

    def list_document_uris(self) -> list[str]:
        rows = self.conn.execute("SELECT uri FROM documents ORDER BY uri").fetchall()
        return [r[0] for r in rows]

    def document_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) FROM documents").fetchone()
        return row[0] if row else 0

    # ── diagnostics ─────────────────────────────────────────────────

    _INSERT_DIAGNOSTIC = (
        "INSERT INTO diagnostics "
        "(uri, code, message, range_json, severity, tags_json, related_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )

    def insert_diagnostic(
        self,
        uri: str,
        code: str = "",
        message: str = "",
        range_json: str = "{}",
        severity: int = 1,
        tags: list[str] | None = None,
        related: list[dict[str, Any]] | None = None,
    ) -> None:
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        related_json = json.dumps(related or [], ensure_ascii=False)
        self.conn.execute(
            self._INSERT_DIAGNOSTIC,
            (uri, code, message, range_json, severity, tags_json, related_json),
        )

    def insert_diagnostics_batch(self, diagnostics: list[dict[str, Any]]) -> None:
        rows = []
        for d in diagnostics:
            rows.append((
                d["uri"], d.get("code", ""), d.get("message", ""),
                d.get("range_json", "{}"), d.get("severity", 1),
                json.dumps(d.get("tags", []), ensure_ascii=False),
                json.dumps(d.get("related", []), ensure_ascii=False),
            ))
        self.conn.executemany(self._INSERT_DIAGNOSTIC, rows)

    def get_diagnostics(self, uri: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM diagnostics WHERE uri = ? ORDER BY severity", (uri,)
        ).fetchall()
        return [dict(r) for r in rows]

    def delete_diagnostics(self, uri: str) -> int:
        cursor = self.conn.execute("DELETE FROM diagnostics WHERE uri = ?", (uri,))
        return cursor.rowcount

    def clear_diagnostics(self) -> None:
        self.conn.execute("DELETE FROM diagnostics")

    # ── meta ─────────────────────────────────────────────────────────

    def get_meta(self, key: str) -> str | None:
        row = self.conn.execute(
            "SELECT value FROM meta WHERE key = ?", (key,)
        ).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value),
        )

    def delete_meta(self, key: str) -> bool:
        cursor = self.conn.execute("DELETE FROM meta WHERE key = ?", (key,))
        return cursor.rowcount > 0

    # ── maintenance ────────────────────────────────────────────────

    def vacuum(self) -> None:
        self.conn.execute("VACUUM")
        logger.info("Database vacuum completed for %s", self._db_path)

    def analyze(self) -> None:
        self.conn.execute("ANALYZE")
        logger.info("Database analysis completed for %s", self._db_path)

    def integrity_check(self) -> list[str]:
        rows = self.conn.execute("PRAGMA integrity_check").fetchall()
        return [r[0] for r in rows]

    def clear_all(self) -> None:
        for table in ("symbols", "references_", "dependencies", "documents", "diagnostics"):
            self.conn.execute(f"DELETE FROM {table}")
        logger.info("All index data cleared from %s", self._db_path)

    # ── stats ───────────────────────────────────────────────────────

    def get_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {}
        for table in ("symbols", "references_", "dependencies", "documents", "diagnostics"):
            row = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            stats[table] = row[0] if row else 0
        page_count = self.conn.execute("PRAGMA page_count").fetchone()
        page_size = self.conn.execute("PRAGMA page_size").fetchone()
        if page_count and page_size:
            stats["database_size_bytes"] = page_count[0] * page_size[0]
        stats["schema_version"] = CURRENT_SCHEMA_VERSION
        stats["db_path"] = str(self._db_path)
        return stats

    # ── lifecycle ───────────────────────────────────────────────────

    def close(self) -> None:
        with self._lock:
            self._closed = True
            if self._ref_count <= 0:
                self._close_connection()

    def _close_connection(self) -> None:
        if self._conn is not None:
            try:
                self._conn.execute("PRAGMA optimize")
                self._conn.close()
            except sqlite3.Error:
                logger.exception("Error closing SQLite connection")
            finally:
                self._conn = None

    def __enter__(self) -> SqliteStore:
        self.acquire()
        return self

    def __exit__(self, *args: Any) -> None:
        self.release()


class _Transaction:
    def __init__(self, store: SqliteStore) -> None:
        self._store = store

    def __enter__(self) -> SqliteStore:
        self._store.begin()
        return self._store

    def __exit__(self, exc_type: type | None, *args: Any) -> None:
        if exc_type is None:
            try:
                self._store.commit()
            except sqlite3.Error:
                logger.exception("Commit failed in transaction, rolling back")
                self._store.rollback()
                raise
        else:
            self._store.rollback()
