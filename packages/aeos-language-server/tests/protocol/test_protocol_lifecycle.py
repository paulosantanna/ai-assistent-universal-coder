from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from lsprotocol.types import (
    INITIALIZE,
    INITIALIZED,
    SHUTDOWN,
    EXIT,
    ClientCapabilities,
    ClientInfo,
    InitializeParams,
    InitializeResult,
    ServerCapabilities,
    ServerInfo,
    TextDocumentSyncKind,
)

from aeos_lsp.protocol.lifecycle import (
    AEOSLifecycleManager,
    AEOSInitializeResult,
    register_lifecycle_handlers,
)
from aeos_lsp.protocol.text_sync import PositionEncoding


@pytest.fixture
def mock_ls():
    ls = MagicMock()
    ls.protocol.fm.add_builtin_feature = MagicMock()
    return ls


@pytest.fixture
def manager(mock_ls):
    m = AEOSLifecycleManager(mock_ls)
    return m


class TestProtocolLifecycle:
    def test_initialize_minimal(self, manager):
        params = InitializeParams(
            process_id=1234,
            capabilities=ClientCapabilities(),
        )
        result = manager.handle_initialize(params)
        assert isinstance(result, AEOSInitializeResult)
        assert result.server_info.name == "aeos-lsp"
        assert result.capabilities is not None

    def test_initialize_full(self, manager):
        params = InitializeParams(
            process_id=1234,
            client_info=ClientInfo(name="test-client", version="1.0"),
            root_uri="file:///workspace",
            capabilities=ClientCapabilities(),
            workspace_folders=[
                {"uri": "file:///ws1", "name": "WS1"},
                {"uri": "file:///ws2", "name": "WS2"},
            ],
            initialization_options={"enableExperimentalFeatures": True},
        )
        result = manager.handle_initialize(params)
        assert result.position_encoding == PositionEncoding.UTF16
        assert len(result.experimental_features) > 0

    def test_initialized_notification(self, manager):
        with patch.object(manager, "_start_background_indexing") as mock_bg:
            manager.handle_initialized()
            assert manager.initialized is True
            mock_bg.assert_called_once()

    def test_shutdown_then_exit(self, manager):
        manager.handle_shutdown()
        assert manager.shutting_down is True
        assert manager._shutdown_complete.is_set()
        manager.handle_exit()

    def test_exit_without_shutdown(self, manager):
        manager.handle_exit()
        assert manager.shutting_down is True

    def test_double_initialize(self, manager):
        params = InitializeParams(
            process_id=1234,
            capabilities=ClientCapabilities(),
        )
        result1 = manager.handle_initialize(params)
        assert result1 is not None
        result2 = manager.handle_initialize(params)
        assert result2 is not None

    def test_double_shutdown(self, manager):
        manager.handle_shutdown()
        assert manager.shutting_down is True
        manager.handle_shutdown()
        assert manager.shutting_down is True

    def test_register_lifecycle_handlers(self, mock_ls, manager):
        register_lifecycle_handlers(mock_ls, manager)
        calls = mock_ls.protocol.fm.add_builtin_feature.call_args_list
        methods = [call[0][0] for call in calls]
        assert INITIALIZE in methods
        assert INITIALIZED in methods
        assert SHUTDOWN in methods
        assert EXIT in methods
