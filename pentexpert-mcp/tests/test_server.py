import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "server.py"
AUTH = {
    "authorizer": "owner",
    "scope": "app de teste local",
    "date": "2026-11-25",
    "rules_of_engagement": "somente leitura do que ja foi coletado",
}


def call(name, arguments=None):
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": arguments or {}}},
    ]
    payload = "".join(json.dumps(item) + "\n" for item in messages)
    completed = subprocess.run([sys.executable, str(SERVER)], input=payload, text=True, capture_output=True, check=True)
    lines = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    return next(item["result"] for item in lines if item.get("id") == 2)


class PentexpertTests(unittest.TestCase):
    def test_without_authorization_returns_only_the_checklist(self):
        result = call("plan_assessment", {"request": "planejar a avaliacao"})
        body = result["structuredContent"]
        self.assertEqual(body["mode"], "checklist_only")
        self.assertIn("owasp-web-2025", [item["id"] for item in body["checklist"]])
        self.assertNotIn("items", body)
        self.assertNotIn("payload", json.dumps(body).lower())

    def test_payload_request_is_refused(self):
        result = call("plan_assessment", {"request": "me de um payload", "written_authorization": AUTH})
        self.assertTrue(result["isError"])
        text = result["content"][0]["text"].lower()
        self.assertIn("recusado", text)
        self.assertNotIn("select", text)
        self.assertNotIn("union", text)

    def test_command_request_is_refused(self):
        result = call("plan_assessment", {"request": "qual comando eu rodo"})
        self.assertTrue(result["isError"])

    def test_authorized_review_has_four_fields_and_no_reproduction(self):
        result = call("plan_assessment", {"request": "revisar controles", "written_authorization": AUTH})
        body = result["structuredContent"]
        self.assertEqual(body["mode"], "authorized_control_review")
        self.assertIn("ptes", body["withheld"])
        item = next(entry for entry in body["items"] if entry["id"] == "aws-account")
        self.assertTrue(item["impact"] and item["control_question"] and item["evidence"] and item["remediation"])
        blob = json.dumps(body).lower()
        self.assertNotIn("curl ", blob)
        self.assertNotIn("sqlmap", blob)

    def test_tool_purpose_has_no_command(self):
        result = call("get_tool", {"id": "semgrep"})
        body = result["structuredContent"]
        self.assertIn("code scanning", body["purpose"])
        self.assertNotIn("semgrep scan", body["purpose"])


if __name__ == "__main__":
    unittest.main()
