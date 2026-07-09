from __future__ import annotations

from typing import Any, Optional

from aeos.core.agent_runtime.agent_models import AgentTask, AgentResult, generate_task_id
from aeos.core.agent_runtime.agent_runtime import AgentRuntime
from aeos.core.agent_runtime.delegation_policy import DelegationPolicyEngine


class SubAgentRuntime:
    def __init__(self, parent_runtime: AgentRuntime):
        self.parent_runtime = parent_runtime

    def spawn_subagent(
        self,
        parent_task: AgentTask,
        sub_agent_id: str,
        sub_objective: str,
        sub_scope: dict[str, Any],
    ) -> AgentResult:
        return self.parent_runtime.delegate_task(
            parent_task=parent_task,
            child_agent_id=sub_agent_id,
            child_objective=sub_objective,
            child_scope=sub_scope,
        )

    def execute_skill_in_subagent(
        self,
        task: AgentTask,
        skill_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.parent_runtime.skill_executor:
            return {"status": "ERROR", "error": "No skill executor available"}

        from aeos.core.skill_engine.skill_models import SkillRequest
        sr = SkillRequest(
            execution_id=task.execution_id,
            skill_id=skill_id,
            actor=task.actor,
            role=task.role,
            input=input_data,
        )
        skill_result = self.parent_runtime.skill_executor.execute(sr)
        return skill_result.to_dict()

    def execute_playbook_in_subagent(
        self,
        task: AgentTask,
        playbook_id: str,
        input_data: dict[str, Any],
        dry_run: bool = True,
    ) -> dict[str, Any]:
        if not self.parent_runtime.playbook_executor:
            return {"status": "ERROR", "error": "No playbook executor available"}

        from aeos.core.playbook_engine.playbook_models import PlaybookRequest
        pr = PlaybookRequest(
            execution_id=task.execution_id,
            playbook_id=playbook_id,
            actor=task.actor,
            role=task.role,
            target_path=".",
            input=input_data,
            dry_run=dry_run,
        )
        playbook_result = self.parent_runtime.playbook_executor.execute(pr)
        return playbook_result.to_dict()
