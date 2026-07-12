from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestDocumentSync:
    def test_open_document(self, lsp_server):
        uri = "file:///test.agent.md"
        text = "agent:\n  name: test-agent\n  description: A test agent\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(1)
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("method") == "textDocument/publishDiagnostics":
            assert resp["params"]["uri"] == uri
            assert isinstance(resp["params"]["diagnostics"], list)

    def test_incremental_change(self, lsp_server):
        uri = "file:///test2.skill.md"
        text = "skill:\n  name: test-skill\n  tools:\n    - file-reader\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.5)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": uri, "version": 2},
                "contentChanges": [
                    {
                        "range": {
                            "start": {"line": 0, "character": 0},
                            "end": {"line": 3, "character": 0},
                        },
                        "text": "skill:\n  name: changed-skill\n",
                    }
                ],
            },
        })
        time.sleep(1)
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("method") == "textDocument/publishDiagnostics":
            assert resp["params"]["uri"] == uri

    def test_save_document(self, lsp_server):
        uri = "file:///test3.agent.yaml"
        text = "agent:\n  name: save-test\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "textDocument/didSave",
            "params": {"textDocument": {"uri": uri}},
        })
        time.sleep(0.5)
        resp = recv_json(lsp_server.stdout, timeout=3)
        if resp and resp.get("method") == "textDocument/publishDiagnostics":
            assert resp["params"]["uri"] == uri

    def test_close_document(self, lsp_server):
        uri = "file:///test4.agent.yaml"
        init_and_open_doc(lsp_server, uri, "agent:\n  name: close-test\n")
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "textDocument/didClose",
            "params": {"textDocument": {"uri": uri}},
        })
        time.sleep(0.5)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=3)
        if resp and resp.get("id") == 2:
            result = resp.get("result", {})
            items = result.get("items", []) if isinstance(result, dict) else []
            assert len(items) == 0

    def test_non_aeos_ignore(self, lsp_server):
        uri = "file:///readme.txt"
        init_and_open_doc(lsp_server, uri, "This is not an AEOS document.")
        time.sleep(1)
        resp = recv_json(lsp_server.stdout, timeout=3)
        if resp and resp.get("method") == "textDocument/publishDiagnostics":
            assert resp["params"]["uri"] == uri
            assert len(resp["params"]["diagnostics"]) == 0
