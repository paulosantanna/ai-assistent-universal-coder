import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "server.py"


def call(name, arguments=None):
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": arguments or {}}},
    ]
    payload = "".join(json.dumps(item) + "\n" for item in messages)
    completed = subprocess.run([sys.executable, str(SERVER)], input=payload, text=True, capture_output=True, check=True)
    lines = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    result = next(item["result"] for item in lines if item.get("id") == 2)
    return result


class QaExpertTests(unittest.TestCase):
    def test_missing_category_lists_choices(self):
        result = call("plan_checks")
        self.assertFalse(result["isError"])
        body = result["structuredContent"]
        self.assertEqual(body["status"], "needs_category")
        self.assertIn("pyramid", body["categories"])
        self.assertIsNone(body["selected"])

    def test_unsourced_category_has_no_invented_checks(self):
        result = call("plan_checks", {"category": "partition"})
        body = result["structuredContent"]
        self.assertEqual(body["status"], "definition_unavailable")
        self.assertEqual(body["checks"], [])

    def test_sourced_category_keeps_the_read_excerpt(self):
        result = call("get_category", {"id": "llm-rag"})
        body = result["structuredContent"]
        self.assertIn("FP7 Incomplete", body["sources"][0]["excerpt"])
        self.assertIn("oito", body["gap"])

    def test_unknown_tool_fails(self):
        result = call("get_tool", {"id": "nao-existe"})
        self.assertTrue(result["isError"])

    def test_questions_are_not_invented(self):
        result = call("list_questions", {"kind": "release"})
        body = result["structuredContent"]
        self.assertEqual(body["questions"], [])
        self.assertEqual(body["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
