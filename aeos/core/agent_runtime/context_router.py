class ContextRouter:
    """
    Resolves minimal context packets for each task.

    This skeleton does not load raw repository content directly.
    It should use ToolRouter/File refs and LCP Resolver.
    """

    def __init__(self, lcp_resolver, memory_gateway):
        self.lcp_resolver = lcp_resolver
        self.memory_gateway = memory_gateway

    def build_context_packet(self, execution_id: str, task: dict) -> dict:
        lcps = self.lcp_resolver.resolve(task.get("required_lcps", []))
        memory_refs = self.memory_gateway.query_refs(task.get("scope", {}))

        return {
            "context_id": f"{execution_id}:{task.get('task_id')}",
            "task_id": task.get("task_id"),
            "agent_id": task.get("assigned_agent"),
            "loaded_lcps": lcps,
            "memory_refs": memory_refs,
            "file_refs": task.get("required_context", []),
            "evidence_refs": task.get("required_evidence", []),
            "rules": [],
            "forbidden_actions": task.get("forbidden_actions", []),
            "quality_gates": task.get("quality_gates", []),
        }
