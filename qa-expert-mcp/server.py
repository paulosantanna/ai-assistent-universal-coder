#!/usr/bin/env python3
"""MCP somente leitura de QA. Não consulta rede e não inventa definição."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KB = json.loads((ROOT / "knowledge.json").read_text(encoding="utf-8"))
PROTOCOL = "2025-11-25"

READ_ONLY = {"readOnlyHint": True, "openWorldHint": False}


def schema(properties, required=None):
    return {
        "type": "object",
        "properties": properties,
        "required": required or [],
        "additionalProperties": False,
    }


TOOLS = [
    {
        "name": "list_categories",
        "description": "Lista categorias de teste com o estado da fonte. Nao escolhe uma categoria.",
        "inputSchema": schema({}),
        "annotations": READ_ONLY,
    },
    {
        "name": "get_category",
        "description": "Devolve uma categoria e as fontes ja lidas. Id desconhecido falha.",
        "inputSchema": schema({"id": {"type": "string"}}, ["id"]),
        "annotations": READ_ONLY,
    },
    {
        "name": "list_tools",
        "description": "Lista ferramentas de teste com quando, onde, por que e como, sem linha de comando.",
        "inputSchema": schema({}),
        "annotations": READ_ONLY,
    },
    {
        "name": "get_tool",
        "description": "Detalha uma ferramenta de teste a partir da pagina oficial ja lida.",
        "inputSchema": schema({"id": {"type": "string"}}, ["id"]),
        "annotations": READ_ONLY,
    },
    {
        "name": "plan_checks",
        "description": "Sem categoria, devolve so a lista para o operador escolher. Com categoria sem fonte, nao inventa checks.",
        "inputSchema": schema({"category": {"type": "string"}}),
        "annotations": READ_ONLY,
    },
    {
        "name": "list_questions",
        "description": "Perguntas de refinamento ou release somente quando ha fonte. Caso contrario, recusa inventar.",
        "inputSchema": schema({"kind": {"type": "string"}}, ["kind"]),
        "annotations": READ_ONLY,
    },
]


def find(items, item_id, label):
    for item in items:
        if item["id"] == item_id:
            return item
    raise ValueError(f"Unknown {label}: {item_id}")


def list_categories(_args):
    return {
        "categories": [
            {"id": item["id"], "name": item["name"], "status": item["status"]}
            for item in KB["categories"]
        ]
    }


def get_category(args):
    return find(KB["categories"], args.get("id"), "category")


def list_tools(_args):
    return {
        "tools": [
            {"id": item["id"], "name": item["name"], "status": item["status"]}
            for item in KB["tools"]
        ]
    }


def get_tool(args):
    return find(KB["tools"], args.get("id"), "tool")


def plan_checks(args):
    category = (args.get("category") or "").strip()
    if not category:
        return {
            "status": "needs_category",
            "selected": None,
            "categories": [item["id"] for item in KB["categories"]],
        }
    item = find(KB["categories"], category, "category")
    if item["status"] != "sourced" or not item.get("checks"):
        return {"status": "definition_unavailable", "category": item["id"], "checks": []}
    return {
        "status": "checklist",
        "category": item["id"],
        "checks": item["checks"],
        "sources": item["sources"],
    }


def list_questions(args):
    kind = args.get("kind")
    entry = KB["questions"].get(kind)
    if entry is None:
        raise ValueError("Unknown question kind. Use refinement or release.")
    if entry["status"] != "sourced":
        return {"status": "unavailable", "kind": kind, "reason": entry["reason"], "questions": []}
    return entry


HANDLERS = {
    "list_categories": list_categories,
    "get_category": get_category,
    "list_tools": list_tools,
    "get_tool": get_tool,
    "plan_checks": plan_checks,
    "list_questions": list_questions,
}


def handle(message):
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or "method" not in message:
        return _error(message.get("id") if isinstance(message, dict) else None, -32600, "Invalid Request")
    method = message["method"]
    number = message.get("id")
    params = message.get("params") or {}
    if method == "initialize":
        return _result(number, {
            "protocolVersion": PROTOCOL,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "qa-expert-mcp", "version": "1.0.0"},
        })
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return _result(number, {})
    if method == "tools/list":
        return _result(number, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            return _error(number, -32602, f"Unknown tool: {name}")
        try:
            payload = handler(params.get("arguments") or {})
        except (KeyError, TypeError, ValueError) as exc:
            return _result(number, {"content": [{"type": "text", "text": str(exc)}], "isError": True})
        return _result(number, {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
            "structuredContent": payload,
            "isError": False,
        })
    if number is None:
        return None
    return _error(number, -32601, f"Method not found: {method}")


def _result(number, result):
    return {"jsonrpc": "2.0", "id": number, "result": result}


def _error(number, code, message):
    return {"jsonrpc": "2.0", "id": number, "error": {"code": code, "message": message}}


def serve():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            response = _error(None, -32700, "Parse error")
        else:
            response = handle(message)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    serve()
