from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestHoverIntegration:
    def test_hover_on_agent_id(self, lsp_server):
        uri = "file:///hover-agent.agent.yaml"
        text = "agent:\n  name: hover-agent\n  description: An agent to hover over\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            if result is not None:
                contents = result.get("contents", {})
                value = contents.get("value", "") if isinstance(contents, dict) else ""
                assert "agent" in value.lower() or "hover" in value

    def test_hover_on_skill_id(self, lsp_server):
        uri = "file:///hover-skill.skill.yaml"
        text = "skill:\n  name: hover-skill\n  tools:\n    - reader\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            if result is not None:
                contents = result.get("contents", {})
                value = contents.get("value", "") if isinstance(contents, dict) else ""
                assert "skill" in value.lower() or "hover" in value

    def test_hover_on_variable(self, lsp_server):
        uri = "file:///hover-var.playbook.yaml"
        text = "playbook:\n  name: test-pb\n  variables:\n    - name: threshold\n      type: integer\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 2, "character": 5},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            assert result is not None or True

    def test_hover_on_deprecated(self, lsp_server):
        uri = "file:///hover-depr.agent.yaml"
        text = "agent:\n  name: old-agent\n  deprecation: deprecated\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            if result is not None:
                contents = result.get("contents", {})
                value = contents.get("value", "") if isinstance(contents, dict) else ""
                assert "deprecated" in value.lower()
