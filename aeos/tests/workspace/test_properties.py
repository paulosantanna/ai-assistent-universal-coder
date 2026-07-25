from __future__ import annotations

import hashlib
from pathlib import Path

from hypothesis import HealthCheck, given, settings, strategies as st

from aeos.core.workspace.contracts import TaskSpec
from aeos.core.workspace.store import WorkspaceStore
from aeos.core.workspace.task_graph import TaskGraph
from aeos.core.workspace.token_ledger import MeasurementKind, TokenLedger


@given(st.permutations(["root", "left", "right", "leaf"]))
def test_dag_order_is_independent_of_insertion(order: list[str]) -> None:
    tasks = {
        "root": TaskSpec("root"),
        "left": TaskSpec("left", dependencies=("root",)),
        "right": TaskSpec("right", dependencies=("root",)),
        "leaf": TaskSpec("leaf", dependencies=("left", "right")),
    }
    graph = TaskGraph(tasks[task_id] for task_id in order)
    assert graph.topological_ids() == ("root", "left", "right", "leaf")


@given(
    limit=st.integers(min_value=0, max_value=10_000),
    reservations=st.lists(
        st.integers(min_value=0, max_value=1_000), min_size=0, max_size=20
    ),
)
@settings(
    max_examples=25,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_ledger_never_exceeds_limit(
    tmp_path: Path, limit: int, reservations: list[int]
) -> None:
    case = hashlib.sha256(repr((limit, reservations)).encode()).hexdigest()[:24]
    execution_id = f"run-{case}"
    ledger = TokenLedger(WorkspaceStore(tmp_path))
    ledger.create_execution(execution_id, limit)
    ledger.create_task_budget(execution_id, "task", limit)
    ledger.create_attempt_budget(execution_id, "task", "attempt", limit)
    charged = 0
    for index, requested in enumerate(reservations):
        remaining = limit - charged
        amount = min(requested, remaining)
        call_id = f"call-{index}"
        ledger.reserve(execution_id, "task", "attempt", call_id, amount)
        ledger.reconcile(
            execution_id,
            "task",
            "attempt",
            call_id,
            amount,
            MeasurementKind.ACTUAL,
        )
        charged += amount
    summary = ledger.summary(execution_id)
    assert 0 <= summary["charged_tokens"] <= limit
    assert summary["remaining_unreserved"] == limit - summary["charged_tokens"]
