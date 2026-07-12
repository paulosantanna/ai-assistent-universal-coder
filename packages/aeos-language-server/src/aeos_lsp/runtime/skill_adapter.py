from __future__ import annotations

import logging
import time
from typing import Any

from aeos_lsp.runtime.ports import ExecutionResult, SkillDefinition, SkillPort

logger = logging.getLogger(__name__)


class SkillAdapter(SkillPort):
    def __init__(self) -> None:
        self._initialized = False
        self._skills: dict[str, SkillDefinition] = {}

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        logger.info("Skill adapter initialized")

    async def shutdown(self) -> None:
        self._initialized = False
        self._skills.clear()
        logger.info("Skill adapter shut down")

    def register_skill(self, skill: SkillDefinition) -> None:
        self._skills[skill.id] = skill
        logger.debug("Registered skill: %s", skill.id)

    async def resolve(self, skill_ref: str) -> SkillDefinition | None:
        if skill_ref in self._skills:
            return self._skills[skill_ref]
        for sid, skill in self._skills.items():
            if skill_ref in sid or skill.name == skill_ref:
                return skill
        return None

    async def execute(
        self,
        skill: SkillDefinition,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        if not self._initialized:
            return ExecutionResult(success=False, error="Skill adapter not initialized")

        start = time.monotonic()
        try:
            missing_inputs = [i for i in skill.inputs if i not in inputs]
            if missing_inputs:
                return ExecutionResult(
                    success=False,
                    error=f"Missing required inputs: {', '.join(missing_inputs)}",
                    elapsed_seconds=time.monotonic() - start,
                )

            resolved_tools = []
            tool_adapter = None
            if context and "tool_adapter" in context:
                tool_adapter = context["tool_adapter"]

            for tool_ref in skill.tools:
                resolved_tools.append({
                    "reference": tool_ref,
                    "resolved": tool_adapter is not None,
                })

            output = {
                "status": "simulated",
                "inputs_received": len(inputs),
                "tools_invoked": resolved_tools,
                "instructions": skill.instructions[:200] if skill.instructions else "",
                "outputs": {o: f"<simulated:{o}>" for o in skill.outputs},
            }

            elapsed = time.monotonic() - start
            return ExecutionResult(
                success=True,
                output=output,
                elapsed_seconds=elapsed,
                metadata={
                    "skill_id": skill.id,
                    "tools_count": len(skill.tools),
                    "inputs_count": len(skill.inputs),
                },
            )
        except Exception as exc:
            elapsed = time.monotonic() - start
            logger.exception("Skill execution failed for %s", skill.id)
            return ExecutionResult(
                success=False,
                error=str(exc),
                elapsed_seconds=elapsed,
            )

    async def list_skills(self) -> list[SkillDefinition]:
        return list(self._skills.values())

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "skill_count": len(self._skills),
        }
