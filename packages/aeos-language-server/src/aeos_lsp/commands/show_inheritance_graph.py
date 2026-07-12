from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def show_inheritance_graph(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    logger.info("Retrieving inheritance graph")

    try:
        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        inher_graph = semantic_model.inheritance_graph

        uri_filter = args.get("uri")
        stable_id_filter = args.get("stable_id")

        all_relationships = inher_graph.all_relationships()

        if uri_filter:
            all_relationships = [
                (c, p) for c, p in all_relationships
                if uri_filter in c or uri_filter in p
            ]

        if stable_id_filter:
            all_relationships = [
                (c, p) for c, p in all_relationships
                if stable_id_filter in c or stable_id_filter in p
            ]

        roots = inher_graph.get_roots()
        leaves = inher_graph.get_leaves()
        has_cycles = inher_graph.has_cycle()

        return {
            "relationships": [
                {"child": child, "parent": parent}
                for child, parent in all_relationships
            ],
            "relationship_count": len(all_relationships),
            "roots": roots,
            "leaves": leaves,
            "has_cycles": has_cycles,
            "node_count": inher_graph.count(),
        }
    except Exception as exc:
        logger.exception("Failed to retrieve inheritance graph")
        return {"error": str(exc)}
