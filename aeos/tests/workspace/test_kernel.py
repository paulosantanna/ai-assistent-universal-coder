from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event, Thread
from typing import Any

import pytest

from aeos.core.workspace.contracts import (
    EvidenceClaim,
    KnowledgeKind,
    OutcomeStatus,
    TaskOutcome,
    TaskState,
)
from aeos.core.workspace.kernel import WorkspaceKernel, WorkspacePlanError
from aeos.core.workspace.evidence import EvidenceVerification
from aeos.core.workspace.state_machine import CompletionEvidenceRequired
from aeos.core.workspace.exceptions import RevisionConflictError
from aeos.core.workspace.store import (
    SchemaMismatchError,
    WorkspaceStore,
    WorkspaceStoreError,
)


def plan_document() -> dict[str, object]:
    return {
        "execution_id": "run-1",
        "hard_token_limit": 100,
        "tasks": [
            {
                "task_id": "second",
                "priority": 9,
                "dependencies": ["first"],
                "hard_token_limit": 60,
            },
            {
                "task_id": "first",
                "priority": 1,
                "hard_token_limit": 40,
            },
        ],
    }


class StubEvidenceAuthority:
    def verify(self, **values: Any) -> EvidenceVerification:
        artifact = values["artifact_path"]
        accepted = artifact.is_file() and artifact.read_text(encoding="utf-8") != "TAMPERED"
        return EvidenceVerification(
            accepted=accepted,
            verifier_id="test-authority-v1",
            provenance="pytest:test_kernel",
            reason="artifact missing or modified" if not accepted else "",
        )


class SecretProvenanceAuthority(StubEvidenceAuthority):
    def verify(self, **values: Any) -> EvidenceVerification:
        result = super().verify(**values)
        return EvidenceVerification(
            accepted=result.accepted,
            verifier_id=result.verifier_id,
            provenance="client_secret=must-not-persist",
            reason=result.reason,
        )


def trusted_kernel(tmp_path: Path) -> WorkspaceKernel:
    return WorkspaceKernel(
        WorkspaceStore(tmp_path), evidence_verifier=StubEvidenceAuthority()
    )


def evidenced_outcome() -> TaskOutcome:
    return TaskOutcome(
        OutcomeStatus.SUCCEEDED,
        "verified",
        (
            EvidenceClaim(
                KnowledgeKind.FACT,
                "test passed",
                ("evidence-1",),
            ),
        ),
    )


