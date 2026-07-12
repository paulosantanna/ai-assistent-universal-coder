from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    Position,
    Range,
    TextDocumentContentChangePartial,
    TextDocumentContentChangeWholeDocument,
    TextDocumentIdentifier,
    TextDocumentItem,
    VersionedTextDocumentIdentifier,
)

from aeos_lsp.protocol.errors import AEOSErrorCodes, JsonRpcError
from aeos_lsp.protocol.text_sync import (
    DebouncedChange,
    PositionEncoding,
    TextSynchronizer,
)


@pytest.fixture
def text_sync():
    ls = MagicMock()
    return TextSynchronizer(ls, debounce_ms=100)


class TestProtocolTextSync:
    def test_did_open(self, text_sync):
        params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri="file:///test.yaml",
                language_id="aeos",
                version=1,
                text="agent:\n  name: test\n",
            ),
        )
        text_sync.handle_open(params)
        assert text_sync.is_open("file:///test.yaml")
        assert text_sync.get_version("file:///test.yaml") == 1

    def test_did_change_incremental(self, text_sync):
        open_params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri="file:///change.yaml",
                language_id="aeos",
                version=1,
                text="agent:\n  name: old\n",
            ),
        )
        text_sync.handle_open(open_params)

        change_params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(
                uri="file:///change.yaml", version=2
            ),
            content_changes=[
                TextDocumentContentChangePartial(
                    range=Range(
                        start=Position(line=1, character=0),
                        end=Position(line=1, character=10),
                    ),
                    text="  name: new\n",
                )
            ],
        )
        text_sync.handle_change(change_params)
        assert text_sync.get_version("file:///change.yaml") == 2

    def test_did_change_full(self, text_sync):
        open_params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri="file:///full.yaml",
                language_id="aeos",
                version=1,
                text="old content",
            ),
        )
        text_sync.handle_open(open_params)

        change_params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(
                uri="file:///full.yaml", version=2
            ),
            content_changes=[TextDocumentContentChangeWholeDocument(text="brand new content")],
        )
        text_sync.handle_change(change_params)
        assert text_sync.get_version("file:///full.yaml") == 2

    def test_did_save(self, text_sync):
        params = DidSaveTextDocumentParams(
            text_document=TextDocumentIdentifier(uri="file:///save.yaml"),
        )
        text_sync.handle_save(params)

    def test_did_save_with_text(self, text_sync):
        params = DidSaveTextDocumentParams(
            text_document=TextDocumentIdentifier(uri="file:///save-text.yaml"),
            text="saved content",
        )
        text_sync.handle_save(params)

    def test_did_close(self, text_sync):
        open_params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri="file:///close.yaml",
                language_id="aeos",
                version=1,
                text="content",
            ),
        )
        text_sync.handle_open(open_params)
        assert text_sync.is_open("file:///close.yaml")

        close_params = DidCloseTextDocumentParams(
            text_document=TextDocumentIdentifier(uri="file:///close.yaml"),
        )
        text_sync.handle_close(close_params)
        assert not text_sync.is_open("file:///close.yaml")

    def test_stale_version(self, text_sync):
        open_params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri="file:///stale.yaml",
                language_id="aeos",
                version=5,
                text="content",
            ),
        )
        text_sync.handle_open(open_params)

        change_params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(
                uri="file:///stale.yaml", version=3
            ),
            content_changes=[TextDocumentContentChangeWholeDocument(text="new")],
        )
        with pytest.raises(JsonRpcError) as exc_info:
            text_sync.handle_change(change_params)
        assert exc_info.value.code == AEOSErrorCodes.DocumentVersionStale

    def test_position_encoding_utf8(self):
        assert PositionEncoding.UTF8.value == "utf-8"

    def test_position_encoding_utf16(self):
        assert PositionEncoding.UTF16.value == "utf-16"

    def test_debounced_change(self):
        debouncer = DebouncedChange(delay_ms=50)
        callback = MagicMock()
        debouncer.debounce("file:///db.yaml", callback)
        assert debouncer.pending_count > 0
        debouncer.cancel_pending("file:///db.yaml")
        assert debouncer.pending_count == 0

    def test_debounce_cancel_all(self):
        debouncer = DebouncedChange(delay_ms=50)
        debouncer.debounce("file:///a.yaml", MagicMock())
        debouncer.debounce("file:///b.yaml", MagicMock())
        debouncer.cancel_pending()
        assert debouncer.pending_count == 0
