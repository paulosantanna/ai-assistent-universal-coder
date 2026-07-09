from __future__ import annotations

from typing import Any, Optional


class ContextRouter:
    def __init__(self, lcp_resolver=None, memory_gateway=None):
        self.lcp_resolver = lcp_resolver
        self.memory_gateway = memory_gateway

    def build_context_packet(self, execution_id: str, task: dict[str, Any]) -> dict[str, Any]:
        lcps = self._resolve_lcps(task.get("required_lcps", []))
        memory_refs = self._query_memory(task.get("scope", {}))

        return {
            "context_id": f"{execution_id}:{task.get('task_id')}",
            "task_id": task.get("task_id"),
            "agent_id": task.get("assigned_agent") or task.get("agent_id"),
            "loaded_lcps": lcps,
            "memory_refs": memory_refs,
            "file_refs": task.get("required_context", task.get("context_refs", [])),
            "evidence_refs": task.get("required_evidence", task.get("evidence_refs", [])),
            "rules": [],
            "forbidden_actions": task.get("forbidden_actions", []),
            "quality_gates": task.get("quality_gates", []),
        }

    def limit_context(self, context: dict[str, Any], max_size_bytes: int = 100000) -> dict[str, Any]:
        result = dict(context)
        if "loaded_lcps" in result:
            result["loaded_lcps"] = result["loaded_lcps"][:5]
        if "file_refs" in result:
            result["file_refs"] = result["file_refs"][:10]
        if "evidence_refs" in result:
            result["evidence_refs"] = result["evidence_refs"][:20]
        return result

    def _resolve_lcps(self, lcp_ids: list[str]) -> list[dict[str, Any]]:
        if self.lcp_resolver and hasattr(self.lcp_resolver, "resolve"):
            return self.lcp_resolver.resolve(lcp_ids)
        return [{"lcp_id": lid, "resolved": False} for lid in lcp_ids]

    def _query_memory(self, scope: dict[str, Any]) -> list[dict[str, Any]]:
        if self.memory_gateway and hasattr(self.memory_gateway, "query_refs"):
            return self.memory_gateway.query_refs(scope)
        return []
