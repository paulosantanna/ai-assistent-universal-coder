from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import CANCEL_REQUEST, CancelParams

from aeos_lsp.protocol.cancellation import (
    CancellationToken,
    CancellationManager,
    _handle_cancel_request,
    register_cancellation_handlers,
)


@pytest.fixture
def manager():
    return CancellationManager()


class TestProtocolCancellation:
    def test_cancel_request(self, manager):
        token = manager.register("test-op")
        assert not token.cancelled
        manager.cancel("test-op")
        assert token.cancelled

    def test_cancel_nonexistent(self, manager):
        result = manager.cancel("nonexistent-op")
        assert result is False

    def test_cancellation_during_index(self, manager):
        token = manager.register("index-op")
        cancel_callbacks = []
        token.on_cancel(lambda: cancel_callbacks.append("cancelled"))
        manager.cancel("index-op")
        assert len(cancel_callbacks) == 1
        assert cancel_callbacks[0] == "cancelled"

    def test_handle_cancel_request(self):
        ls = MagicMock()
        params = CancelParams(id=42)
        cm = CancellationManager()
        cm.register("42")
        with pytest.MonkeyPatch().context() as mp:
            import aeos_lsp.protocol.cancellation as mod
            mp.setattr(mod, "cancellation_manager", cm)
            _handle_cancel_request(ls, params)

    def test_cancel_all(self, manager):
        t1 = manager.register("op1")
        t2 = manager.register("op2")
        manager.cancel_all()
        assert t1.cancelled
        assert t2.cancelled
        assert len(manager._operations) == 0

    def test_unregister(self, manager):
        manager.register("op")
        assert manager.get_token("op") is not None
        manager.unregister("op")
        assert manager.get_token("op") is None

    def test_register_cancellation_handlers(self):
        ls = MagicMock()
        ls.protocol.fm.add_builtin_feature = MagicMock()
        register_cancellation_handlers(ls)
        ls.protocol.fm.add_builtin_feature.assert_called_once_with(
            CANCEL_REQUEST, _handle_cancel_request
        )
