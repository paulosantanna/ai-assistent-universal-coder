"""Conservative, transactional token accounting for Workspace OS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .store import (
    MAX_SQLITE_INTEGER,
    WorkspaceStore,
    WorkspaceStoreError,
    validate_identifier,
)


class MeasurementKind(StrEnum):
    ACTUAL = "ACTUAL"
    ESTIMATED = "ESTIMATED"
    UNMETERED = "UNMETERED"


_TASK_CHARGE_SQL = {
    MeasurementKind.ACTUAL: """
        UPDATE task_budgets
        SET charged_tokens = charged_tokens + ?,
            actual_tokens = actual_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ?
    """,
    MeasurementKind.ESTIMATED: """
        UPDATE task_budgets
        SET charged_tokens = charged_tokens + ?,
            estimated_tokens = estimated_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ?
    """,
    MeasurementKind.UNMETERED: """
        UPDATE task_budgets
        SET charged_tokens = charged_tokens + ?,
            unmetered_tokens = unmetered_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ?
    """,
}

_ATTEMPT_CHARGE_SQL = {
    MeasurementKind.ACTUAL: """
        UPDATE attempt_budgets
        SET charged_tokens = charged_tokens + ?,
            actual_tokens = actual_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
    """,
    MeasurementKind.ESTIMATED: """
        UPDATE attempt_budgets
        SET charged_tokens = charged_tokens + ?,
            estimated_tokens = estimated_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
    """,
    MeasurementKind.UNMETERED: """
        UPDATE attempt_budgets
        SET charged_tokens = charged_tokens + ?,
            unmetered_tokens = unmetered_tokens + ?, revision = revision + 1
        WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
    """,
}

_EXECUTION_CHARGE_SQL = {
    MeasurementKind.ACTUAL: """
        UPDATE executions
        SET charged_tokens = charged_tokens + ?,
            actual_tokens = actual_tokens + ?, revision = revision + 1
        WHERE execution_id = ?
    """,
    MeasurementKind.ESTIMATED: """
        UPDATE executions
        SET charged_tokens = charged_tokens + ?,
            estimated_tokens = estimated_tokens + ?, revision = revision + 1
        WHERE execution_id = ?
    """,
    MeasurementKind.UNMETERED: """
        UPDATE executions
        SET charged_tokens = charged_tokens + ?,
            unmetered_tokens = unmetered_tokens + ?, revision = revision + 1
        WHERE execution_id = ?
    """,
}

_AGGREGATE_EXECUTION_SQL = """
    SELECT COALESCE(SUM(charged_tokens), 0) charged_tokens,
        COALESCE(SUM(CASE WHEN measurement_kind = 'ACTUAL'
            THEN charged_tokens ELSE 0 END), 0) actual_tokens,
        COALESCE(SUM(CASE WHEN measurement_kind = 'ESTIMATED'
            THEN charged_tokens ELSE 0 END), 0) estimated_tokens,
        COALESCE(SUM(CASE WHEN measurement_kind = 'UNMETERED'
            THEN charged_tokens ELSE 0 END), 0) unmetered_tokens
    FROM token_calls WHERE execution_id = ?
