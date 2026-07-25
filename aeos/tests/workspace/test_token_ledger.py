from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path

import pytest

from aeos.core.workspace.store import SchemaMismatchError, WorkspaceStore
from aeos.core.workspace.token_ledger import (
    BudgetExceededError,
    MeasurementKind,
    ReservationConflictError,
    TokenLedger,
    TokenLedgerError,
    UnknownReservationError,
)


def ledger(tmp_path: Path, limit: int = 100) -> TokenLedger:
    tmp_path.mkdir(parents=True, exist_ok=True)
    result = TokenLedger(WorkspaceStore(tmp_path))
    result.create_execution("run-1", limit)
    result.create_task_budget("run-1", "task-1", limit)
    result.create_attempt_budget("run-1", "task-1", "attempt-1", limit)
    return result


def test_reservation_reconcile_and_release_are_idempotent(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path)
    reserved = token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 40)
    assert reserved.state == "RESERVED"
    assert token_ledger.reserve(
        "run-1", "task-1", "attempt-1", "call-1", 40
    ) == reserved

    charged = token_ledger.reconcile(
        "run-1",
        "task-1",
        "attempt-1",
        "call-1",
        25,
        MeasurementKind.ACTUAL,
    )
    assert charged.state == "CHARGED"
    assert charged.charged_tokens == 25
    assert (
        token_ledger.reconcile(
            "run-1",
            "task-1",
            "attempt-1",
            "call-1",
            25,
            MeasurementKind.ACTUAL,
        )
        == charged
    )

    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-2", 30)
    released = token_ledger.release("run-1", "task-1", "attempt-1", "call-2")
    assert released.state == "RELEASED"
    assert token_ledger.release(
        "run-1", "task-1", "attempt-1", "call-2"
    ) == released


def test_reservation_blocks_before_budget_is_exceeded(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path, limit=10)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 8)
    with pytest.raises(BudgetExceededError):
        token_ledger.reserve("run-1", "task-1", "attempt-1", "call-2", 3)
    assert token_ledger.summary("run-1")["remaining_unreserved"] == 2


def test_actual_above_reservation_does_not_mutate(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 10)
    with pytest.raises(BudgetExceededError):
        token_ledger.reconcile(
            "run-1",
            "task-1",
            "attempt-1",
            "call-1",
            11,
            MeasurementKind.ACTUAL,
        )
    summary = token_ledger.summary("run-1")
    assert summary["charged_tokens"] == 0
    assert summary["active_reservations"] == 10


def test_unmetered_charges_full_reservation_and_is_explicit(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 40)
    charged = token_ledger.reconcile(
        "run-1",
        "task-1",
        "attempt-1",
        "call-1",
        None,
        MeasurementKind.UNMETERED,
    )
    assert charged.charged_tokens == 40
    summary = token_ledger.summary("run-1")
    assert summary["metering_quality"] == "UNMETERED"
    assert summary["hard_cap_verifiable"] is False


@pytest.mark.parametrize("value", [-1, True, 1.5])
def test_invalid_token_values_fail_closed(tmp_path: Path, value: object) -> None:
    token_ledger = ledger(tmp_path)
    with pytest.raises(TokenLedgerError):
        token_ledger.reserve(
            "run-1", "task-1", "attempt-1", "call-1", value  # type: ignore[arg-type]
        )


def test_conflicting_duplicate_and_unknown_usage_fail(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 10)
    with pytest.raises(ReservationConflictError):
        token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 9)
    with pytest.raises(UnknownReservationError):
        token_ledger.reconcile(
            "run-1",
            "task-1",
            "attempt-1",
            "missing",
            1,
            MeasurementKind.ACTUAL,
        )


