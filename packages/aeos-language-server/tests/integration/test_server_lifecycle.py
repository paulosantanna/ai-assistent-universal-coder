from __future__ import annotations

import os

from .conftest import send_json, recv_json, lsp_server  # noqa: F401


class TestServerLifecycle:
    def test_server_start_stdio(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"processId": os.getpid(), "capabilities": {}},
        })
        resp = recv_json(lsp_server.stdout, timeout=15)
        assert resp is not None
        assert resp["id"] == 1
        assert "result" in resp
        assert resp["result"]["serverInfo"]["name"] == "aeos-lsp"

    def test_server_initialize(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"processId": os.getpid(), "rootUri": None, "capabilities": {}},
        })
        resp = recv_json(lsp_server.stdout, timeout=15)
        assert resp is not None
        assert resp["id"] == 1
        result = resp["result"]
        caps = result["capabilities"]
        assert "textDocumentSync" in caps
        assert "completionProvider" in caps
        assert "hoverProvider" in caps
        assert "definitionProvider" in caps
        assert "referencesProvider" in caps
        assert "renameProvider" in caps
        assert result["serverInfo"]["name"] == "aeos-lsp"

    def test_server_shutdown(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "shutdown",
        })
        resp = recv_json(lsp_server.stdout, timeout=10)
        assert resp is not None
        assert resp.get("id") == 2
        assert "result" in resp
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "exit",
        })
        import time
        time.sleep(0.5)
        assert lsp_server.poll() is not None

    def test_server_no_orphan_process(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 3, "method": "initialize",
            "params": {"processId": os.getpid(), "rootUri": None, "capabilities": {}},
        })
        recv_json(lsp_server.stdout, timeout=10)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 4, "method": "shutdown",
        })
        recv_json(lsp_server.stdout, timeout=10)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "exit",
        })
        import time
        time.sleep(1)
        assert lsp_server.poll() == 0
