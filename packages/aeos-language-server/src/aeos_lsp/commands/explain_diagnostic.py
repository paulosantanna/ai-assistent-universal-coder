from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

_KNOWN_DIAGNOSTIC_CODES: dict[str, dict[str, str]] = {
    "AEOS001": {
        "title": "Missing Required Field",
        "severity": "Error",
        "description": "A required field is missing from the AEOS document. Add the missing field with an appropriate value.",
        "remediation": "Check the schema definition for required fields and ensure all are present.",
    },
    "AEOS002": {
        "title": "Invalid Reference",
        "severity": "Error",
        "description": "A reference to another AEOS entity (agent, skill, playbook, tool) could not be resolved.",
        "remediation": "Verify that the referenced entity exists, is spelled correctly, and is registered in the appropriate registry.",
    },
    "AEOS003": {
        "title": "Schema Validation Error",
        "severity": "Error",
        "description": "The document content does not conform to the expected AEOS schema.",
        "remediation": "Review the schema definition and fix type mismatches, missing fields, or structural issues.",
    },
    "AEOS004": {
        "title": "Deprecated Entity Reference",
        "severity": "Warning",
        "description": "The document references an entity that has been marked as deprecated.",
        "remediation": "Update the reference to use the replacement entity specified in the deprecation notice.",
    },
    "AEOS005": {
        "title": "Circular Dependency Detected",
        "severity": "Error",
        "description": "A circular dependency exists between AEOS entities, which will cause resolution failures at runtime.",
        "remediation": "Break the cycle by removing or restructuring dependencies between the affected entities.",
    },
    "AEOS006": {
        "title": "Unsafe Tool Usage",
        "severity": "Warning",
        "description": "The tool is marked as unsafe or uses patterns that may be restricted by security policies.",
        "remediation": "Review the tool configuration and ensure it complies with the workspace security policy.",
    },
    "AEOS007": {
        "title": "Token Budget Exceeded",
        "severity": "Warning",
        "description": "The estimated token usage exceeds the configured token budget for the agent or model profile.",
        "remediation": "Increase the token budget, reduce the model complexity, or split the operation into smaller steps.",
    },
    "AEOS008": {
        "title": "Missing Rollback Definition",
        "severity": "Warning",
        "description": "A step with approval required or mutating tool is missing a rollback definition.",
        "remediation": "Add a rollback plan for the step to ensure safe recovery on failure.",
    },
    "AEOS009": {
        "title": "Unresolved Import",
        "severity": "Error",
        "description": "The document imports or references a file, entity, or module that cannot be found.",
        "remediation": "Ensure the referenced import path exists and is accessible from the current workspace.",
    },
    "AEOS010": {
        "title": "Permission Scope Violation",
        "severity": "Error",
        "description": "The operation requires a permission scope that is not granted.",
        "remediation": "Add the required permission scope to the permissions configuration.",
    },
}


def explain_diagnostic(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    code = args.get("code", "")
    if not code:
        return {"error": "Missing 'code' argument"}

    logger.info("Explaining diagnostic code: %s", code)

    known = _KNOWN_DIAGNOSTIC_CODES.get(code)
    if known is not None:
        return {
            "code": code,
            "found": True,
            "title": known["title"],
            "severity": known["severity"],
            "description": known["description"],
            "remediation": known["remediation"],
        }

    engine = getattr(server, "diagnostics_engine", None)
    if engine is not None:
        registry = getattr(engine, "registry", None)
        if registry is not None:
            rule = registry.get_rule(code)
            if rule is not None:
                meta = rule.metadata
                return {
                    "code": code,
                    "found": True,
                    "title": getattr(meta, "title", getattr(meta, "code", code)),
                    "severity": getattr(meta, "severity", "unknown"),
                    "description": getattr(meta, "description", ""),
                    "remediation": getattr(meta, "remediation", getattr(meta, "help", "")),
                }

    return {
        "code": code,
        "found": False,
        "title": "Unknown diagnostic code",
        "description": f"No explanation available for diagnostic code '{code}'.",
        "remediation": "Refer to the AEOS documentation for diagnostic code definitions.",
    }
