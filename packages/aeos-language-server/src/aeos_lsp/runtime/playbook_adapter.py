from __future__ import annotations

import logging
import time
from typing import Any

from aeos_lsp.runtime.ports import ExecutionResult, PlaybookDefinition, PlaybookPort

logger = logging.getLogger(__name__)


class PlaybookAdapter(PlaybookPort):
    def __init__(self) -> None:
        self._initialized = False
        self._playbooks: dict[str, PlaybookDefinition] = {}

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        logger.info("Playbook adapter initialized")

    async def shutdown(self) -> None:
        self._initialized = False
        self._playbooks.clear()
        logger.info("Playbook adapter shut down")

    def register_playbook(self, playbook: PlaybookDefinition) -> None:
        self._playbooks[playbook.id] = playbook
        logger.debug("Registered playbook: %s", playbook.id)

    async def resolve(self, playbook_ref: str) -> PlaybookDefinition | None:
        if playbook_ref in self._playbooks:
            return self._playbooks[playbook_ref]
        for pid, pb in self._playbooks.items():
            if playbook_ref in pid or pb.name == playbook_ref:
                return pb
        return None

    async def execute(
        self,
        playbook: PlaybookDefinition,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        if not self._initialized:
            return ExecutionResult(success=False, error="Playbook adapter not initialized")

        start = time.monotonic()
        try:
            step_results = []
            for i, step in enumerate(playbook.steps):
                step_name = step.get("name", f"step_{i}")
                step_type = step.get("type", "tool")
                step_tool = step.get("tool", "")
                step_skill = step.get("skill", "")

                step_output = {
                    "step_index": i,
                    "step_name": step_name,
                    "step_type": step_type,
                    "status": "simulated",
                }

                if step.get("approval", False):
                    step_output["approval_required"] = True
                    step_output["approval_status"] = "pending"

                step_results.append(step_output)

            elapsed = time.monotonic() - start
            return ExecutionResult(
                success=True,
                output={
                    "status": "completed",
                    "steps_completed": len(step_results),
                    "steps": step_results,
                },
                elapsed_seconds=elapsed,
                metadata={
                    "playbook_id": playbook.id,
                    "step_count": len(playbook.steps),
                },
            )
        except Exception as exc:
            elapsed = time.monotonic() - start
            logger.exception("Playbook execution failed for %s", playbook.id)
            return ExecutionResult(
                success=False,
                error=str(exc),
                elapsed_seconds=elapsed,
            )

    async def list_playbooks(self) -> list[PlaybookDefinition]:
        return list(self._playbooks.values())

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "playbook_count": len(self._playbooks),
        }
