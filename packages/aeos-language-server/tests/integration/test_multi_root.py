from __future__ import annotations

import os

from .conftest import send_json, recv_json, lsp_server  # noqa: F401


class TestMultiRoot:
    def test_multi_root_workspace(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "processId": os.getpid(),
                "rootUri": None,
                "capabilities": {"workspace": {"workspaceFolders": True}},
                "workspaceFolders": [
                    {"uri": "file:///workspace1", "name": "Workspace 1"},
                    {"uri": "file:///workspace2", "name": "Workspace 2"},
                ],
            },
        })
        resp = recv_json(lsp_server.stdout, timeout=10)
        assert resp is not None
        assert resp.get("id") == 1
        result = resp.get("result", {})
        caps = result.get("capabilities", {})
        workspace = caps.get("workspace", {})
        wf = workspace.get("workspaceFolders", {}) if isinstance(workspace, dict) else {}
        if wf:
            assert wf.get("supported") == True
            assert wf.get("changeNotifications") == True

    def test_workspace_folder_changes(self, lsp_server):
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "processId": os.getpid(),
                "rootUri": None,
                "capabilities": {"workspace": {"workspaceFolders": True}},
                "workspaceFolders": [
                    {"uri": "file:///initial", "name": "Initial"}
                ],
            },
        })
        recv_json(lsp_server.stdout, timeout=10)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "initialized", "params": None,
        })
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "method": "workspace/didChangeWorkspaceFolders",
            "params": {
                "event": {
                    "added": [{"uri": "file:///added", "name": "Added"}],
                    "removed": [{"uri": "file:///removed", "name": "Removed"}],
                }
            },
        })
        import time
        time.sleep(0.3)
        send_json(lsp_server.stdin, {
            "jsonrpc": "2.0", "id": 2, "method": "workspace/symbol",
            "params": {"query": "test"}
        })
        resp = recv_json(lsp_server.stdout, timeout=5)
        assert resp is not None
        assert resp.get("id") == 2
