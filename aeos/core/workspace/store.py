"""Transactional storage for the isolated AEOS Workspace OS slice."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import Any, Iterator, Literal

from .redaction import assert_safe_payload, assert_safe_text
from .exceptions import WorkspaceError, RevisionConflictError


SCHEMA_VERSION = 1
MAX_SQLITE_INTEGER = (1 << 63) - 1
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class WorkspaceStoreError(WorkspaceError):
    """Base error for workspace persistence."""


class InvalidIdentifierError(WorkspaceStoreError):
    """Raised when an identifier could influence storage unsafely."""


class SchemaMismatchError(WorkspaceStoreError):
    """Raised when the database schema is unknown or damaged."""


class _ClosingConnection(sqlite3.Connection):
    """Commit/rollback e feche ao sair de ``with``."""

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        try:
            super().__exit__(exc_type, exc, traceback)
            return False
        finally:
            self.close()


def validate_identifier(value: object, field: str = "identifier") -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise InvalidIdentifierError(f"invalid {field}")
    return value


class WorkspaceStore:
    """Own one SQLite database below ``.aeos/workspace``.

    The store is intentionally separate from all legacy AEOS state.
    """

    def __init__(
        self,
        workspace_root: str | Path,
        *,
        create: bool = True,
        read_only: bool = False,
    ):
        root = Path(workspace_root).resolve()
        if not root.exists() or not root.is_dir():
            raise WorkspaceStoreError("workspace root must be an existing directory")
        if create and read_only:
            raise WorkspaceStoreError("read-only store cannot create state")
        self.workspace_root = root
        self.read_only = read_only
        state_dir = (root / ".aeos" / "workspace").resolve()
        if root != state_dir and root not in state_dir.parents:
            raise WorkspaceStoreError("workspace state escaped workspace root")
        self.database_path = state_dir / "workspace-v1.sqlite3"
        if create:
            state_dir.mkdir(parents=True, exist_ok=True)
            self._initialize()
        elif not self.database_path.is_file():
            raise WorkspaceStoreError("workspace state does not exist")
        else:
            self.health()

    def connect(self) -> sqlite3.Connection:
        if self.read_only:
            uri = f"{self.database_path.resolve().as_uri()}?mode=ro&immutable=0"
            connection = sqlite3.connect(
                uri,
                uri=True,
                timeout=30.0,
                isolation_level=None,
                factory=_ClosingConnection,
            )
        else:
            connection = sqlite3.connect(
                self.database_path,
                timeout=30.0,
                isolation_level=None,
                factory=_ClosingConnection,
            )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        if self.read_only:
            raise WorkspaceStoreError("read-only store cannot start a transaction")
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def read_transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            connection.execute("BEGIN")
            yield connection
            connection.rollback()
        finally:
            connection.close()

    @contextmanager
    def _reader(
        self, connection: sqlite3.Connection | None
    ) -> Iterator[sqlite3.Connection]:
        if connection is not None:
            yield connection
            return
        with self.connect() as owned:
            yield owned

    def health(
        self, connection: sqlite3.Connection | None = None
    ) -> dict[str, object]:
        with self._reader(connection) as reader:
            integrity = str(reader.execute("PRAGMA quick_check").fetchone()[0])
            version_row = reader.execute(
                "SELECT value FROM workspace_metadata WHERE key = 'schema_version'"
            ).fetchone()
            if version_row is None or int(version_row["value"]) != SCHEMA_VERSION:
                raise SchemaMismatchError("workspace schema version mismatch")
            if integrity != "ok":
                raise SchemaMismatchError(f"workspace database integrity: {integrity}")
            return {
                "schema_version": SCHEMA_VERSION,
                "integrity": integrity,
                "database": str(self.database_path),
            }

    @staticmethod
    def canonical_payload(payload: dict[str, Any]) -> tuple[str, str]:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return encoded, hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def load_task_snapshots(
        self,
        execution_id: str,
        connection: sqlite3.Connection | None = None,
    ) -> list[dict[str, Any]]:
        validate_identifier(execution_id, "execution_id")
        with self._reader(connection) as reader:
            rows = reader.execute(
                """
                SELECT task_id, payload_json, payload_sha256, revision
                FROM task_snapshots
                WHERE execution_id = ?
                ORDER BY task_id
                """,
                (execution_id,),
            ).fetchall()
        snapshots: list[dict[str, Any]] = []
        for row in rows:
            digest = hashlib.sha256(
                str(row["payload_json"]).encode("utf-8")
            ).hexdigest()
            if digest != str(row["payload_sha256"]):
                raise SchemaMismatchError(
                    f"task snapshot integrity mismatch: {row['task_id']}"
                )
            payload = json.loads(str(row["payload_json"]))
            if (
                payload.get("task_id") != row["task_id"]
                or payload.get("revision") != row["revision"]
            ):
                raise SchemaMismatchError(
                    f"task snapshot metadata mismatch: {row['task_id']}"
                )
            snapshots.append(payload)
        return snapshots

    def verify_events(
        self,
        execution_id: str,
        connection: sqlite3.Connection | None = None,
    ) -> int:
        validate_identifier(execution_id, "execution_id")
        with self._reader(connection) as reader:
            execution = reader.execute(
                "SELECT event_count, event_head_sha256 FROM executions WHERE execution_id = ?",
                (execution_id,),
            ).fetchone()
            if execution is None:
                raise WorkspaceStoreError("unknown execution")
            rows = reader.execute(
                """
                SELECT event_id, sequence, task_id, attempt_id, call_id,
                    event_type, payload_json, payload_sha256,
                    previous_event_sha256, event_sha256
                FROM workspace_events
                WHERE execution_id = ?
                ORDER BY sequence
                """,
                (execution_id,),
            ).fetchall()
        previous = ""
        for expected_sequence, row in enumerate(rows, start=1):
            payload_hash = hashlib.sha256(
                str(row["payload_json"]).encode("utf-8")
            ).hexdigest()
            envelope, event_hash = self.canonical_payload(
                {
                    "execution_id": execution_id,
                    "sequence": int(row["sequence"]),
                    "task_id": row["task_id"],
                    "attempt_id": row["attempt_id"],
                    "call_id": row["call_id"],
                    "event_type": str(row["event_type"]),
                    "payload_sha256": payload_hash,
                    "previous_event_sha256": previous,
                }
            )
            del envelope
            if (
                int(row["sequence"]) != expected_sequence
                or payload_hash != str(row["payload_sha256"])
                or str(row["previous_event_sha256"]) != previous
                or str(row["event_sha256"]) != event_hash
            ):
                raise SchemaMismatchError(
                    f"workspace event integrity mismatch: {row['event_id']}"
                )
            previous = event_hash
        if (
            len(rows) != int(execution["event_count"])
            or previous != str(execution["event_head_sha256"])
        ):
            raise SchemaMismatchError("workspace event head mismatch")
        return len(rows)

    def load_verified_events(
        self,
        execution_id: str,
        connection: sqlite3.Connection | None = None,
    ) -> list[dict[str, Any]]:
        with self._reader(connection) as reader:
            self.verify_events(execution_id, reader)
            rows = reader.execute(
                """
                SELECT sequence, task_id, attempt_id, call_id,
                    event_type, payload_json
                FROM workspace_events
                WHERE execution_id = ? ORDER BY sequence
                """,
                (execution_id,),
            ).fetchall()
        return [
            {
                "sequence": int(row["sequence"]),
                "task_id": row["task_id"],
                "attempt_id": row["attempt_id"],
                "call_id": row["call_id"],
                "event_type": str(row["event_type"]),
                "payload": json.loads(str(row["payload_json"])),
            }
            for row in rows
        ]

    def append_event(
        self,
        connection: sqlite3.Connection,
        *,
        execution_id: str,
        event_type: str,
        payload: dict[str, Any],
        task_id: str | None = None,
        attempt_id: str | None = None,
        call_id: str | None = None,
    ) -> str:
        assert_safe_payload(payload, "event")
        validate_identifier(execution_id, "execution_id")
        validate_identifier(event_type, "event_type")
        for field, value in (
            ("task_id", task_id),
            ("attempt_id", attempt_id),
            ("call_id", call_id),
        ):
            if value is not None:
                validate_identifier(value, field)
        execution = connection.execute(
            "SELECT event_count, event_head_sha256 FROM executions WHERE execution_id = ?",
            (execution_id,),
        ).fetchone()
        if execution is None:
            raise WorkspaceStoreError("unknown execution")
        sequence = int(execution["event_count"]) + 1
        previous = str(execution["event_head_sha256"])
        payload_json, payload_hash = self.canonical_payload(payload)
        _, event_hash = self.canonical_payload(
            {
                "execution_id": execution_id,
                "sequence": sequence,
                "task_id": task_id,
                "attempt_id": attempt_id,
                "call_id": call_id,
                "event_type": event_type,
                "payload_sha256": payload_hash,
                "previous_event_sha256": previous,
            }
        )
        connection.execute(
            """
            INSERT INTO workspace_events(
                execution_id, sequence, task_id, attempt_id, call_id,
                event_type, payload_json, payload_sha256,
                previous_event_sha256, event_sha256
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                execution_id,
                sequence,
                task_id,
                attempt_id,
                call_id,
                event_type,
                payload_json,
                payload_hash,
                previous,
                event_hash,
            ),
        )
        cursor = connection.execute(
            """
            UPDATE executions
            SET event_count = ?, event_head_sha256 = ?
            WHERE execution_id = ? AND event_count = ? AND event_head_sha256 = ?
            """,
            (sequence, event_hash, execution_id, sequence - 1, previous),
        )
        if cursor.rowcount != 1:
            raise RevisionConflictError("workspace event head changed concurrently")
        return event_hash

    @staticmethod
    def _file_sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    def register_evidence(
        self,
        execution_id: str,
        task_id: str,
        *,
        task_revision: int,
        evidence_id: str,
        evidence_type: str,
        artifact_path: str | Path,
        verifier_id: str,
        provenance: str,
    ) -> str:
        assert_safe_text(provenance, "evidence provenance")
        for field, value in (
            ("execution_id", execution_id),
            ("task_id", task_id),
            ("evidence_id", evidence_id),
            ("evidence_type", evidence_type),
            ("verifier_id", verifier_id),
        ):
            validate_identifier(value, field)
        artifact = Path(artifact_path)
        if not artifact.is_absolute():
            artifact = self.workspace_root / artifact
        artifact = artifact.resolve()
        if self.workspace_root != artifact and self.workspace_root not in artifact.parents:
            raise WorkspaceStoreError("evidence artifact escaped workspace root")
        if not artifact.is_file():
            raise WorkspaceStoreError("evidence artifact does not exist")
        relative = artifact.relative_to(self.workspace_root).as_posix()
        artifact_hash = self._file_sha256(artifact)
        with self.transaction() as connection:
            snapshot = connection.execute(
                """
                SELECT revision FROM task_snapshots
                WHERE execution_id = ? AND task_id = ?
                """,
                (execution_id, task_id),
            ).fetchone()
            if snapshot is None or int(snapshot["revision"]) != task_revision:
                raise RevisionConflictError("evidence task revision is stale")
            existing = connection.execute(
                """
                SELECT * FROM evidence_records
                WHERE execution_id = ? AND task_id = ?
                    AND task_revision = ? AND evidence_id = ?
                """,
                (execution_id, task_id, task_revision, evidence_id),
            ).fetchone()
            if existing is not None:
                if (
                    str(existing["artifact_path"]) == relative
                    and str(existing["artifact_sha256"]) == artifact_hash
                    and str(existing["evidence_type"]) == evidence_type
                    and str(existing["verifier_id"]) == verifier_id
                    and str(existing["provenance"]) == provenance
                ):
                    return evidence_id
                raise WorkspaceStoreError("evidence_id already exists with other content")
            connection.execute(
                """
                INSERT INTO evidence_records(
                    execution_id, task_id, task_revision, evidence_id,
                    evidence_type, artifact_path, artifact_sha256,
                    verifier_id, provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    execution_id,
                    task_id,
                    task_revision,
                    evidence_id,
                    evidence_type,
                    relative,
                    artifact_hash,
                    verifier_id,
                    provenance,
                ),
            )
            self.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                event_type="EVIDENCE_REGISTERED",
                payload={
                    "task_revision": task_revision,
                    "evidence_id": evidence_id,
                    "evidence_type": evidence_type,
                    "artifact_path": relative,
                    "artifact_sha256": artifact_hash,
                    "verifier_id": verifier_id,
                    "provenance": provenance,
                },
            )
        return evidence_id

    def evidence_candidates(
        self, execution_id: str, task_id: str, task_revision: int
    ) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT evidence_id, evidence_type, artifact_path,
                    artifact_sha256, verifier_id, provenance
                FROM evidence_records
                WHERE execution_id = ? AND task_id = ? AND task_revision = ?
                """,
                (execution_id, task_id, task_revision),
            ).fetchall()
        verified: list[dict[str, Any]] = []
        for row in rows:
            artifact = (self.workspace_root / str(row["artifact_path"])).resolve()
            if (
                artifact.is_file()
                and self.workspace_root in artifact.parents
                and self._file_sha256(artifact) == str(row["artifact_sha256"])
            ):
                verified.append(
                    {
                        "evidence_id": str(row["evidence_id"]),
                        "evidence_type": str(row["evidence_type"]),
                        "artifact_path": artifact,
                        "verifier_id": str(row["verifier_id"]),
                        "provenance": str(row["provenance"]),
                    }
                )
        return verified

    def compare_and_swap_task(
        self,
        execution_id: str,
        task_id: str,
        *,
        expected_revision: int,
        payload: dict[str, Any],
        event_type: str,
    ) -> None:
        assert_safe_payload(payload, "task snapshot")
        validate_identifier(execution_id, "execution_id")
        validate_identifier(task_id, "task_id")
        validate_identifier(event_type, "event_type")
        if payload.get("task_id") != task_id:
            raise WorkspaceStoreError("task payload identifier mismatch")
        if payload.get("revision") != expected_revision + 1:
            raise WorkspaceStoreError("task payload revision mismatch")
        payload_json, payload_sha256 = self.canonical_payload(payload)
        with self.transaction() as connection:
            cursor = connection.execute(
                """
                UPDATE task_snapshots
                SET payload_json = ?, payload_sha256 = ?, revision = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE execution_id = ? AND task_id = ? AND revision = ?
                """,
                (
                    payload_json,
                    payload_sha256,
                    expected_revision + 1,
                    execution_id,
                    task_id,
                    expected_revision,
                ),
            )
            if cursor.rowcount != 1:
                raise RevisionConflictError("task revision changed concurrently")
            self.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                event_type=event_type,
                payload={
                    "expected_revision": expected_revision,
                    "task": payload,
                },
            )

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = FULL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS workspace_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS executions (
                    execution_id TEXT PRIMARY KEY,
                    hard_token_limit INTEGER NOT NULL CHECK (hard_token_limit >= 0),
                    charged_tokens INTEGER NOT NULL DEFAULT 0 CHECK (charged_tokens >= 0),
                    actual_tokens INTEGER NOT NULL DEFAULT 0 CHECK (actual_tokens >= 0),
                    estimated_tokens INTEGER NOT NULL DEFAULT 0 CHECK (estimated_tokens >= 0),
                    unmetered_tokens INTEGER NOT NULL DEFAULT 0 CHECK (unmetered_tokens >= 0),
                    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
                    event_count INTEGER NOT NULL DEFAULT 0 CHECK (event_count >= 0),
                    event_head_sha256 TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS task_budgets (
                    execution_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    hard_token_limit INTEGER NOT NULL CHECK (hard_token_limit >= 0),
                    charged_tokens INTEGER NOT NULL DEFAULT 0 CHECK (charged_tokens >= 0),
                    actual_tokens INTEGER NOT NULL DEFAULT 0 CHECK (actual_tokens >= 0),
                    estimated_tokens INTEGER NOT NULL DEFAULT 0 CHECK (estimated_tokens >= 0),
                    unmetered_tokens INTEGER NOT NULL DEFAULT 0 CHECK (unmetered_tokens >= 0),
                    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
                    PRIMARY KEY (execution_id, task_id),
                    FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
                );

                CREATE TABLE IF NOT EXISTS token_calls (
                    execution_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    call_id TEXT NOT NULL,
                    reserved_tokens INTEGER NOT NULL CHECK (reserved_tokens >= 0),
                    charged_tokens INTEGER NOT NULL DEFAULT 0 CHECK (charged_tokens >= 0),
                    measurement_kind TEXT,
                    state TEXT NOT NULL CHECK (state IN ('RESERVED', 'CHARGED', 'RELEASED')),
                    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
                    PRIMARY KEY (execution_id, task_id, attempt_id, call_id),
                    FOREIGN KEY (execution_id, task_id, attempt_id)
                        REFERENCES attempt_budgets(execution_id, task_id, attempt_id)
                );

                CREATE TABLE IF NOT EXISTS attempt_budgets (
                    execution_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    hard_token_limit INTEGER NOT NULL CHECK (hard_token_limit >= 0),
                    charged_tokens INTEGER NOT NULL DEFAULT 0 CHECK (charged_tokens >= 0),
                    actual_tokens INTEGER NOT NULL DEFAULT 0 CHECK (actual_tokens >= 0),
                    estimated_tokens INTEGER NOT NULL DEFAULT 0 CHECK (estimated_tokens >= 0),
                    unmetered_tokens INTEGER NOT NULL DEFAULT 0 CHECK (unmetered_tokens >= 0),
                    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
                    PRIMARY KEY (execution_id, task_id, attempt_id),
                    FOREIGN KEY (execution_id, task_id)
                        REFERENCES task_budgets(execution_id, task_id)
                );

                CREATE TABLE IF NOT EXISTS task_snapshots (
                    execution_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (execution_id, task_id),
                    FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
                );

                CREATE TABLE IF NOT EXISTS workspace_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL CHECK (sequence > 0),
                    task_id TEXT,
                    attempt_id TEXT,
                    call_id TEXT,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    previous_event_sha256 TEXT NOT NULL,
                    event_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ,UNIQUE (execution_id, sequence)
                );

                CREATE TABLE IF NOT EXISTS evidence_records (
                    execution_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    task_revision INTEGER NOT NULL CHECK (task_revision >= 0),
                    evidence_id TEXT NOT NULL,
                    evidence_type TEXT NOT NULL,
                    artifact_path TEXT NOT NULL,
                    artifact_sha256 TEXT NOT NULL,
                    verifier_id TEXT NOT NULL,
                    provenance TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (execution_id, task_id, task_revision, evidence_id),
                    FOREIGN KEY (execution_id, task_id)
                        REFERENCES task_snapshots(execution_id, task_id)
                );
                """
            )
            row = connection.execute(
                "SELECT value FROM workspace_metadata WHERE key = 'schema_version'"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO workspace_metadata(key, value) VALUES ('schema_version', ?)",
                    (str(SCHEMA_VERSION),),
                )
            elif int(row[0]) != SCHEMA_VERSION:
                raise SchemaMismatchError("workspace schema version mismatch")
        self.health()
