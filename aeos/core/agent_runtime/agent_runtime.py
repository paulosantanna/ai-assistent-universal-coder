"""AEOS Agent Runtime — controlled agent orchestration with delegation, context, trace and judge."""

from dataclasses import asdict


class AgentRuntime:
    def __init__(self, registry, delegation_policy, context_router, trace_store, judge_gateway):
        self.registry = registry
        self.delegation_policy = delegation_policy
        self.context_router = context_router
        self.trace_store = trace_store
        self.judge_gateway = judge_gateway

    def assign_task(self, task):
        agent = self.registry.resolve(task.assigned_agent)
        if not agent:
            task.status = "BLOCKED"
            self.trace_store.write_event(task.execution_id, {
                "task_id": task.task_id,
                "agent_id": task.assigned_agent,
                "state": "BLOCKED",
                "reason": "agent_not_registered"
            })
            return task

        validation = self.judge_gateway.validate_task_delegation(
            task.execution_id, task.parent_task_id or "root", task.assigned_agent, asdict(task)
        )
        if not validation.get("allowed", False):
            task.status = "BLOCKED"
            self.trace_store.write_event(task.execution_id, {
                "task_id": task.task_id,
                "agent_id": task.assigned_agent,
                "state": "BLOCKED",
                "reason": validation.get("reason", "delegation_denied")
            })
            return task

        if task.parent_task_id:
            delegation = self.delegation_policy.can_delegate(
                task.parent_task_id, task.assigned_agent, asdict(task)
            )
            if not delegation.get("allowed", False):
                task.status = "BLOCKED"
                self.trace_store.write_event(task.execution_id, {
                    "task_id": task.task_id,
                    "agent_id": task.assigned_agent,
                    "state": "BLOCKED",
                    "reason": delegation.get("reason", "policy_denied")
                })
                return task

        context_packet = self.context_router.build_context_packet(task.execution_id, asdict(task))
        task.status = "ASSIGNED"
        self.trace_store.write_event(task.execution_id, {
            "task_id": task.task_id,
            "agent_id": task.assigned_agent,
            "state": "ASSIGNED",
            "context_refs": [context_packet.get("context_id")]
        })
        return task

    def finalize_execution(self, execution_id: str, task_graph):
        return self.judge_gateway.validate_agent_runtime(execution_id, task_graph)