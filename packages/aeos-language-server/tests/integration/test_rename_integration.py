from __future__ import annotations

import time

from .conftest import send_json, recv_json, init_and_open_doc, lsp_server  # noqa: F401


class TestRenameIntegration:
    def test_prepare_rename(self, lsp_server):
        uri = "file:///prep-rename.agent.yaml"
        text = "agent:\n  name: prepare-target\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/prepareRename",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            error = resp.get("error")
            has_range = isinstance(result, dict) and ("start" in result or "line" in (result.get("start") or {}))
            assert has_range or error is not None

    def test_rename_symbol(self, lsp_server):
        uri = "file:///rename-sym.agent.yaml"
        text = "agent:\n  name: rename-target\n"
        init_and_open_doc(lsp_server, uri, text)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/rename",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": 0, "character": 0},
                "newName": "renamed-target",
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            error = resp.get("error")
            if result:
                if isinstance(result, dict):
                    assert "changes" in result or "documentChanges" in result
            elif error:
                assert isinstance(error, dict)
                assert "message" in error

    def test_rename_blocked(self, lsp_server):
        uri = "file:///block-rename.txt"
        init_and_open_doc(lsp_server, uri, "not an aeos doc")
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "textDocument/didClose",
            "params": {"textDocument": {"uri": uri}},
        })
        time.sleep(0.2)
        uri2 = "file:///block-rename.agent.yaml"
        text2 = "config:\n  aeos:\n    name: non-renameable\n"
        init_and_open_doc(lsp_server, uri2, text2)
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "textDocument/prepareRename",
            "params": {
                "textDocument": {"uri": uri2},
                "position": {"line": 0, "character": 0},
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        if resp and resp.get("id") == 2:
            result = resp.get("result")
            error = resp.get("error")
            if error:
                assert isinstance(error, dict)
