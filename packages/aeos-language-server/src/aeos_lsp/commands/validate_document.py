from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def validate_document(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    uri = args.get("uri", "")
    if not uri:
        return {"error": "Missing 'uri' argument", "uri": uri}

    logger.info("Validating document: %s", uri)

    try:
        workspace = getattr(server, "workspace_manager", None)
        if workspace is None:
            return {"error": "Workspace manager not available", "uri": uri}

        doc = workspace.document_store.get(uri) if hasattr(workspace, "document_store") else None
        if doc is None:
            return {"error": "Document not found in store", "uri": uri}

        text = doc.text if hasattr(doc, "text") else ""

        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available", "uri": uri}

        config = getattr(server, "config", None)

        engine = getattr(server, "diagnostics_engine", None)
        if engine is None:
            return {"error": "Diagnostics engine not available", "uri": uri}

        result = engine.run_document_diagnostics(
            uri=uri,
            text=text,
            semantic_model=semantic_model,
            config=config,
            workspace=workspace,
        )

        diag_list = result.diagnostics.get(uri, [])
        formatted = [
            {
                "range": {
                    "start": {"line": d.range.start.line, "character": d.range.start.character},
                    "end": {"line": d.range.end.line, "character": d.range.end.character},
                },
                "severity": d.severity.value if hasattr(d.severity, "value") else d.severity,
                "code": d.code,
                "message": d.message,
                "source": d.source,
            }
            for d in diag_list
        ]

        return {
            "uri": uri,
            "diagnostics": formatted,
            "total": result.total_count,
            "errors": result.errors_count,
            "warnings": result.warnings_count,
            "informations": result.informations_count,
            "hints": result.hints_count,
        }
    except Exception as exc:
        logger.exception("Failed to validate document %s", uri)
        return {"error": str(exc), "uri": uri}
