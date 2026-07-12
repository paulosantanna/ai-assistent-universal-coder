from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def show_dependency_graph(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    logger.info("Retrieving dependency graph")

    try:
        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        dep_graph = semantic_model.dependency_graph
        nodes = dep_graph.all_nodes()

        uri_filter = args.get("uri")
        stable_id_filter = args.get("stable_id")

        serialized = []
        for node in nodes:
            if uri_filter and node.uri != uri_filter:
                continue
            if stable_id_filter and node.id != stable_id_filter:
                continue
            serialized.append({
                "id": node.id,
                "kind": node.kind.value if hasattr(node.kind, "value") else str(node.kind),
                "uri": node.uri,
                "dependencies": list(node.dependencies),
                "dependents": list(node.dependents),
            })

        has_cycles = dep_graph.has_cycle()

        return {
            "nodes": serialized,
            "node_count": len(serialized),
            "has_cycles": has_cycles,
            "total_nodes": dep_graph.count(),
        }
    except Exception as exc:
        logger.exception("Failed to retrieve dependency graph")
        return {"error": str(exc)}
