from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def dry_run_playbook(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    playbook_ref = args.get("playbook_ref", "")
    if not playbook_ref:
        return {"error": "Missing 'playbook_ref' argument"}

    inputs = args.get("inputs", {})
    logger.info("Dry-running playbook: %s", playbook_ref)

    try:
        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        symbol = semantic_model.get_symbol_by_id(playbook_ref)
        if symbol is None:
            symbols = semantic_model.get_symbols_by_kind(
                getattr(semantic_model.semantic_symbol_kind, "PLAYBOOK", None)
            )
            for sym in symbols or []:
                if getattr(sym, "name", "") == playbook_ref or playbook_ref in getattr(sym, "stable_id", ""):
                    symbol = sym
                    break

        if symbol is None:
            return {"error": f"Playbook '{playbook_ref}' not found in semantic model"}

        steps_raw = getattr(symbol, "steps", [])
        variables = getattr(symbol, "variables", [])
        documentation = getattr(symbol, "documentation", "")
        visibility = getattr(symbol, "visibility", "unknown")

        step_details = []
        total_approvals_needed = 0
        has_rollback = False

        for i, step_ref in enumerate(steps_raw):
            step_sym = semantic_model.get_symbol_by_id(step_ref) if isinstance(step_ref, str) else None
            if step_sym is None:
                step_info = {
                    "index": i,
                    "reference": step_ref,
                    "type": "unknown",
                    "resolved": False,
                }
            else:
                step_tool = getattr(step_sym, "tool", None)
                step_skill = getattr(step_sym, "skill", None)
                needs_approval = getattr(step_sym, "approval", False)
                has_rollback_def = getattr(step_sym, "rollback", None) is not None
                step_timeout = getattr(step_sym, "timeout", None)
                step_retry = getattr(step_sym, "retry", None)

                if needs_approval:
                    total_approvals_needed += 1
                if has_rollback_def:
                    has_rollback = True

                step_info = {
                    "index": i,
                    "reference": step_ref,
                    "name": getattr(step_sym, "name", f"step_{i}"),
                    "type": getattr(step_sym, "step_type", "unknown"),
                    "resolved": True,
                    "tool": step_tool,
                    "skill": step_skill,
                    "approval_required": needs_approval,
                    "has_rollback": has_rollback_def,
                    "timeout": step_timeout,
                    "retry": step_retry,
                }
            step_details.append(step_info)

        return {
            "playbook_ref": playbook_ref,
            "name": getattr(symbol, "name", playbook_ref),
            "status": "preview",
            "steps": step_details,
            "step_count": len(step_details),
            "variables": variables,
            "total_approvals_needed": total_approvals_needed,
            "has_rollback": has_rollback,
            "visibility": str(visibility),
            "documentation": documentation,
        }
    except Exception as exc:
        logger.exception("Failed to dry-run playbook %s", playbook_ref)
        return {"error": str(exc), "playbook_ref": playbook_ref}
