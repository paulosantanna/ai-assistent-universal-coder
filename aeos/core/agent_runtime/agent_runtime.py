from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, Optional

from aeos.core.agent_runtime.agent_models import (
    AgentTask,
    AgentResult,
    AgentMessage,
    AgentContract,
    generate_task_id,
)
from aeos.core.agent_runtime.agent_loader import AgentLoader
from aeos.core.agent_runtime.agent_contract_validator import AgentContractValidator
from aeos.core.agent_runtime.delegation_policy import DelegationPolicyEngine
from aeos.core.agent_runtime.context_router import ContextRouter
from aeos.core.agent_runtime.trace_store import AgentTraceStore
from aeos.core.agent_runtime.message_bus import MessageBus
from aeos.core.agent_runtime.agent_result_validator import AgentResultValidator
from aeos.core.agent_runtime.agent_reporter import AgentReporter
from aeos.core.tool_router.router import ToolRouter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.skill_engine.skill_models import SkillRequest
from aeos.core.playbook_engine.playbook_executor import PlaybookExecutor
from aeos.core.playbook_engine.playbook_models import PlaybookRequest
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import GovernanceRequest
from aeos.core.evidence.evidence_store import EvidenceStore


class AgentRuntime:
    def __init__(
        self,
        workspace_root: str = ".",
        tool_router: Optional[ToolRouter] = None,
        skill_executor: Optional[SkillExecutor] = None,
        playbook_executor: Optional[PlaybookExecutor] = None,
        governance_gate: Optional[GovernanceGate] = None,
        evidence_store: Optional[EvidenceStore] = None,
    ):
        self.workspace_root = Path(workspace_root)
        self.loader = AgentLoader(workspace_root)
        self.contract_validator = AgentContractValidator(workspace_root)
        self.trace_store = AgentTraceStore(str(self.workspace_root))
        self.message_bus = MessageBus()
        self.result_validator = AgentResultValidator()
        self.reporter = AgentReporter(workspace_root)
        self.tool_router = tool_router
        self.skill_executor = skill_executor
        self.playbook_executor = playbook_executor
        self.governance_gate = governance_gate
        self.evidence_store = evidence_store or EvidenceStore()
        self._delegation_history: dict[str, set[str]] = {}

    def execute_task(self, task: AgentTask) -> AgentResult:
        started = monotonic()
        execution_id = task.execution_id

        self.evidence_store.store_record(execution_id, "agent-task", task.to_dict())

        contract = self.loader.load_agent_contract(task.agent_id)

        validation = self.contract_validator.validate(task.agent_id)
        self.evidence_store.store_record(execution_id, "agent-contract-validation", validation)

        if contract is None or not validation["valid"]:
            result = AgentResult(
                execution_id=execution_id,
                task_id=task.task_id,
                agent_id=task.agent_id,
                status="BLOCKED",
                blocking_conditions=validation.get("findings", ["Agent not found"]),
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
            self.reporter.generate_report(execution_id, task, result)
            return result

        contract_path = contract.path or self.loader.resolver.get_agent_path(task.agent_id)
        if contract_path:
            fp = self.workspace_root / contract_path
            if not fp.exists():
                result = AgentResult(
                    execution_id=execution_id,
                    task_id=task.task_id,
                    agent_id=task.agent_id,
                    status="BLOCKED",
                    blocking_conditions=[f"Agent file does not exist: {fp}"],
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
                self.reporter.generate_report(execution_id, task, result)
                return result

        if self.governance_gate:
            cap = contract.capabilities[0] if contract and contract.capabilities else ""
            gov_req = GovernanceRequest(
                execution_id=execution_id,
                action="agent.execute_task",
                actor=task.actor,
                role=task.role,
                capability=cap,
                resource=f"agent:{task.agent_id}",
            )
            gov_result = self.governance_gate.evaluate(gov_req)
            if gov_result.status in ("BLOCKED", "WAITING_APPROVAL"):
                result = AgentResult(
                    execution_id=execution_id,
                    task_id=task.task_id,
                    agent_id=task.agent_id,
                    status=gov_result.status,
                    blocking_conditions=[gov_result.blocking_reason],
                    evidence_refs=gov_result.evidence_refs,
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
                self.reporter.generate_report(execution_id, task, result)
                return result

        msg = AgentMessage(
            execution_id=execution_id,
            task_id=task.task_id,
            from_agent="runtime",
            message_type="task_assigned",
            payload={"task_id": task.task_id, "objective": task.objective},
            to_agent=task.agent_id,
        )
        msg_id = self.message_bus.send(msg)
        self.trace_store.write_event(execution_id, {
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "state": "ASSIGNED",
            "message_id": msg_id,
        })
        self.evidence_store.store_record(execution_id, "agent-message", msg.to_dict())

        skill_results_list: list[dict[str, Any]] = []
        playbook_results_list: list[dict[str, Any]] = []
        tool_results_list: list[dict[str, Any]] = []
        all_evidence_refs: list[str] = []

        if contract and "execute_skill" in contract.allowed_actions and self.skill_executor:
            sr = SkillRequest(
                execution_id=execution_id,
                skill_id="repo-scanner",
                actor=task.actor,
                role=task.role,
                input=task.scope,
            )
            skill_result = self.skill_executor.execute(sr)
            skill_results_list.append(skill_result.to_dict())
            all_evidence_refs.extend(skill_result.evidence_refs)

        if contract and "execute_playbook" in contract.allowed_actions and self.playbook_executor:
            pr = PlaybookRequest(
                execution_id=execution_id,
                playbook_id="project-analysis",
                actor=task.actor,
                role=task.role,
                target_path=".",
                input=task.scope,
                dry_run=True,
            )
            playbook_result = self.playbook_executor.execute(pr)
            playbook_results_list.append(playbook_result.to_dict())
            all_evidence_refs.extend(playbook_result.evidence_refs)

        all_evidence_refs.extend(task.evidence_refs)

        result = AgentResult(
            execution_id=execution_id,
            task_id=task.task_id,
            agent_id=task.agent_id,
            status="PASS",
            messages=self.message_bus.get_messages_by_task(task.task_id),
            skill_results=skill_results_list,
            playbook_results=playbook_results_list,
            tool_results=tool_results_list,
            facts=[
                {"claim": f"Agent {task.agent_id} executed task {task.task_id}", "evidence": execution_id},
            ],
            assumptions=[
                {"assumption": "All allowed actions were executed via governed paths", "evidence_ref": execution_id},
            ],
            evidence_refs=all_evidence_refs,
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
        self.reporter.generate_report(execution_id, task, result)
        return result

    def delegate_task(
        self,
        parent_task: AgentTask,
        child_agent_id: str,
        child_objective: str,
        child_scope: dict[str, Any],
    ) -> AgentResult:
        started = monotonic()
        execution_id = parent_task.execution_id

        # Block agent delegating to itself
        if child_agent_id == parent_task.agent_id:
            result = AgentResult(
                execution_id=execution_id,
                task_id=parent_task.task_id,
                agent_id=child_agent_id,
                status="BLOCKED",
                blocking_conditions=["Agent cannot delegate to itself"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
            return result

        # Block self-judging
        if child_agent_id == "judge" and parent_task.agent_id == "judge":
            result = AgentResult(
                execution_id=execution_id,
                task_id=parent_task.task_id,
                agent_id=child_agent_id,
                status="BLOCKED",
                blocking_conditions=["Agent self-judging is forbidden"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
            return result

        # Check delegation policy
        parent_contract = self.loader.load_agent_contract(parent_task.agent_id)
        if parent_contract:
            dep = DelegationPolicyEngine(parent_contract.delegation_policy)
            policy_result = dep.can_delegate(parent_task.agent_id, child_agent_id, parent_task.to_dict())
            if not policy_result.get("allowed", False):
                result = AgentResult(
                    execution_id=execution_id,
                    task_id=parent_task.task_id,
                    agent_id=child_agent_id,
                    status="BLOCKED",
                    blocking_conditions=[f"Delegation denied: {policy_result.get('reason', 'policy_denied')}"],
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
                return result

        # Detect delegation loops
        if child_agent_id in self._delegation_history.get(parent_task.task_id, set()):
            result = AgentResult(
                execution_id=execution_id,
                task_id=parent_task.task_id,
                agent_id=child_agent_id,
                status="BLOCKED",
                blocking_conditions=["Delegation loop detected"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "agent-result", result.to_dict())
            return result

        if parent_task.task_id not in self._delegation_history:
            self._delegation_history[parent_task.task_id] = set()
        self._delegation_history[parent_task.task_id].add(child_agent_id)

        child_task = AgentTask(
            execution_id=execution_id,
            task_id=generate_task_id(),
            agent_id=child_agent_id,
            actor=parent_task.actor,
            role=parent_task.role,
            objective=child_objective,
            scope=child_scope,
            context_refs=parent_task.context_refs,
            evidence_refs=parent_task.evidence_refs,
            parent_task_id=parent_task.task_id,
        )

        delegation_record = {
            "parent_task_id": parent_task.task_id,
            "parent_agent": parent_task.agent_id,
            "child_task_id": child_task.task_id,
            "child_agent": child_agent_id,
            "objective": child_objective,
        }
        self.evidence_store.store_record(execution_id, "agent-delegation", delegation_record)
        self.trace_store.write_event(execution_id, {
            "event": "delegation",
            "from": parent_task.agent_id,
            "to": child_agent_id,
            "task_id": child_task.task_id,
        })

        child_result = self.execute_task(child_task)
        return child_result

    def finalize_execution(self, execution_id: str) -> dict[str, Any]:
        messages = self.message_bus.get_all_messages()
        return {
            "execution_id": execution_id,
            "message_count": len(messages),
            "delegation_history": {k: list(v) for k, v in self._delegation_history.items()},
        }
