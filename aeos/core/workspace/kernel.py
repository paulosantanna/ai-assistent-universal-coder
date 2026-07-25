"""Autoridade transacional do novo namespace AEOS Workspace OS."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .contracts import (
    EvidenceClaim,
    KnowledgeKind,
    OutcomeStatus,
    TaskOutcome,
    TaskSnapshot,
    TaskSpec,
    TaskState,
)
from .evidence import EvidenceVerifier
from .redaction import assert_safe_payload, assert_safe_text, is_sensitive_key
from .scheduler import DeterministicScheduler
from .state_machine import transition
from .store import (
    MAX_SQLITE_INTEGER,
    WorkspaceStore,
    WorkspaceStoreError,
    validate_identifier,
)
from .task_graph import TaskGraph
from .token_ledger import TokenLedger


class WorkspacePlanError(WorkspaceStoreError):
    """Plano inválido ou conflitante."""


class WorkspaceKernel:
    """Planeja e consulta tarefas sem acionar runtimes, ferramentas ou modelos."""

    def __init__(
        self,
        store: WorkspaceStore,
        *,
        evidence_verifier: EvidenceVerifier | None = None,
    ):
        self.store = store
        self.ledger = TokenLedger(store)
        self.evidence_verifier = evidence_verifier

    def plan(self, document: Mapping[str, Any]) -> dict[str, Any]:
        execution_id, hard_limit, specs, task_limits = self._parse_plan(document)
        graph = TaskGraph(specs)

        with self.store.transaction() as connection:
            exists = connection.execute(
                "SELECT 1 FROM executions WHERE execution_id = ?", (execution_id,)
            ).fetchone()
            if exists is not None:
                raise WorkspacePlanError("execution_id already exists")
            connection.execute(
                "INSERT INTO executions(execution_id, hard_token_limit) VALUES (?, ?)",
                (execution_id, hard_limit),
            )
            for task_id in graph.topological_ids():
                spec = graph.task(task_id)
                connection.execute(
                    """
                    INSERT INTO task_budgets(execution_id, task_id, hard_token_limit)
                    VALUES (?, ?, ?)
                    """,
                    (execution_id, task_id, task_limits[task_id]),
                )
                payload = self._snapshot_payload(
                    spec, TaskSnapshot(task_id=task_id)
                )
                payload_json, payload_hash = self.store.canonical_payload(payload)
                connection.execute(
                    """
                    INSERT INTO task_snapshots(
                        execution_id, task_id, payload_json, payload_sha256, revision
                    ) VALUES (?, ?, ?, ?, 0)
                    """,
                    (execution_id, task_id, payload_json, payload_hash),
                )
            event = {
                "execution_id": execution_id,
                "hard_token_limit": hard_limit,
                "task_order": list(graph.topological_ids()),
                "tasks": [
                    {
                        **self._snapshot_payload(
                            graph.task(task_id), TaskSnapshot(task_id=task_id)
                        ),
                        "hard_token_limit": task_limits[task_id],
                    }
                    for task_id in graph.topological_ids()
                ],
            }
            self.store.append_event(
                connection,
                execution_id=execution_id,
                event_type="PLAN_CREATED",
                payload=event,
            )
        return self.status(execution_id)

    def status(self, execution_id: str) -> dict[str, Any]:
        validate_identifier(execution_id, "execution_id")
        with self.store.read_transaction() as connection:
            rows = self.store.load_task_snapshots(execution_id, connection)
            if not rows:
                raise WorkspacePlanError("unknown execution")
            specs = [self._spec_from_payload(row) for row in rows]
            snapshots = {
                row["task_id"]: self._snapshot_from_payload(row) for row in rows
            }
            graph = TaskGraph(specs)
            ready = DeterministicScheduler().select(graph, snapshots)
            events = self.store.load_verified_events(execution_id, connection)
            replayed_tasks = self._replay_tasks(events)
            if replayed_tasks != rows:
                raise WorkspacePlanError(
                    "materialized task state differs from event replay"
                )
            result = {
                "execution_id": execution_id,
                "health": self.store.health(connection),
                "verified_event_count": len(events),
                "replay_verified": True,
                "budget": self.ledger.summary(execution_id, connection),
                "ready_task_ids": [task.task_id for task in ready],
                "tasks": rows,
            }
        return result

    def transition_task(
        self,
        execution_id: str,
        task_id: str,
        target: TaskState,
        *,
        expected_revision: int,
        outcome: TaskOutcome | None = None,
    ) -> TaskSnapshot:
        rows = self.store.load_task_snapshots(execution_id)
        row = next((item for item in rows if item["task_id"] == task_id), None)
        if row is None:
            raise WorkspacePlanError("unknown task")
        current = self._snapshot_from_payload(row)
        if target is TaskState.READY:
            spec = self._spec_from_payload(row)
            snapshots = {
                item["task_id"]: self._snapshot_from_payload(item) for item in rows
            }
            if not all(
                snapshots[dependency].state is TaskState.COMPLETED
                for dependency in spec.dependencies
            ):
                raise WorkspacePlanError("task dependencies are not completed")
        changed = transition(
            current,
            target,
            expected_revision=expected_revision,
            outcome=outcome,
            verified_evidence_refs=self._verified_evidence_refs(
                execution_id, task_id, expected_revision
            ),
        )
        payload = self._snapshot_payload(self._spec_from_payload(row), changed)
        self.store.compare_and_swap_task(
            execution_id,
            task_id,
            expected_revision=expected_revision,
            payload=payload,
            event_type="TASK_TRANSITION",
        )
        return changed

    def register_evidence(
        self,
        execution_id: str,
        task_id: str,
        *,
        task_revision: int,
        evidence_id: str,
        evidence_type: str,
        artifact_path: str,
    ) -> str:
        if self.evidence_verifier is None:
            raise WorkspacePlanError("no evidence authority is configured")
        artifact = Path(artifact_path).resolve()
        verification = self.evidence_verifier.verify(
            execution_id=execution_id,
            task_id=task_id,
            task_revision=task_revision,
            evidence_type=evidence_type,
            artifact_path=artifact,
        )
        if not verification.accepted:
            raise WorkspacePlanError(
                f"evidence authority rejected artifact: {verification.reason}"
            )
        assert_safe_text(verification.provenance, "evidence provenance")
        return self.store.register_evidence(
            execution_id,
            task_id,
            task_revision=task_revision,
            evidence_id=evidence_id,
            evidence_type=evidence_type,
            artifact_path=artifact_path,
            verifier_id=verification.verifier_id,
            provenance=verification.provenance,
        )

    def _verified_evidence_refs(
        self, execution_id: str, task_id: str, task_revision: int
    ) -> frozenset[str]:
        if self.evidence_verifier is None:
            return frozenset()
        verified: set[str] = set()
        for candidate in self.store.evidence_candidates(
            execution_id, task_id, task_revision
        ):
            result = self.evidence_verifier.verify(
                execution_id=execution_id,
                task_id=task_id,
                task_revision=task_revision,
                evidence_type=candidate["evidence_type"],
                artifact_path=candidate["artifact_path"],
            )
            if result.accepted and result.verifier_id == candidate["verifier_id"]:
                verified.add(candidate["evidence_id"])
        return frozenset(verified)

    @staticmethod
    def _replay_tasks(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        tasks: dict[str, dict[str, Any]] = {}
        for event in events:
            event_type = event["event_type"]
            payload = event["payload"]
            if event_type == "PLAN_CREATED":
                if tasks:
                    raise WorkspacePlanError("duplicate plan event")
                tasks = {
                    str(task["task_id"]): {
                        key: value
                        for key, value in task.items()
                        if key != "hard_token_limit"
                    }
                    for task in payload["tasks"]
                }
            elif event_type == "TASK_TRANSITION":
                task = payload["task"]
                task_id = str(task["task_id"])
                if task_id not in tasks:
                    raise WorkspacePlanError("transition precedes task plan")
                tasks[task_id] = task
        if not tasks:
            raise WorkspacePlanError("execution has no replayable plan")
        return [tasks[task_id] for task_id in sorted(tasks)]

    @staticmethod
    def _parse_plan(
        document: Mapping[str, Any],
    ) -> tuple[str, int, list[TaskSpec], dict[str, int]]:
        if not isinstance(document, Mapping):
            raise WorkspacePlanError("plan must be a JSON object")
        execution_id = validate_identifier(
            document.get("execution_id"), "execution_id"
        )
        hard_limit = WorkspaceKernel._integer(
            document.get("hard_token_limit"), "hard_token_limit"
        )
        raw_tasks = document.get("tasks")
        if not isinstance(raw_tasks, list) or not raw_tasks:
            raise WorkspacePlanError("tasks must be a non-empty array")
        specs: list[TaskSpec] = []
        limits: dict[str, int] = {}
        for raw in raw_tasks:
            if not isinstance(raw, Mapping):
                raise WorkspacePlanError("each task must be an object")
            task_id = validate_identifier(raw.get("task_id"), "task_id")
            dependencies = raw.get("dependencies", [])
            metadata = raw.get("metadata", {})
            if not isinstance(dependencies, list) or not all(
                isinstance(value, str) for value in dependencies
            ):
                raise WorkspacePlanError("dependencies must be an array of strings")
            if not isinstance(metadata, Mapping) or not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in metadata.items()
            ):
                raise WorkspacePlanError("metadata must map strings to strings")
            sensitive = sorted(key for key in metadata if is_sensitive_key(key))
            if sensitive:
                raise WorkspacePlanError(
                    "sensitive values must not be persisted in task metadata"
                )
            assert_safe_payload(metadata, "task metadata")
            priority = WorkspaceKernel._integer(raw.get("priority", 0), "priority")
            token_limit = WorkspaceKernel._integer(
                raw.get("hard_token_limit"), "task hard_token_limit"
            )
            if token_limit > hard_limit:
                raise WorkspacePlanError("task token limit exceeds execution limit")
            specs.append(
                TaskSpec(
                    task_id=task_id,
                    priority=priority,
                    dependencies=tuple(dependencies),
                    metadata=dict(metadata),
                )
            )
            limits[task_id] = token_limit
        return execution_id, hard_limit, specs, limits

    @staticmethod
    def _integer(value: Any, field: str) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            or value > MAX_SQLITE_INTEGER
        ):
            raise WorkspacePlanError(
                f"{field} must be between 0 and {MAX_SQLITE_INTEGER}"
            )
        return value

    @staticmethod
    def _snapshot_payload(spec: TaskSpec, snapshot: TaskSnapshot) -> dict[str, Any]:
        outcome = None
        if snapshot.outcome is not None:
            outcome = {
                "status": snapshot.outcome.status.value,
                "summary": snapshot.outcome.summary,
                "claims": [
                    {
                        "kind": claim.kind.value,
                        "statement": claim.statement,
                        "evidence_refs": list(claim.evidence_refs),
                    }
                    for claim in snapshot.outcome.claims
                ],
            }
        payload = {
            "task_id": spec.task_id,
            "priority": spec.priority,
            "dependencies": list(spec.dependencies),
            "metadata": dict(spec.metadata),
            "state": snapshot.state.value,
            "revision": snapshot.revision,
            "outcome": outcome,
        }
        assert_safe_payload(payload, "task snapshot")
        return payload

    @staticmethod
    def _spec_from_payload(payload: Mapping[str, Any]) -> TaskSpec:
        return TaskSpec(
            task_id=str(payload["task_id"]),
            priority=int(payload["priority"]),
            dependencies=tuple(payload["dependencies"]),
            metadata=dict(payload["metadata"]),
        )

    @staticmethod
    def _snapshot_from_payload(payload: Mapping[str, Any]) -> TaskSnapshot:
        raw_outcome = payload.get("outcome")
        outcome = None
        if isinstance(raw_outcome, Mapping):
            outcome = TaskOutcome(
                status=OutcomeStatus(str(raw_outcome["status"])),
                summary=str(raw_outcome["summary"]),
                claims=tuple(
                    EvidenceClaim(
                        kind=KnowledgeKind(str(claim["kind"])),
                        statement=str(claim["statement"]),
                        evidence_refs=tuple(claim["evidence_refs"]),
                    )
                    for claim in raw_outcome["claims"]
                ),
            )
        return TaskSnapshot(
            task_id=str(payload["task_id"]),
            state=TaskState(str(payload["state"])),
            revision=int(payload["revision"]),
            outcome=outcome,
        )
