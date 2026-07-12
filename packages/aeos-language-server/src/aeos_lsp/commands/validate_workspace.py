from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


def validate_workspace(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    logger.info("Validating entire workspace")

    try:
        workspace = getattr(server, "workspace_manager", None)
        if workspace is None:
            return {"error": "Workspace manager not available"}

        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        config = getattr(server, "config", None)

        engine = getattr(server, "diagnostics_engine", None)
        if engine is None:
            return {"error": "Diagnostics engine not available"}

        start = time.monotonic()
        result = engine.run_workspace_diagnostics(
            workspace=workspace,
            semantic_model=semantic_model,
            config=config,
        )
        elapsed = time.monotonic() - start

        file_count = len(result.diagnostics)
        total_count = result.total_count

        return {
            "elapsed_ms": round(elapsed * 1000, 2),
            "files_with_diagnostics": file_count,
            "total_diagnostics": total_count,
            "errors": result.errors_count,
            "warnings": result.warnings_count,
            "informations": result.informations_count,
            "hints": result.hints_count,
            "cancelled": result.cancelled,
            "result_ids": result.result_ids,
        }
    except Exception as exc:
        logger.exception("Failed to validate workspace")
        return {"error": str(exc)}
