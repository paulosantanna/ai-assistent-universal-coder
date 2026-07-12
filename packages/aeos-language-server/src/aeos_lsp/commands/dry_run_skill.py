from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def dry_run_skill(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    skill_ref = args.get("skill_ref", "")
    if not skill_ref:
        return {"error": "Missing 'skill_ref' argument"}

    inputs = args.get("inputs", {})
    logger.info("Dry-running skill: %s", skill_ref)

    try:
        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        symbol = semantic_model.get_symbol_by_id(skill_ref)
        if symbol is None:
            symbols = semantic_model.get_symbols_by_kind(
                getattr(semantic_model.semantic_symbol_kind, "SKILL", None)
            )
            for sym in symbols or []:
                if getattr(sym, "name", "") == skill_ref or skill_ref in getattr(sym, "stable_id", ""):
                    symbol = sym
                    break

        if symbol is None:
            return {"error": f"Skill '{skill_ref}' not found in semantic model"}

        tools = getattr(symbol, "tools", [])
        expected_inputs = getattr(symbol, "inputs", [])
        expected_outputs = getattr(symbol, "outputs", [])
        documentation = getattr(symbol, "documentation", "")
        visibility = getattr(symbol, "visibility", "unknown")

        input_validations = []
        for inp in expected_inputs:
            inp_str = str(inp)
            present = inp_str in inputs
            input_validations.append({
                "name": inp_str,
                "provided": present,
                "status": "ok" if present else "missing",
            })

        missing_inputs = [v["name"] for v in input_validations if v["status"] == "missing"]

        steps = [
            {
                "description": "Load skill definition",
                "inputs_used": list(inputs.keys()) if inputs else [],
            },
            {
                "description": "Resolve tools and dependencies",
                "tools_used": tools,
            },
            {
                "description": "Execute skill logic",
                "inputs_validated": len(expected_inputs),
            },
            {
                "description": "Produce outputs",
                "outputs_produced": expected_outputs,
            },
        ]

        return {
            "skill_ref": skill_ref,
            "name": getattr(symbol, "name", skill_ref),
            "status": "preview",
            "can_execute": len(missing_inputs) == 0,
            "issues": missing_inputs,
            "inputs_validated": input_validations,
            "expected_outputs": expected_outputs,
            "steps": steps,
            "tool_count": len(tools),
            "visibility": str(visibility),
            "documentation": documentation,
            "warnings": [f"Missing required input: {m}" for m in missing_inputs],
        }
    except Exception as exc:
        logger.exception("Failed to dry-run skill %s", skill_ref)
        return {"error": str(exc), "skill_ref": skill_ref}
