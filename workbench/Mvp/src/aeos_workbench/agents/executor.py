"""Simple Agent Executor - dispatches tasks to agent specifications.

This is a basic executor that validates tasks against agent contracts
and manages the agent lifecycle. Full subagent orchestration is planned
for a future phase.
"""

from datetime import datetime, timezone


class AgentTask:
    def __init__(self, task_id, objective, target_agent, scope, evidence_required=None):
        self.task_id = task_id
        self.objective = objective
        self.target_agent = target_agent
        self.scope = scope
        self.evidence_required = evidence_required or ["code"]
        self.status = "pending"
        self.created = datetime.now(timezone.utc).isoformat()
        self.completed = None
        self.result = None
        self.evidence = []

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "objective": self.objective,
            "target_agent": self.target_agent,
            "scope": self.scope,
            "status": self.status,
            "created": self.created,
            "completed": self.completed,
            "evidence_count": len(self.evidence),
        }


class AgentExecutor:
    def __init__(self, registry):
        self.registry = registry
        self.tasks = []
        self.results = []

    def validate_task(self, task):
        agent = self.registry.get(task.target_agent)
        if not agent:
            return {"valid": False, "reason": "Agent not found: " + task.target_agent}
        spec = agent["spec"]
        task_scope = task.scope
        allowed_scopes = spec.get("scope", [])
        if "all" not in allowed_scopes and task_scope not in allowed_scopes:
            return {
                "valid": False,
                "reason": "Scope '" + task_scope + "' not in agent allowed scopes: " + str(allowed_scopes),
            }
        return {"valid": True, "agent": spec}

    def dispatch(self, task):
        validation = self.validate_task(task)
        if not validation["valid"]:
            task.status = "rejected"
            task.result = validation["reason"]
            return validation

        task.status = "running"
        self.tasks.append(task)

        task.status = "completed"
        task.completed = datetime.now(timezone.utc).isoformat()
        task.result = {
            "status": "completed",
            "agent": task.target_agent,
            "objective": task.objective,
            "note": "Task validated and dispatched. Execution requires agent implementation.",
        }

        self.results.append(task.to_dict())
        return task.result

    def get_queue(self):
        return [t.to_dict() for t in self.tasks if t.status == "running"]

    def get_completed(self):
        return [t.to_dict() for t in self.tasks if t.status == "completed"]

    def get_summary(self):
        return {
            "total": len(self.tasks),
            "running": sum(1 for t in self.tasks if t.status == "running"),
            "completed": sum(1 for t in self.tasks if t.status == "completed"),
            "rejected": sum(1 for t in self.tasks if t.status == "rejected"),
        }
