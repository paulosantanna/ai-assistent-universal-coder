"""AEOS Agent Runtime Judge Gateway — validates agent execution through Judge Layer."""

from dataclasses import asdict


class AgentJudgeGateway:
    def __init__(self, judge_engine, evidence_store):
        self.judge_engine = judge_engine
        self.evidence_store = evidence_store

    def validate_agent_runtime(self, execution_id: str, task_graph) -> dict:
        graph_dict = task_graph.to_dict()
        tasks = graph_dict.get("tasks", {})
        if not tasks:
            return {"decision": "BLOCKED", "reason": "no_tasks", "score": 0.0}

        evidence = {
            "execution_id": execution_id,
            "task_count": len(tasks),
            "completed_count": sum(1 for t in tasks.values() if t.get("status") == "COMPLETED"),
            "blocked_count": sum(1 for t in tasks.values() if t.get("status") == "BLOCKED"),
        }

        if evidence["blocked_count"] > 0:
            return {"decision": "BLOCKED", "reason": "tasks_blocked", "score": 0.0, "evidence": evidence}

        result = self.judge_engine.evaluate(evidence)
        return result

    def validate_task_delegation(self, execution_id: str, parent_agent: str, child_agent: str, task: dict) -> dict:
        if parent_agent == child_agent:
            return {"allowed": False, "reason": "self_delegation_forbidden"}

        if task.get("risk_level") in ("high", "critical") and child_agent == "judge":
            return {"allowed": False, "reason": "judge_cannot_execute_high_risk_tasks"}

        return {"allowed": True, "reason": "delegation_allowed"}

    def validate_execution_finalization(self, execution_id: str, task_graph, judge_report: dict) -> dict:
        graph_dict = task_graph.to_dict()
        incomplete = [
            tid for tid, t in graph_dict.get("tasks", {}).items()
            if t.get("status") not in ("COMPLETED", "BLOCKED")
        ]
        if incomplete:
            return {"decision": "BLOCKED", "reason": "incomplete_tasks", "incomplete": incomplete, "score": 0.0}

        if judge_report.get("decision") == "BLOCKED":
            return {"decision": "BLOCKED", "reason": "judge_blocked", "score": judge_report.get("final_score", 0.0)}

        return {"decision": "PASS", "reason": "execution_finalized", "score": judge_report.get("final_score", 10.0)}