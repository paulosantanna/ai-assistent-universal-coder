from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from aeos_lsp.protocol.cancellation import CancellationToken, CancellationManager
from aeos_lsp.protocol.text_sync import PositionEncoding, DebouncedChange


class TestCancellationToken:
    def test_not_cancelled_by_default(self):
        token = CancellationToken()
        assert not token.cancelled

    def test_cancel(self):
        token = CancellationToken()
        token.cancel()
        assert token.cancelled

    def test_on_callback(self):
        callback = MagicMock()
        token = CancellationToken()
        token.on_cancel(callback)
        token.cancel()
        callback.assert_called_once()

    def test_remove_callback(self):
        callback = MagicMock()
        token = CancellationToken()
        token.on_cancel(callback)
        token.remove_callback(callback)
        token.cancel()
        callback.assert_not_called()

    def test_reset(self):
        token = CancellationToken()
        token.cancel()
        assert token.cancelled
        token.reset()
        assert not token.cancelled


class TestCancellationManager:
    @pytest.fixture
    def manager(self) -> CancellationManager:
        return CancellationManager()

    def test_register(self, manager):
        token = manager.register("test-id")
        assert token is not None
        assert not token.cancelled

    def test_get_token(self, manager):
        token1 = manager.register("test-id")
        token2 = manager.get_token("test-id")
        assert token1 is token2

    def test_cancel(self, manager):
        token = manager.register("test-id")
        manager.cancel("test-id")
        assert token.cancelled

    def test_cancel_nonexistent(self, manager):
        result = manager.cancel("nonexistent")
        assert result is False

    def test_cancel_all(self, manager):
        t1 = manager.register("id-1")
        t2 = manager.register("id-2")
        manager.cancel_all()
        assert t1.cancelled
        assert t2.cancelled

    def test_unregister(self, manager):
        manager.register("test-id")
        manager.unregister("test-id")
        assert manager.get_token("test-id") is None


class TestPositionEncoding:
    def test_enum_values(self):
        assert PositionEncoding.UTF16.value == "utf-16"
        assert PositionEncoding.UTF8.value == "utf-8"
        assert PositionEncoding.UTF32.value == "utf-32"


class TestDebouncedChange:
    @pytest.fixture
    def debouncer(self) -> DebouncedChange:
        return DebouncedChange(delay_ms=100)

    def test_initialization(self, debouncer):
        assert debouncer is not None

    def test_debounce(self, debouncer):
        callback = MagicMock()
        debouncer.debounce("file:///test.yaml", callback)
        assert debouncer.pending_count > 0

    def test_cancel_pending(self, debouncer):
        debouncer.debounce("file:///test.yaml", MagicMock())
        debouncer.cancel_pending("file:///test.yaml")
        assert debouncer.pending_count == 0

    def test_cancel_pending_all(self, debouncer):
        debouncer.debounce("file:///a.yaml", MagicMock())
        debouncer.debounce("file:///b.yaml", MagicMock())
        debouncer.cancel_pending()
        assert debouncer.pending_count == 0
