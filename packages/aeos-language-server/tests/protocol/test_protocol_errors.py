from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import ErrorCodes, LSPErrorCodes

from aeos_lsp.protocol.errors import (
    AEOSErrorCodes,
    JsonRpcError,
    create_error_response,
    parse_error_response,
    _handle_method_not_found,
    _handle_request_failed,
    _dispatch_error,
    register_error_handlers,
)


class TestProtocolErrors:
    def test_method_not_found(self):
        ls = MagicMock()
        result = _handle_method_not_found(ls, {"method": "unknown"})
        assert result is not None
        assert result.get("error", {}).get("code") == ErrorCodes.MethodNotFound
        assert "not found" in result["error"]["message"]

    def test_invalid_params(self):
        err = JsonRpcError(code=LSPErrorCodes.RequestFailed, message="Invalid params")
        assert err.code == LSPErrorCodes.RequestFailed
        assert "Invalid params" in err.message

    def test_invalid_json(self):
        err = JsonRpcError(code=ErrorCodes.ParseError, message="Parse error")
        assert err.code == ErrorCodes.ParseError

    def test_invalid_request(self):
        err = JsonRpcError(code=ErrorCodes.InvalidRequest, message="Invalid request")
        assert err.code == ErrorCodes.InvalidRequest

    def test_aeos_error_codes(self):
        assert AEOSErrorCodes.DocumentVersionStale == -32900
        assert AEOSErrorCodes.IndexNotReady == -32901
        assert AEOSErrorCodes.ConfigurationError == -32902
        assert AEOSErrorCodes.WorkspaceNotTrusted == -32903
        assert AEOSErrorCodes.PermissionDenied == -32904

    def test_create_error_response(self):
        resp = create_error_response(
            code=ErrorCodes.MethodNotFound,
            message="Not found",
            id=1,
        )
        assert resp["jsonrpc"] == "2.0"
        assert resp["id"] == 1
        assert resp["error"]["code"] == ErrorCodes.MethodNotFound
        assert resp["error"]["message"] == "Not found"

    def test_create_error_response_with_data(self):
        resp = create_error_response(
            code=AEOSErrorCodes.DocumentVersionStale,
            message="Version mismatch",
            data={"expected": 5, "received": 3},
            id=2,
        )
        assert resp["error"]["data"]["expected"] == 5
        assert resp["error"]["data"]["received"] == 3

    def test_parse_error_response(self):
        raw = {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {"code": -32601, "message": "Not found"},
        }
        err = parse_error_response(raw)
        assert err is not None
        assert err.code == -32601
        assert err.message == "Not found"

    def test_parse_error_response_no_error(self):
        raw = {"jsonrpc": "2.0", "id": 1, "result": {}}
        err = parse_error_response(raw)
        assert err is None

    def test_request_failed(self):
        ls = MagicMock()
        result = _handle_request_failed(ls, ValueError("something broke"))
        assert result is not None
        assert "error" in result
        assert "something broke" in result["error"]["message"]

    def test_dispatch_jsonrpc_error(self):
        ls = MagicMock()
        err = JsonRpcError(code=AEOSErrorCodes.PermissionDenied, message="Denied")
        _dispatch_error(ls, err, "test")
        ls.window_show_message.assert_called_once()
        args = ls.window_show_message.call_args[0][0]
        assert "Denied" in args.message

    def test_dispatch_generic_error(self):
        ls = MagicMock()
        _dispatch_error(ls, RuntimeError("crash"), "test")

    def test_register_error_handlers(self):
        ls = MagicMock()
        register_error_handlers(ls)
        assert hasattr(ls, "report_server_error")

    def test_jsonrpc_error_to_dict(self):
        err = JsonRpcError(code=-32900, message="Stale", data={"uri": "x"})
        d = err.to_dict()
        assert d["code"] == -32900
        assert d["message"] == "Stale"
        assert d["data"]["uri"] == "x"
