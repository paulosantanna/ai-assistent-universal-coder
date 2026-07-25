from __future__ import annotations

from pathlib import Path

import pytest

from aeos.core.workspace.store import (
    InvalidIdentifierError,
    SchemaMismatchError,
    WorkspaceStore,
    validate_identifier,
)


def test_store_is_isolated_and_reopens(tmp_path: Path) -> None:
    first = WorkspaceStore(tmp_path)
    assert first.database_path == tmp_path / ".aeos" / "workspace" / "workspace-v1.sqlite3"
    assert first.health()["integrity"] == "ok"

    second = WorkspaceStore(tmp_path)
    assert second.health()["schema_version"] == 1


@pytest.mark.parametrize(
    "value",
    ["", "../escape", "a/b", "a\\b", ".hidden", "space value", "x" * 129],
)
def test_identifier_rejects_unsafe_values(value: str) -> None:
    with pytest.raises(InvalidIdentifierError):
        validate_identifier(value)


def test_store_rejects_unknown_schema(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    with store.connect() as connection:
        connection.execute(
            "UPDATE workspace_metadata SET value = '999' WHERE key = 'schema_version'"
        )
    with pytest.raises(SchemaMismatchError):
        WorkspaceStore(tmp_path)


def test_store_transaction_rolls_back(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    with pytest.raises(RuntimeError):
        with store.transaction() as connection:
            connection.execute(
                "INSERT INTO executions(execution_id, hard_token_limit) VALUES ('run', 10)"
            )
            raise RuntimeError("simulated crash")

    with store.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0]
    assert count == 0
