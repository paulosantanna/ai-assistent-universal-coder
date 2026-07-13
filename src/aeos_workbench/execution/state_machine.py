"""Execution State Machine — formal states, transitions, and persistence."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from enum import Enum
from typing import Optional

class ExecutionState(str, Enum):
    PENDING = "PENDING"
    VALIDATING_CONFIG = "VALIDATING_CONFIG"
    RESOLVING_PLAYBOOK = "RESOLVING_PLAYBOOK"
    RESOLVING_CONTEXT = "RESOLVING_CONTEXT"
    CHECKING_PERMISSIONS = "CHECKING_PERMISSIONS"
    DRY_RUN = "DRY_RUN"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    EXECUTING = "EXECUTING"
    COLLECTING_EVIDENCE = "COLLECTING_EVIDENCE"
    JUDGING = "JUDGING"
    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"

_TRANSITIONS = {
    ExecutionState.PENDING: [ExecutionState.VALIDATING_CONFIG, ExecutionState.BLOCKED],
    ExecutionState.VALIDATING_CONFIG: [ExecutionState.RESOLVING_PLAYBOOK, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.RESOLVING_PLAYBOOK: [ExecutionState.RESOLVING_CONTEXT, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.RESOLVING_CONTEXT: [ExecutionState.CHECKING_PERMISSIONS, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.CHECKING_PERMISSIONS: [ExecutionState.DRY_RUN, ExecutionState.WAITING_APPROVAL, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.DRY_RUN: [ExecutionState.WAITING_APPROVAL, ExecutionState.EXECUTING, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.WAITING_APPROVAL: [ExecutionState.EXECUTING, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.EXECUTING: [ExecutionState.COLLECTING_EVIDENCE, ExecutionState.FAILED, ExecutionState.BLOCKED],
    ExecutionState.COLLECTING_EVIDENCE: [ExecutionState.JUDGING, ExecutionState.FAILED, ExecutionState.BLOCKED],
    ExecutionState.JUDGING: [ExecutionState.PASSED, ExecutionState.BLOCKED, ExecutionState.FAILED],
    ExecutionState.PASSED: [ExecutionState.ROLLED_BACK],
    ExecutionState.BLOCKED: [],
    ExecutionState.FAILED: [ExecutionState.ROLLED_BACK],
    ExecutionState.ROLLED_BACK: [],
}


class ExecutionStateMachine:
    def __init__(self, execution_id: Optional[str] = None):
        self.execution_id = execution_id or f"ex-{uuid.uuid4().hex[:12]}"
        self.state = ExecutionState.PENDING
        self.history: list[dict] = []
        self.metadata: dict = {}
        self._add_history("Initialized")

    def _add_history(self, detail: str):
        self.history.append({
            "state": self.state.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "detail": detail,
        })

    def transition(self, target: ExecutionState, detail: str = "") -> bool:
        if target not in _TRANSITIONS.get(self.state, []):
            raise ValueError(
                f"Invalid transition: {self.state.value} -> {target.value}. "
                f"Allowed: {[s.value for s in _TRANSITIONS.get(self.state, [])]}"
            )
        self.state = target
        self._add_history(detail or f"Transitioned to {target.value}")
        return True

    def save(self, evidence_dir: Path):
        path = evidence_dir / self.execution_id / "execution-state.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "execution_id": self.execution_id,
            "current_state": self.state.value,
            "history": self.history,
            "metadata": self.metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    @staticmethod
    def load(evidence_dir: Path, execution_id: str) -> "ExecutionStateMachine":
        path = evidence_dir / execution_id / "execution-state.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        sm = ExecutionStateMachine(execution_id)
        sm.state = ExecutionState(data["current_state"])
        sm.history = data["history"]
        sm.metadata = data.get("metadata", {})
        return sm