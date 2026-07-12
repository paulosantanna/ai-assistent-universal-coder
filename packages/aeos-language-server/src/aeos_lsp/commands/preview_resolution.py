from __future__ import annotations

import logging
from typing import Any

from lsprotocol.types import Position

logger = logging.getLogger(__name__)


def preview_resolution(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    uri = args.get("uri", "")
    position_raw = args.get("position", {})

    if not uri:
        return {"error": "Missing 'uri' argument"}
    if not position_raw:
        return {"error": "Missing 'position' argument"}

    logger.info("Previewing resolution at %s:%s", uri, position_raw)

    try:
        line = position_raw.get("line", 0)
        character = position_raw.get("character", 0)
        position = Position(line=line, character=character)

        semantic_model = getattr(server, "semantic_model", None)
        if semantic_model is None:
            return {"error": "Semantic model not available"}

        symbol = semantic_model.get_symbol(uri, position)
        if symbol is None:
            return {
                "uri": uri,
                "position": {"line": line, "character": character},
                "resolved": False,
                "message": "No symbol found at this position",
            }

        stable_id = symbol.stable_id
        name = getattr(symbol, "name", stable_id)
        kind = getattr(symbol, "kind", getattr(symbol, "symbol_kind", None))
        kind_name = kind.value if hasattr(kind, "value") else str(kind)

        definitions = semantic_model.get_definitions(uri, position)
        references = semantic_model.get_references(uri, position)

        return {
            "uri": uri,
            "position": {"line": line, "character": character},
            "resolved": True,
            "symbol": {
                "stable_id": stable_id,
                "name": name,
                "kind": kind_name,
                "documentation": getattr(symbol, "documentation", "")[:500],
            },
            "definitions": definitions[:20],
            "references": references[:50],
            "definition_count": len(definitions),
            "reference_count": len(references),
        }
    except Exception as exc:
        logger.exception("Failed to preview resolution at %s", uri)
        return {"error": str(exc), "uri": uri}
