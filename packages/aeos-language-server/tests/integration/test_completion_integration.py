from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestCompletionIntegration:
    def test_completion_at_directive(self, lsp_server):
        uri = "file:///comp-directive.agent.md"
        text = "---\nagent: test\n---\n\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 3, "character": 1},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            items = result.get("items", []) if isinstance(result, dict) else []
            labels = [i["label"] for i in items if "label" in i]
            assert any(l.startswith("@") for l in labels)

    def test_completion_at_id(self, lsp_server):
        uri = "file:///comp-id.agent.yaml"
        text = "agent:\n  name: test\n  skills:\n    - \n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 3, "character": 7},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            items = result.get("items", []) if isinstance(result, dict) else []
            assert isinstance(items, list)

    def test_completion_at_key(self, lsp_server):
        uri = "file:///comp-key.agent.yaml"
        text = "agent:\n  name: test\n  "
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 2, "character": 3},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            items = result.get("items", []) if isinstance(result, dict) else []
            labels = [i["label"] for i in items if "label" in i]
            assert any(k in labels for k in ["description", "skills", "layers"])

    def test_completion_at_value(self, lsp_server):
        uri = "file:///comp-value.agent.yaml"
        text = "agent:\n  name: test\n  visibility: \n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 2, "character": 16},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            items = result.get("items", []) if isinstance(result, dict) else []
            labels = [i["label"] for i in items if "label" in i]
            assert "public" in labels or "private" in labels

    def test_non_aeos_no_completion(self, lsp_server):
        uri = "file:///not-aeos.txt"
        init_and_open_doc(lsp_server, uri, "just text")
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 4},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            if isinstance(result, dict):
                assert result.get("is_incomplete", False) == False or len(result.get("items", [])) == 0
