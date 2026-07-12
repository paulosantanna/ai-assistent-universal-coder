from __future__ import annotations

import logging
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)

SCHEMA_VERSION_KEY = "schema_version"
CURRENT_SCHEMA_VERSION = 1


def _migrate_v1(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS symbols (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            stable_id   TEXT    NOT NULL,
            kind        TEXT    NOT NULL,
            name        TEXT    NOT NULL,
            uri         TEXT    NOT NULL,
            selection_range TEXT NOT NULL,
            full_range     TEXT NOT NULL,
            content_hash   TEXT NOT NULL DEFAULT '',
            metadata_json  TEXT NOT NULL DEFAULT '{}',
            UNIQUE(stable_id)
        );

        CREATE INDEX IF NOT EXISTS idx_symbols_kind     ON symbols(kind);
        CREATE INDEX IF NOT EXISTS idx_symbols_name     ON symbols(name);
        CREATE INDEX IF NOT EXISTS idx_symbols_uri      ON symbols(uri);
        CREATE INDEX IF NOT EXISTS idx_symbols_stable_id ON symbols(stable_id);

        CREATE TABLE IF NOT EXISTS references_ (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source_uri  TEXT    NOT NULL,
            source_range TEXT   NOT NULL,
            target_uri  TEXT    NOT NULL,
            target_range TEXT   NOT NULL,
            kind        TEXT    NOT NULL DEFAULT 'usage',
            role        TEXT    NOT NULL DEFAULT 'reference'
        );

        CREATE INDEX IF NOT EXISTS idx_refs_source ON references_(source_uri);
        CREATE INDEX IF NOT EXISTS idx_refs_target ON references_(target_uri);
        CREATE INDEX IF NOT EXISTS idx_refs_kind   ON references_(kind);

        CREATE TABLE IF NOT EXISTS dependencies (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            kind      TEXT NOT NULL DEFAULT '',
            UNIQUE(source_id, target_id)
        );

        CREATE INDEX IF NOT EXISTS idx_deps_source ON dependencies(source_id);
        CREATE INDEX IF NOT EXISTS idx_deps_target ON dependencies(target_id);

        CREATE TABLE IF NOT EXISTS documents (
            uri             TEXT    PRIMARY KEY,
            content_hash    TEXT    NOT NULL DEFAULT '',
            version         INTEGER NOT NULL DEFAULT 0,
            last_indexed    TEXT    NOT NULL DEFAULT '',
            parse_errors_json TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS diagnostics (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            uri          TEXT    NOT NULL,
            code         TEXT    NOT NULL DEFAULT '',
            message      TEXT    NOT NULL DEFAULT '',
            range_json   TEXT    NOT NULL DEFAULT '{}',
            severity     INTEGER NOT NULL DEFAULT 1,
            tags_json    TEXT    NOT NULL DEFAULT '[]',
            related_json TEXT    NOT NULL DEFAULT '[]'
        );

        CREATE INDEX IF NOT EXISTS idx_diag_uri ON diagnostics(uri);

        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', '1');
    """)


_MIGRATIONS: dict[int, Any] = {
    1: _migrate_v1,
}


def get_schema_version(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute("SELECT value FROM meta WHERE key = ?", (SCHEMA_VERSION_KEY,)).fetchone()
        if row is not None:
            return int(row[0])
    except sqlite3.OperationalError:
        pass
    return 0


def set_schema_version(conn: sqlite3.Connection, version: int) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
        (SCHEMA_VERSION_KEY, str(version)),
    )


def auto_migrate(conn: sqlite3.Connection) -> bool:
    current = get_schema_version(conn)
    if current > CURRENT_SCHEMA_VERSION:
        logger.error(
            "Database schema version %d is newer than supported %d. Downgrade not supported.",
            current, CURRENT_SCHEMA_VERSION,
        )
        return False

    if current == CURRENT_SCHEMA_VERSION:
        return True

    for version in range(current + 1, CURRENT_SCHEMA_VERSION + 1):
        migrator = _MIGRATIONS.get(version)
        if migrator is None:
            logger.error("No migration found for schema version %d.", version)
            return False
        try:
            migrator(conn)
            set_schema_version(conn, version)
            conn.commit()
            logger.info("Migration to schema version %d completed.", version)
        except Exception:
            logger.exception("Migration to schema version %d failed. Rolling back.", version)
            conn.rollback()
            return False

    return True


def validate_schema(conn: sqlite3.Connection) -> bool:
    required_tables = {
        "symbols", "references_", "dependencies",
        "documents", "diagnostics", "meta",
    }
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing = {row[0] for row in cursor.fetchall()}
    missing = required_tables - existing
    if missing:
        logger.warning("Missing tables: %s. Running migration.", missing)
        return auto_migrate(conn)
    return get_schema_version(conn) == CURRENT_SCHEMA_VERSION


def ensure_schema(conn: sqlite3.Connection) -> bool:
    if not validate_schema(conn):
        logger.info("Schema validation failed. Attempting auto-migration.")
        return auto_migrate(conn)
    return True