"""
_AGGREGATE_TASK_SQL = _AGGREGATE_EXECUTION_SQL + " AND task_id = ?"
_AGGREGATE_ATTEMPT_SQL = _AGGREGATE_TASK_SQL + " AND attempt_id = ?"


class TokenLedgerError(WorkspaceStoreError):
    """Base error for invalid or conflicting token operations."""


class BudgetExceededError(TokenLedgerError):
    """Raised before a reservation could exceed a hard limit."""


class ReservationConflictError(TokenLedgerError):
    """Raised when an idempotency key is reused with different input."""


class UnknownReservationError(TokenLedgerError):
    """Raised when usage is reported without a reservation."""


@dataclass(frozen=True)
class TokenReservation:
    execution_id: str
    task_id: str
    attempt_id: str
    call_id: str
    reserved_tokens: int
    charged_tokens: int
    measurement_kind: MeasurementKind | None
    state: str
    revision: int


class TokenLedger:
    """Reserve before a call and reconcile afterwards.

    The ledger never treats estimates or unmetered usage as actual metering.
    """

    def __init__(self, store: WorkspaceStore):
        self.store = store

    def create_execution(self, execution_id: str, hard_limit: int) -> dict[str, Any]:
        validate_identifier(execution_id, "execution_id")
        self._non_negative(hard_limit, "hard_limit")
        with self.store.transaction() as connection:
            existing = connection.execute(
                "SELECT * FROM executions WHERE execution_id = ?",
                (execution_id,),
            ).fetchone()
            if existing is not None:
                if int(existing["hard_token_limit"]) != hard_limit:
                    raise ReservationConflictError("execution budget already exists")
                return dict(existing)
            connection.execute(
                "INSERT INTO executions(execution_id, hard_token_limit) VALUES (?, ?)",
                (execution_id, hard_limit),
            )
            self.store.append_event(
                connection,
                execution_id=execution_id,
                event_type="EXECUTION_BUDGET_CREATED",
                payload={"hard_token_limit": hard_limit},
            )
            return dict(
                connection.execute(
                    "SELECT * FROM executions WHERE execution_id = ?",
                    (execution_id,),
                ).fetchone()
            )

    def create_task_budget(
        self,
        execution_id: str,
        task_id: str,
        hard_limit: int,
    ) -> dict[str, Any]:
        validate_identifier(execution_id, "execution_id")
        validate_identifier(task_id, "task_id")
        self._non_negative(hard_limit, "hard_limit")
        with self.store.transaction() as connection:
            execution = connection.execute(
                "SELECT hard_token_limit FROM executions WHERE execution_id = ?",
                (execution_id,),
            ).fetchone()
            if execution is None:
                raise TokenLedgerError("unknown execution")
            if hard_limit > int(execution["hard_token_limit"]):
                raise BudgetExceededError("task limit exceeds execution limit")
            existing = connection.execute(
                "SELECT * FROM task_budgets WHERE execution_id = ? AND task_id = ?",
                (execution_id, task_id),
            ).fetchone()
            if existing is not None:
                if int(existing["hard_token_limit"]) != hard_limit:
                    raise ReservationConflictError("task budget already exists")
                return dict(existing)
            connection.execute(
                """
                INSERT INTO task_budgets(execution_id, task_id, hard_token_limit)
                VALUES (?, ?, ?)
                """,
                (execution_id, task_id, hard_limit),
            )
            self.store.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                event_type="TASK_BUDGET_CREATED",
                payload={"hard_token_limit": hard_limit},
            )
            return dict(
                connection.execute(
                    "SELECT * FROM task_budgets WHERE execution_id = ? AND task_id = ?",
                    (execution_id, task_id),
                ).fetchone()
            )

    def create_attempt_budget(
        self,
        execution_id: str,
        task_id: str,
        attempt_id: str,
        hard_limit: int,
    ) -> dict[str, Any]:
        for field, value in (
            ("execution_id", execution_id),
            ("task_id", task_id),
            ("attempt_id", attempt_id),
        ):
            validate_identifier(value, field)
        self._non_negative(hard_limit, "hard_limit")
        with self.store.transaction() as connection:
            task = connection.execute(
                """
                SELECT hard_token_limit FROM task_budgets
                WHERE execution_id = ? AND task_id = ?
                """,
                (execution_id, task_id),
            ).fetchone()
            if task is None:
                raise TokenLedgerError("unknown task budget")
            if hard_limit > int(task["hard_token_limit"]):
                raise BudgetExceededError("attempt limit exceeds task limit")
            existing = connection.execute(
                """
                SELECT * FROM attempt_budgets
                WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
                """,
                (execution_id, task_id, attempt_id),
            ).fetchone()
            if existing is not None:
                if int(existing["hard_token_limit"]) != hard_limit:
                    raise ReservationConflictError("attempt budget already exists")
                return dict(existing)
            connection.execute(
                """
                INSERT INTO attempt_budgets(
                    execution_id, task_id, attempt_id, hard_token_limit
                ) VALUES (?, ?, ?, ?)
                """,
                (execution_id, task_id, attempt_id, hard_limit),
            )
            self.store.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                attempt_id=attempt_id,
                event_type="ATTEMPT_BUDGET_CREATED",
                payload={"hard_token_limit": hard_limit},
            )
            return dict(
                connection.execute(
                    """
                    SELECT * FROM attempt_budgets
                    WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
                    """,
                    (execution_id, task_id, attempt_id),
                ).fetchone()
            )

    def reserve(
        self,
        execution_id: str,
        task_id: str,
        attempt_id: str,
        call_id: str,
        tokens: int,
    ) -> TokenReservation:
        for field, value in (
            ("execution_id", execution_id),
            ("task_id", task_id),
            ("attempt_id", attempt_id),
            ("call_id", call_id),
        ):
            validate_identifier(value, field)
        self._non_negative(tokens, "tokens")

        with self.store.transaction() as connection:
            existing = connection.execute(
                """
                SELECT * FROM token_calls
                WHERE execution_id = ? AND task_id = ? AND attempt_id = ? AND call_id = ?
                """,
                (execution_id, task_id, attempt_id, call_id),
            ).fetchone()
            if existing is not None:
                if int(existing["reserved_tokens"]) != tokens:
                    raise ReservationConflictError("call_id reused with different reservation")
                return self._reservation(existing)

            execution = connection.execute(
                "SELECT * FROM executions WHERE execution_id = ?",
                (execution_id,),
            ).fetchone()
            task = connection.execute(
                "SELECT * FROM task_budgets WHERE execution_id = ? AND task_id = ?",
                (execution_id, task_id),
            ).fetchone()
            attempt = connection.execute(
                """
                SELECT * FROM attempt_budgets
                WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
                """,
                (execution_id, task_id, attempt_id),
            ).fetchone()
            if execution is None or task is None or attempt is None:
                raise TokenLedgerError(
                    "execution, task and attempt budgets must exist"
                )

            execution_active = self._active_reservations(
                connection, execution_id=execution_id
            )
            task_active = self._active_reservations(
                connection, execution_id=execution_id, task_id=task_id
            )
            attempt_active = self._active_reservations(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                attempt_id=attempt_id,
            )
            if int(execution["charged_tokens"]) + execution_active + tokens > int(
                execution["hard_token_limit"]
            ):
                raise BudgetExceededError("execution token budget exceeded")
            if int(task["charged_tokens"]) + task_active + tokens > int(
                task["hard_token_limit"]
            ):
                raise BudgetExceededError("task token budget exceeded")
            if int(attempt["charged_tokens"]) + attempt_active + tokens > int(
                attempt["hard_token_limit"]
            ):
                raise BudgetExceededError("attempt token budget exceeded")

            connection.execute(
                """
                INSERT INTO token_calls(
                    execution_id, task_id, attempt_id, call_id,
                    reserved_tokens, state
                ) VALUES (?, ?, ?, ?, ?, 'RESERVED')
                """,
                (execution_id, task_id, attempt_id, call_id, tokens),
            )
            self.store.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                attempt_id=attempt_id,
                call_id=call_id,
                event_type="TOKEN_RESERVED",
                payload={"reserved_tokens": tokens, "revision": 0},
            )
            return self._get_call(connection, execution_id, task_id, attempt_id, call_id)

    def reconcile(
        self,
        execution_id: str,
        task_id: str,
        attempt_id: str,
        call_id: str,
        used_tokens: int | None,
        measurement_kind: MeasurementKind,
    ) -> TokenReservation:
        with self.store.transaction() as connection:
            current = self._get_call(
                connection, execution_id, task_id, attempt_id, call_id
            )
            charge = (
                current.reserved_tokens
                if measurement_kind is MeasurementKind.UNMETERED
                else used_tokens
            )
            if charge is None:
                raise TokenLedgerError("metered usage requires used_tokens")
            self._non_negative(charge, "used_tokens")
            if charge > current.reserved_tokens:
                raise BudgetExceededError("reported usage exceeds reservation")
            if current.state == "CHARGED":
                if (
                    current.charged_tokens == charge
                    and current.measurement_kind is measurement_kind
                ):
                    return current
                raise ReservationConflictError("reservation already reconciled")
            if current.state != "RESERVED":
                raise ReservationConflictError("released reservation cannot be reconciled")

            cursor = connection.execute(
                """
                UPDATE token_calls
                SET charged_tokens = ?, measurement_kind = ?, state = 'CHARGED',
                    revision = revision + 1
                WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
                    AND call_id = ? AND state = 'RESERVED' AND revision = ?
                """,
                (
                    charge,
                    measurement_kind.value,
                    execution_id,
                    task_id,
                    attempt_id,
                    call_id,
                    current.revision,
                ),
            )
            if cursor.rowcount != 1:
                raise ReservationConflictError("reservation changed concurrently")
            connection.execute(
                _ATTEMPT_CHARGE_SQL[measurement_kind],
                (charge, charge, execution_id, task_id, attempt_id),
            )
            connection.execute(
                _TASK_CHARGE_SQL[measurement_kind],
                (charge, charge, execution_id, task_id),
            )
            connection.execute(
                _EXECUTION_CHARGE_SQL[measurement_kind],
                (charge, charge, execution_id),
            )
            self.store.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                attempt_id=attempt_id,
                call_id=call_id,
                event_type="TOKEN_RECONCILED",
                payload={
                    "charged_tokens": charge,
                    "measurement_kind": measurement_kind.value,
                    "revision": current.revision + 1,
                },
            )
            return self._get_call(
                connection, execution_id, task_id, attempt_id, call_id
            )

    def release(
        self,
        execution_id: str,
        task_id: str,
        attempt_id: str,
        call_id: str,
    ) -> TokenReservation:
        with self.store.transaction() as connection:
            current = self._get_call(
                connection, execution_id, task_id, attempt_id, call_id
            )
            if current.state == "RELEASED":
                return current
            if current.state != "RESERVED":
                raise ReservationConflictError("charged reservation cannot be released")
            cursor = connection.execute(
                """
                UPDATE token_calls
                SET state = 'RELEASED', revision = revision + 1
                WHERE execution_id = ? AND task_id = ? AND attempt_id = ?
                    AND call_id = ? AND state = 'RESERVED' AND revision = ?
                """,
                (
                    execution_id,
                    task_id,
                    attempt_id,
                    call_id,
                    current.revision,
                ),
            )
            if cursor.rowcount != 1:
                raise ReservationConflictError("reservation changed concurrently")
            self.store.append_event(
                connection,
                execution_id=execution_id,
                task_id=task_id,
                attempt_id=attempt_id,
                call_id=call_id,
                event_type="TOKEN_RELEASED",
                payload={"revision": current.revision + 1},
            )
            return self._get_call(
                connection, execution_id, task_id, attempt_id, call_id
            )

    def summary(
        self,
        execution_id: str,
        connection: Any | None = None,
    ) -> dict[str, Any]:
        validate_identifier(execution_id, "execution_id")
        with self.store._reader(connection) as reader:
            self.store.verify_events(execution_id, reader)
            execution = reader.execute(
                "SELECT * FROM executions WHERE execution_id = ?",
                (execution_id,),
            ).fetchone()
            if execution is None:
                raise TokenLedgerError("unknown execution")
            active = self._active_reservations(reader, execution_id=execution_id)
            tasks = [
                dict(row)
                for row in reader.execute(
                    """
                    SELECT * FROM task_budgets
                    WHERE execution_id = ? ORDER BY task_id
                    """,
                    (execution_id,),
                ).fetchall()
            ]
            attempts = [
                dict(row)
                for row in reader.execute(
                    """
                    SELECT * FROM attempt_budgets
                    WHERE execution_id = ? ORDER BY task_id, attempt_id
                    """,
                    (execution_id,),
                ).fetchall()
            ]
            self._verify_conservation(reader, execution_id)
            self._verify_token_replay(reader, execution_id)
            result = dict(execution)
            result.update(
                {
                    "active_reservations": active,
                    "remaining_unreserved": int(execution["hard_token_limit"])
                    - int(execution["charged_tokens"])
                    - active,
                    "metering_quality": (
                        "UNMETERED"
                        if int(execution["unmetered_tokens"]) > 0
                        else "ESTIMATED"
                        if int(execution["estimated_tokens"]) > 0
                        else "ACTUAL"
                    ),
                    # Nenhum adapter de modelo é integrado neste slice; portanto
                    # a reserva é aplicada, mas um hard cap do provider não é alegado.
                    "reservation_cap_enforced": True,
                    "hard_cap_verifiable": False,
                    "tasks": tasks,
                    "attempts": attempts,
                }
            )
            return result

    @staticmethod
    def _active_reservations(
        connection: Any,
        *,
        execution_id: str,
        task_id: str | None = None,
        attempt_id: str | None = None,
    ) -> int:
        query = (
            "SELECT COALESCE(SUM(reserved_tokens), 0) AS total "
            "FROM token_calls WHERE execution_id = ? AND state = 'RESERVED'"
        )
        params: tuple[str, ...] = (execution_id,)
        if task_id is not None:
            query += " AND task_id = ?"
            params = (execution_id, task_id)
        if attempt_id is not None:
            if task_id is None:
                raise TokenLedgerError("attempt filter requires task_id")
            query += " AND attempt_id = ?"
            params = (execution_id, task_id, attempt_id)
        return int(connection.execute(query, params).fetchone()["total"])

    @staticmethod
    def _verify_conservation(connection: Any, execution_id: str) -> None:
        def assert_equal(materialized: Any, aggregate: Any, scope: str) -> None:
            for field in (
                "charged_tokens",
                "actual_tokens",
                "estimated_tokens",
                "unmetered_tokens",
            ):
                if int(materialized[field]) != int(aggregate[field]):
                    raise TokenLedgerError(f"token conservation mismatch: {scope}")

        execution = connection.execute(
            "SELECT * FROM executions WHERE execution_id = ?", (execution_id,)
        ).fetchone()
        aggregate = connection.execute(
            _AGGREGATE_EXECUTION_SQL,
            (execution_id,),
        ).fetchone()
        assert_equal(execution, aggregate, "execution")

        tasks = connection.execute(
            "SELECT * FROM task_budgets WHERE execution_id = ?", (execution_id,)
        ).fetchall()
        for task in tasks:
            aggregate = connection.execute(
                _AGGREGATE_TASK_SQL,
                (execution_id, task["task_id"]),
            ).fetchone()
            assert_equal(task, aggregate, f"task:{task['task_id']}")

        attempts = connection.execute(
            "SELECT * FROM attempt_budgets WHERE execution_id = ?", (execution_id,)
        ).fetchall()
        for attempt in attempts:
            aggregate = connection.execute(
                _AGGREGATE_ATTEMPT_SQL,
                (execution_id, attempt["task_id"], attempt["attempt_id"]),
            ).fetchone()
            assert_equal(
                attempt,
                aggregate,
                f"attempt:{attempt['task_id']}:{attempt['attempt_id']}",
            )

    @staticmethod
    def _verify_token_replay(connection: Any, execution_id: str) -> None:
        events = connection.execute(
            """
            SELECT task_id, attempt_id, call_id, event_type, payload_json
            FROM workspace_events
            WHERE execution_id = ? AND event_type IN (
                'TOKEN_RESERVED', 'TOKEN_RECONCILED', 'TOKEN_RELEASED'
            ) ORDER BY sequence
            """,
            (execution_id,),
        ).fetchall()
        replay: dict[tuple[str, str, str], tuple[str, int, int, str | None, int]] = {}
        import json

        for event in events:
            key = (
                str(event["task_id"]),
                str(event["attempt_id"]),
                str(event["call_id"]),
            )
            payload = json.loads(str(event["payload_json"]))
            if event["event_type"] == "TOKEN_RESERVED":
                replay[key] = ("RESERVED", int(payload["reserved_tokens"]), 0, None, 0)
            elif event["event_type"] == "TOKEN_RECONCILED" and key in replay:
                replay[key] = (
                    "CHARGED",
                    replay[key][1],
                    int(payload["charged_tokens"]),
                    str(payload["measurement_kind"]),
                    int(payload["revision"]),
                )
            elif event["event_type"] == "TOKEN_RELEASED" and key in replay:
                replay[key] = (
                    "RELEASED",
                    replay[key][1],
                    0,
                    None,
                    int(payload["revision"]),
                )
            else:
                raise TokenLedgerError("invalid token event sequence")
        calls = connection.execute(
            "SELECT * FROM token_calls WHERE execution_id = ?",
            (execution_id,),
        ).fetchall()
        if len(calls) != len(replay):
            raise TokenLedgerError("token replay call count mismatch")
        for call in calls:
            key = (
                str(call["task_id"]),
                str(call["attempt_id"]),
                str(call["call_id"]),
            )
            expected = (
                str(call["state"]),
                int(call["reserved_tokens"]),
                int(call["charged_tokens"]),
                call["measurement_kind"],
                int(call["revision"]),
            )
            if replay.get(key) != expected:
                raise TokenLedgerError("token replay state mismatch")

    def _get_call(
        self,
        connection: Any,
        execution_id: str,
        task_id: str,
        attempt_id: str,
        call_id: str,
    ) -> TokenReservation:
        for field, value in (
            ("execution_id", execution_id),
            ("task_id", task_id),
            ("attempt_id", attempt_id),
            ("call_id", call_id),
        ):
            validate_identifier(value, field)
        row = connection.execute(
            """
            SELECT * FROM token_calls
            WHERE execution_id = ? AND task_id = ? AND attempt_id = ? AND call_id = ?
            """,
            (execution_id, task_id, attempt_id, call_id),
        ).fetchone()
        if row is None:
            raise UnknownReservationError("unknown token reservation")
        return self._reservation(row)

    @staticmethod
    def _reservation(row: Any) -> TokenReservation:
        kind = (
            MeasurementKind(str(row["measurement_kind"]))
            if row["measurement_kind"] is not None
            else None
        )
        return TokenReservation(
            execution_id=str(row["execution_id"]),
            task_id=str(row["task_id"]),
            attempt_id=str(row["attempt_id"]),
            call_id=str(row["call_id"]),
            reserved_tokens=int(row["reserved_tokens"]),
            charged_tokens=int(row["charged_tokens"]),
            measurement_kind=kind,
            state=str(row["state"]),
            revision=int(row["revision"]),
        )

    @staticmethod
    def _non_negative(value: int, field: str) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            or value > MAX_SQLITE_INTEGER
        ):
            raise TokenLedgerError(
                f"{field} must be between 0 and {MAX_SQLITE_INTEGER}"
            )