def test_concurrent_reservations_cannot_overspend(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path, limit=10)

    def try_reserve(index: int) -> str:
        try:
            token_ledger.reserve(
                "run-1",
                "task-1",
                "attempt-1",
                f"call-{index}",
                6,
            )
            return "reserved"
        except BudgetExceededError:
            return "blocked"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(try_reserve, range(2)))

    assert sorted(results) == ["blocked", "reserved"]
    assert token_ledger.summary("run-1")["active_reservations"] == 6


def test_reopen_preserves_charges(tmp_path: Path) -> None:
    first = ledger(tmp_path)
    first.reserve("run-1", "task-1", "attempt-1", "call-1", 20)
    first.reconcile(
        "run-1",
        "task-1",
        "attempt-1",
        "call-1",
        12,
        MeasurementKind.ESTIMATED,
    )
    second = TokenLedger(WorkspaceStore(tmp_path))
    assert second.summary("run-1")["estimated_tokens"] == 12


def test_attempt_budget_is_enforced_and_reported(tmp_path: Path) -> None:
    token_ledger = TokenLedger(WorkspaceStore(tmp_path))
    token_ledger.create_execution("run-1", 20)
    token_ledger.create_task_budget("run-1", "task-1", 15)
    token_ledger.create_attempt_budget("run-1", "task-1", "attempt-1", 6)
    with pytest.raises(BudgetExceededError, match="attempt"):
        token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 7)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 6)
    token_ledger.reconcile(
        "run-1", "task-1", "attempt-1", "call-1", 5, MeasurementKind.ACTUAL
    )
    attempt = token_ledger.summary("run-1")["attempts"][0]
    assert attempt["charged_tokens"] == 5
    assert attempt["actual_tokens"] == 5


def test_token_events_replay_detects_deleted_call(tmp_path: Path) -> None:
    token_ledger = ledger(tmp_path)
    token_ledger.reserve("run-1", "task-1", "attempt-1", "call-1", 10)
    token_ledger.reconcile(
        "run-1", "task-1", "attempt-1", "call-1", 8, MeasurementKind.ACTUAL
    )
    with token_ledger.store.connect() as connection:
        connection.execute(
            "DELETE FROM token_calls WHERE execution_id = 'run-1'"
        )
    with pytest.raises(TokenLedgerError, match="conservation|replay"):
        token_ledger.summary("run-1")


def test_event_chain_detects_deletion_and_metadata_tamper(tmp_path: Path) -> None:
    first = ledger(tmp_path / "deleted")
    first.reserve("run-1", "task-1", "attempt-1", "call-1", 1)
    with first.store.connect() as connection:
        connection.execute(
            "DELETE FROM workspace_events WHERE event_type = 'TOKEN_RESERVED'"
        )
    with pytest.raises(SchemaMismatchError, match="event head|integrity"):
        first.summary("run-1")

    second = ledger(tmp_path / "metadata")
    second.reserve("run-1", "task-1", "attempt-1", "call-1", 1)
    with second.store.connect() as connection:
        connection.execute(
            """
            UPDATE workspace_events SET task_id = 'forged'
            WHERE event_type = 'TOKEN_RESERVED'
            """
        )
    with pytest.raises(SchemaMismatchError, match="integrity"):
        second.summary("run-1")

    third = ledger(tmp_path / "rehash")
    third.reserve("run-1", "task-1", "attempt-1", "call-1", 1)
    forged_payload = "{}"
    forged_hash = hashlib.sha256(forged_payload.encode()).hexdigest()
    with third.store.connect() as connection:
        connection.execute(
            """
            UPDATE workspace_events SET payload_json = ?, payload_sha256 = ?
            WHERE event_type = 'TOKEN_RESERVED'
            """,
            (forged_payload, forged_hash),
        )
    with pytest.raises(SchemaMismatchError, match="integrity"):
        third.summary("run-1")


def test_sqlite_integer_overflow_is_rejected(tmp_path: Path) -> None:
    token_ledger = TokenLedger(WorkspaceStore(tmp_path))
    with pytest.raises(TokenLedgerError, match="between"):
        token_ledger.create_execution("run", 1 << 63)
