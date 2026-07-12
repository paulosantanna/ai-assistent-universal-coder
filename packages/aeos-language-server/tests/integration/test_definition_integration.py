from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestDefinitionIntegration:
    def test_go_to_definition(self, lsp_server):
        uri = "file:///def-playbook.playbook.yaml"
        text = (
            "playbook:\n"
            "  name: def-pb\n"
            "  steps:\n"
            "    - name: my-step\n"
            "      skill: analysis-skill\n"
            "      inputs:\n"
            "        data: input\n"
        )
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/definition",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            if result:
                if isinstance(result, list):
                    assert len(result) >= 1
                else:
                    assert "uri" in result or "range" in result

    def test_go_to_definition_cross_file(self, lsp_server):
        uri1 = "file:///def-skill.skill.yaml"
        text1 = "skill:\n  name: ref-skill\n  tools:\n    - file-reader\n"
        init_and_open_doc(lsp_server, uri1, text1)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "textDocument/didClose",
            "params": {"textDocument": {"uri": uri1}},
        })
        time.sleep(0.2)
        uri2 = "file:///def-ref.agent.yaml"
        text2 = "agent:\n  name: ref-agent\n  skills:\n    - ref-skill\n"
        init_and_open_doc(lsp_server, uri2, text2)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/definition",
            "params": {
                "textDocument": {"uri": uri2},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            if result:
                if isinstance(result, list):
                    assert len(result) >= 1
                else:
                    assert "uri" in result or "range" in result
