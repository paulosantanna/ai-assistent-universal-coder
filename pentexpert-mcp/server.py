#!/usr/bin/env python3
"""MCP somente leitura de pentest defensivo. Sem payload, comando ou reproducao."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KB = json.loads((ROOT / "knowledge.json").read_text(encoding="utf-8"))
PROTOCOL = "2025-11-25"
READ_ONLY = {"readOnlyHint": True, "openWorldHint": False}
REFUSAL = (
    "Recusado. Este servidor devolve impacto, pergunta de controle, evidencia e correcao. "
    "Nao devolve payload, comando nem reproducao."
)
ATTACK = re.compile(
    r"\b(payloads?|exploits?|pocs?|shellcode|sqlmap)\b|"
    r"\b(reproduz\w*|reproduzir|reproduce|reproduction|reprodu[cç][aã]o)\b|"
    r"\b(comando|command)\b",
    re.IGNORECASE,
)


def schema(properties, required=None):
    return {
        "type": "object",
        "properties": properties,
        "required": required or [],
        "additionalProperties": False,
    }


AUTH = {
    "type": "object",
    "properties": {
        "authorizer": {"type": "string"},
        "scope": {"type": "string"},
        "date": {"type": "string"},
        "rules_of_engagement": {"type": "string"},
    },
    "required": ["authorizer", "scope", "date", "rules_of_engagement"],
    "additionalProperties": False,
}

TOOLS = [
    {
        "name": "plan_assessment",
        "description": "Sem autorizacao escrita devolve so o checklist. Pedido de payload, comando ou reproducao e recusado.",
        "inputSchema": schema({
            "request": {"type": "string"},
            "written_authorization": AUTH,
        }),
        "annotations": READ_ONLY,
    },
    {
        "name": "list_topics",
        "description": "Lista topicos de avaliacao com o estado da fonte. Nao inclui passo de ataque.",
        "inputSchema": schema({}),
        "annotations": READ_ONLY,
    },
    {
        "name": "get_topic",
        "description": "Devolve impacto, pergunta de controle, evidencia e correcao. Nao devolve reproducao.",
        "inputSchema": schema({"id": {"type": "string"}}, ["id"]),
        "annotations": READ_ONLY,
    },
    {
        "name": "list_tools",
        "description": "Lista o proposito das ferramentas citadas, sem modo de uso ofensivo.",
        "inputSchema": schema({}),
        "annotations": READ_ONLY,
    },
    {
        "name": "get_tool",
        "description": "Devolve o proposito lido da fonte oficial. Nao devolve comando.",
        "inputSchema": schema({"id": {"type": "string"}}, ["id"]),
        "annotations": READ_ONLY,
    },
]


def refuse(text):
    return bool(ATTACK.search(text or ""))


def authorized(value):
    if not isinstance(value, dict):
        return False
    needed = ("authorizer", "scope", "date", "rules_of_engagement")
    return all(isinstance(value.get(key), str) and value[key].strip() for key in needed)


def checklist():
    return [{"id": item["id"], "title": item["title"], "status": item["status"]} for item in KB["topics"]]


def plan_assessment(args):
    request = args.get("request") or ""
    if refuse(request):
        raise ValueError(REFUSAL)
    if not authorized(args.get("written_authorization")):
        return {"mode": "checklist_only", "checklist": checklist()}
    return {
        "mode": "authorized_control_review",
        "items": [
            {
                "id": item["id"],
                "title": item["title"],
                "impact": item["impact"],
                "control_question": item["control_question"],
                "evidence": item["evidence"],
                "remediation": item["remediation"],
            }
            for item in KB["topics"]
            if item["status"] == "sourced"
        ],
        "withheld": [item["id"] for item in KB["topics"] if item["status"] != "sourced"],
    }


def list_topics(_args):
    return {"topics": checklist()}


def get_topic(args):
    if refuse(args.get("id")):
        raise ValueError(REFUSAL)
    for item in KB["topics"]:
        if item["id"] == args.get("id"):
            public = {key: item[key] for key in (
                "id", "title", "status", "impact", "control_question", "evidence", "remediation", "sources"
            )}
            return public
    raise ValueError(f"Unknown topic: {args.get('id')}")


def list_tools(_args):
    return {"tools": [{"id": item["id"], "name": item["name"], "status": item["status"]} for item in KB["tools"]]}


def get_tool(args):
    if refuse(args.get("id")):
        raise ValueError(REFUSAL)
    for item in KB["tools"]:
        if item["id"] == args.get("id"):
            return item
    raise ValueError(f"Unknown tool: {args.get('id')}")


HANDLERS = {
    "plan_assessment": plan_assessment,
    "list_topics": list_topics,
    "get_topic": get_topic,
    "list_tools": list_tools,
    "get_tool": get_tool,
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
            "serverInfo": {"name": "pentexpert-mcp", "version": "1.0.0"},
        })
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return _result(number, {})
    if method == "tools/list":
        return _result(number, {"tools": TOOLS})
    if method == "tools/call":
        handler = HANDLERS.get(params.get("name"))
        if handler is None:
            return _error(number, -32602, f"Unknown tool: {params.get('name')}")
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