def test_plan_is_atomic_deterministic_and_reopens(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    status = kernel.plan(plan_document())
    assert status["ready_task_ids"] == ["first"]
    assert [task["task_id"] for task in status["tasks"]] == ["first", "second"]
    reopened = WorkspaceKernel(
        WorkspaceStore(tmp_path, create=False, read_only=True)
    )
    assert reopened.status("run-1")["ready_task_ids"] == ["first"]
    with pytest.raises(WorkspacePlanError):
        kernel.plan(plan_document())


def test_dependency_requires_completed_not_blocked(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())
    first = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    kernel.transition_task(
        "run-1", "first", TaskState.BLOCKED, expected_revision=first.revision
    )
    assert kernel.status("run-1")["ready_task_ids"] == []
    with pytest.raises(WorkspacePlanError):
        kernel.transition_task("run-1", "second", TaskState.READY, expected_revision=0)


def test_evidenced_completion_unlocks_dependency(tmp_path: Path) -> None:
    kernel = trusted_kernel(tmp_path)
    kernel.plan(plan_document())
    ready = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    running = kernel.transition_task(
        "run-1", "first", TaskState.RUNNING, expected_revision=ready.revision
    )
    artifact = tmp_path / "test-result.txt"
    artifact.write_text("pytest test_kernel: PASS", encoding="utf-8")
    kernel.register_evidence(
        "run-1",
        "first",
        task_revision=running.revision,
        evidence_id="evidence-1",
        evidence_type="TEST_RESULT",
        artifact_path=str(artifact),
    )
    kernel.transition_task(
        "run-1",
        "first",
        TaskState.COMPLETED,
        expected_revision=running.revision,
        outcome=evidenced_outcome(),
    )
    assert kernel.status("run-1")["ready_task_ids"] == ["second"]


def test_claim_cannot_self_attest_completion(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())
    ready = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    running = kernel.transition_task(
        "run-1", "first", TaskState.RUNNING, expected_revision=ready.revision
    )
    with pytest.raises(CompletionEvidenceRequired, match="independently verified"):
        kernel.transition_task(
            "run-1",
            "first",
            TaskState.COMPLETED,
            expected_revision=running.revision,
            outcome=evidenced_outcome(),
        )


def test_failed_outcome_survives_persistence_and_replay(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())
    ready = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    running = kernel.transition_task(
        "run-1", "first", TaskState.RUNNING, expected_revision=ready.revision
    )
    kernel.transition_task(
        "run-1",
        "first",
        TaskState.FAILED,
        expected_revision=running.revision,
        outcome=TaskOutcome(OutcomeStatus.FAILED, "command failed"),
    )
    task = kernel.status("run-1")["tasks"][0]
    assert task["state"] == "FAILED"
    assert task["outcome"]["status"] == "FAILED"
    assert kernel.status("run-1")["replay_verified"] is True


def test_evidence_artifact_tamper_blocks_completion(tmp_path: Path) -> None:
    kernel = trusted_kernel(tmp_path)
    kernel.plan(plan_document())
    ready = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    running = kernel.transition_task(
        "run-1", "first", TaskState.RUNNING, expected_revision=ready.revision
    )
    artifact = tmp_path / "result.txt"
    artifact.write_text("PASS", encoding="utf-8")
    kernel.register_evidence(
        "run-1",
        "first",
        task_revision=running.revision,
        evidence_id="evidence-1",
        evidence_type="TEST_RESULT",
        artifact_path=str(artifact),
    )
    artifact.write_text("TAMPERED", encoding="utf-8")
    with pytest.raises(CompletionEvidenceRequired):
        kernel.transition_task(
            "run-1",
            "first",
            TaskState.COMPLETED,
            expected_revision=running.revision,
            outcome=evidenced_outcome(),
        )


def test_evidence_registration_denies_without_authority(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())
    artifact = tmp_path / "result.txt"
    artifact.write_text("PASS", encoding="utf-8")
    with pytest.raises(WorkspacePlanError, match="no evidence authority"):
        kernel.register_evidence(
            "run-1",
            "first",
            task_revision=0,
            evidence_id="evidence-1",
            evidence_type="TEST_RESULT",
            artifact_path=str(artifact),
        )


def test_sensitive_evidence_provenance_is_not_persisted(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    kernel = WorkspaceKernel(
        store, evidence_verifier=SecretProvenanceAuthority()
    )
    kernel.plan(plan_document())
    artifact = tmp_path / "result.txt"
    artifact.write_text("PASS", encoding="utf-8")
    with pytest.raises(ValueError, match="sensitive"):
        kernel.register_evidence(
            "run-1",
            "first",
            task_revision=0,
            evidence_id="evidence-1",
            evidence_type="TEST_RESULT",
            artifact_path=str(artifact),
        )
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM evidence_records").fetchone()[0] == 0
        assert connection.execute("SELECT event_count FROM executions").fetchone()[0] == 1


def test_task_cas_allows_only_one_concurrent_transition(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())

    def mark_ready() -> str:
        try:
            kernel.transition_task(
                "run-1", "first", TaskState.READY, expected_revision=0
            )
            return "changed"
        except RevisionConflictError:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: mark_ready(), range(2)))
    assert sorted(results) == ["changed", "conflict"]


