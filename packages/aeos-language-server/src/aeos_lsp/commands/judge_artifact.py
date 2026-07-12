from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


def judge_artifact(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    uri = args.get("uri", "")
    if not uri:
        return {"error": "Missing 'uri' argument"}

    logger.info("Running Judge evaluation on artifact: %s", uri)

    try:
        workspace = getattr(server, "workspace_manager", None)
        if workspace is None:
            return {"error": "Workspace manager not available"}

        doc = workspace.document_store.get(uri) if hasattr(workspace, "document_store") else None
        if doc is None:
            return {"error": "Document not found", "uri": uri}

        text = doc.text if hasattr(doc, "text") else ""

        config = getattr(server, "config", None)
        judge_gates = None
        if config is not None:
            judge_gates = getattr(config, "judge_gates", None)

        results: list[dict[str, Any]] = []
        start = time.monotonic()

        quality_checks = {
            "has_description": {
                "description_missing": "description" not in text.lower()[:200],
            },
            "has_documentation": {
                "documentation_missing": "documentation" not in text.lower()[:300],
            },
            "has_references": {
                "references_missing": "references" not in text.lower()[:500],
            },
            "has_stable_id": {
                "stable_id_missing": "stable_id" not in text,
            },
            "has_version": {
                "version_missing": "version" not in text.lower()[:200],
            },
        }

        for check_name, check_results in quality_checks.items():
            passed = not any(check_results.values())
            results.append({
                "check": check_name,
                "passed": passed,
                "details": check_results,
            })

        if judge_gates is not None and hasattr(judge_gates, "__iter__"):
            for gate in judge_gates:
                gate_check = _evaluate_gate(gate, text)
                results.append(gate_check)

        elapsed = time.monotonic() - start

        passed_count = sum(1 for r in results if r["passed"])
        failed_count = sum(1 for r in results if not r["passed"])

        return {
            "uri": uri,
            "passed": failed_count == 0,
            "score": round(passed_count / max(1, len(results)), 4),
            "checks_passed": passed_count,
            "checks_failed": failed_count,
            "total_checks": len(results),
            "elapsed_ms": round(elapsed * 1000, 2),
            "results": results,
        }
    except Exception as exc:
        logger.exception("Failed to judge artifact %s", uri)
        return {"error": str(exc), "uri": uri}


def _evaluate_gate(gate: Any, text: str) -> dict[str, Any]:
    gate_name = gate if isinstance(gate, str) else getattr(gate, "name", "unknown")
    rule_text = gate if isinstance(gate, str) else getattr(gate, "rule", "")
    min_score = getattr(gate, "min_score", 0.0) if not isinstance(gate, str) else 0.0

    present = rule_text.lower() in text.lower() if rule_text else True
    passed = present

    return {
        "check": f"gate:{gate_name}",
        "passed": passed,
        "details": {
            "rule": rule_text,
            "min_score": min_score,
            "rule_present": present,
        },
    }
