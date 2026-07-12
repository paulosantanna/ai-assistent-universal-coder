from __future__ import annotations

import logging
import threading
import time
from typing import Any

logger = logging.getLogger(__name__)


def refresh_index(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    logger.info("Rebuilding index")

    try:
        indexer = getattr(server, "indexer", None)
        if indexer is None:
            return {"error": "Indexer not available"}

        workspace = getattr(server, "workspace_manager", None)
        if workspace is None:
            return {"error": "Workspace manager not available"}

        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        def _rebuild() -> dict[str, Any]:
            start = time.monotonic()
            try:
                indexer.build_full_index(
                    workspace_manager=workspace,
                    semantic_model=semantic_model,
                )
                elapsed = time.monotonic() - start
                return {
                    "status": "completed",
                    "elapsed_ms": round(elapsed * 1000, 2),
                    "indexed_count": indexer.get_indexed_count(),
                    "failed_count": indexer.get_failed_count(),
                }
            except Exception as exc:
                logger.exception("Index rebuild failed")
                return {"status": "failed", "error": str(exc)}

        rebuild_type = args.get("mode", "sync")
        if rebuild_type == "async":
            thread = threading.Thread(target=_rebuild, daemon=True, name="aeos-index-rebuild")
            thread.start()
            return {"status": "started", "mode": "async"}

        return _rebuild()
    except Exception as exc:
        logger.exception("Failed to refresh index")
        return {"error": str(exc)}