def test_snapshot_tampering_is_detected(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    kernel = WorkspaceKernel(store)
    kernel.plan(plan_document())
    with store.connect() as connection:
        connection.execute(
            """
            UPDATE task_snapshots SET payload_json = '{"task_id":"forged"}'
            WHERE execution_id = 'run-1' AND task_id = 'first'
            """
        )
    with pytest.raises(SchemaMismatchError):
        kernel.status("run-1")


def test_event_tampering_is_detected(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    kernel = WorkspaceKernel(store)
    kernel.plan(plan_document())
    with store.connect() as connection:
        connection.execute(
            "UPDATE workspace_events SET payload_json = '{}' WHERE event_id = 1"
        )
    with pytest.raises(SchemaMismatchError):
        kernel.status("run-1")


def test_large_dag_plan_and_status_are_complete(tmp_path: Path) -> None:
    tasks = []
    for index in range(500):
        task = {
            "task_id": f"task-{index:04d}",
            "hard_token_limit": 1,
        }
        if index:
            task["dependencies"] = [f"task-{index - 1:04d}"]
        tasks.append(task)
    document = {
        "execution_id": "volume-run",
        "hard_token_limit": 500,
        "tasks": tasks,
    }
    status = WorkspaceKernel(WorkspaceStore(tmp_path)).plan(document)
    assert len(status["tasks"]) == 500
    assert status["ready_task_ids"] == ["task-0000"]
    assert status["verified_event_count"] == 1
    assert status["replay_verified"] is True


@pytest.mark.parametrize(
    "mutation",
    [
        {"hard_token_limit": -1},
        {"tasks": []},
        {"execution_id": "../escape"},
        {
            "tasks": [
                {
                    "task_id": "task",
                    "hard_token_limit": 1,
                    "metadata": {"api_key": "must-not-persist"},
                }
            ]
        },
    ],
)
def test_invalid_plans_leave_no_execution(
    tmp_path: Path, mutation: dict[str, object]
) -> None:
    store = WorkspaceStore(tmp_path)
    document = plan_document()
    document.update(mutation)
    with pytest.raises((ValueError, WorkspaceStoreError)):
        WorkspaceKernel(store).plan(document)
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


@pytest.mark.parametrize(
    "key",
    [
        "client_secret",
        "private_key",
        "token",
        "passphrase",
        "session_cookie",
        "OpenAIApiKey",
        "authorization",
    ],
)
def test_sensitive_metadata_families_fail_atomically(tmp_path: Path, key: str) -> None:
    store = WorkspaceStore(tmp_path)
    document = plan_document()
    document["tasks"] = [
        {
            "task_id": "task",
            "hard_token_limit": 1,
            "metadata": {key: "must-not-persist"},
        }
    ]
    with pytest.raises(WorkspacePlanError, match="sensitive"):
        WorkspaceKernel(store).plan(document)
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM workspace_events").fetchone()[0] == 0


def test_sensitive_outcome_text_does_not_mutate_snapshot(tmp_path: Path) -> None:
    kernel = WorkspaceKernel(WorkspaceStore(tmp_path))
    kernel.plan(plan_document())
    ready = kernel.transition_task("run-1", "first", TaskState.READY, expected_revision=0)
    running = kernel.transition_task(
        "run-1", "first", TaskState.RUNNING, expected_revision=ready.revision
    )
    with pytest.raises(ValueError, match="sensitive"):
        kernel.transition_task(
            "run-1",
            "first",
            TaskState.FAILED,
            expected_revision=running.revision,
            outcome=TaskOutcome(OutcomeStatus.FAILED, "password=hunter2"),
        )
    status = kernel.status("run-1")
    assert status["tasks"][0]["state"] == "RUNNING"


def test_status_is_one_snapshot_during_concurrent_commit(
    tmp_path: Path, monkeypatch
) -> None:
    store = WorkspaceStore(tmp_path)
    kernel = WorkspaceKernel(store)
    kernel.plan(plan_document())
    read_started = Event()
    writer_done = Event()
    original = store.load_task_snapshots

    def paused_load(execution_id, connection=None):
        rows = original(execution_id, connection)
        if connection is not None:
            read_started.set()
            assert writer_done.wait(10)
        return rows

    monkeypatch.setattr(store, "load_task_snapshots", paused_load)

    def writer() -> None:
        assert read_started.wait(10)
        kernel.transition_task(
            "run-1", "first", TaskState.READY, expected_revision=0
        )
        writer_done.set()

    thread = Thread(target=writer)
    thread.start()
    during = kernel.status("run-1")
    thread.join(timeout=10)
    assert not thread.is_alive()
    assert during["tasks"][0]["state"] == "PENDING"
    assert during["verified_event_count"] == 1

    after = kernel.status("run-1")
    assert after["tasks"][0]["state"] == "READY"
    assert after["verified_event_count"] == 2
