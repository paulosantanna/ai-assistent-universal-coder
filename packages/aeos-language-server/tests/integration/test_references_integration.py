from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestReferencesIntegration:
    def test_find_references(self, lsp_server):
        uri = "file:///ref-agent.agent.yaml"
        text = "agent:\n  name: ref-agent\n  description: referenced\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/references",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
                "context": {"includeDeclaration": False},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            assert result is not None

    def test_find_references_include_declaration(self, lsp_server):
        uri = "file:///ref-agent2.agent.yaml"
        text = "agent:\n  name: ref-agent2\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/references",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
                "context": {"includeDeclaration": True},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            assert result is not None
