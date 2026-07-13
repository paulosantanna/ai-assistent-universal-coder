"""Playbook Step Engine — transforms playbooks into executable steps with per-step evidence."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PlaybookStepEngine:
    def __init__(self, evidence_dir: Path, execution_id: str):
        self.evidence_dir = evidence_dir / execution_id / "steps"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.steps: list[dict] = []

    def register_step(self, step: dict) -> str:
        step_id = step.get("step_id") or f"step-{uuid.uuid4().hex[:8]}"
        step["step_id"] = step_id
        step.setdefault("status", "pending")
        step.setdefault("inputs", {})
        step.setdefault("outputs", {})
        step.setdefault("evidence", [])
        step.setdefault("permission_decisions", [])
        step.setdefault("risks", [])
        step.setdefault("errors", [])
        step.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        self.steps.append(step)
        return step_id

    def update_step(self, step_id: str, updates: dict):
        for step in self.steps:
            if step["step_id"] == step_id:
                step.update(updates)
                if "status" in updates:
                    step["updated_at"] = datetime.now(timezone.utc).isoformat()
                return

    def save_step(self, step: dict) -> Path:
        path = self.evidence_dir / f"{step['step_id']}.step-result.json"
        path.write_text(json.dumps(step, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def save_all(self) -> list[Path]:
        paths = []
        for step in self.steps:
            paths.append(self.save_step(step))
        return paths

    def get_summary(self) -> dict:
        return {
            "total_steps": len(self.steps),
            "statuses": {
                s: sum(1 for st in self.steps if st.get("status") == s)
                for s in set(st.get("status", "unknown") for st in self.steps)
            },
        }