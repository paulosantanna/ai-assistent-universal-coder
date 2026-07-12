from __future__ import annotations

import enum
import logging
import traceback
from typing import Any, ClassVar

from lsprotocol import types
from pygls.lsp.server import LanguageServer

logger = logging.getLogger(__name__)


class AEOSErrorCodes(enum.IntEnum):
    DocumentVersionStale = -32900
    IndexNotReady = -32901
    ConfigurationError = -32902
    WorkspaceNotTrusted = -32903
    PermissionDenied = -32904
    PolicyViolation = -32905
    EvidenceIntegrityFailure = -32906
    ToolExecutionBlocked = -32907
    CapabilityNotSupported = -32908
    CacheOutdated = -32909
    ResourceQuotaExceeded = -32910


JsonRpcErrorCode = int | types.ErrorCodes | types.LSPErrorCodes | AEOSErrorCodes


class JsonRpcError(Exception):
    codes: ClassVar[dict[str, JsonRpcErrorCode]] = {}

    def __init__(
        self,
        code: JsonRpcErrorCode,
        message: str,
        data: Any = None,
    ) -> None:
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": int(self.code),
            "message": self.message,
        }
        if self.data is not None:
            result["data"] = self.data
        return result


def create_error_response(
    code: JsonRpcErrorCode,
    message: str,
    data: Any = None,
    id: int | str | None = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "jsonrpc": "2.0",
        "error": {
            "code": int(code),
            "message": message,
        },
    }
    if data is not None:
        response["error"]["data"] = data
    if id is not None:
        response["id"] = id
    return response


def parse_error_response(response: dict[str, Any]) -> JsonRpcError | None:
    error = response.get("error")
    if error is None:
        return None
    return JsonRpcError(
        code=error.get("code", types.ErrorCodes.UnknownErrorCode),
        message=error.get("message", "Unknown error"),
        data=error.get("data"),
    )


def _jsonrpc_error_to_message_type(code: JsonRpcErrorCode) -> types.MessageType:
    if isinstance(code, AEOSErrorCodes) and code >= AEOSErrorCodes.PermissionDenied:
        return types.MessageType.Warning
    if isinstance(code, types.LSPErrorCodes):
        return types.MessageType.Info
    return types.MessageType.Error


def _handle_method_not_found(
    ls: LanguageServer,
    params: dict[str, Any] | None,
) -> dict[str, Any] | None:
    logger.warning("Method not found: %s", params)
    ls.window_show_message(
        types.ShowMessageParams(
            message=f"Unsupported method requested: {params}",
            type=types.MessageType.Warning,
        )
    )
    return create_error_response(
        code=types.ErrorCodes.MethodNotFound,
        message=f"Method not found: {params}",
        data={"request": params},
    )


def _handle_request_failed(
    ls: LanguageServer,
    exception: Exception,
) -> dict[str, Any]:
    logger.error("Request failed: %s", traceback.format_exc())
    ls.window_show_message(
        types.ShowMessageParams(
            message=f"Request failed: {exception}",
            type=types.MessageType.Error,
        )
    )
    return create_error_response(
        code=types.LSPErrorCodes.RequestFailed,
        message=str(exception),
        data={"exception": type(exception).__name__},
    )


def _dispatch_error(
    ls: LanguageServer,
    error: Exception,
    source: Any,
) -> None:
    if isinstance(error, JsonRpcError):
        ls.window_show_message(
            types.ShowMessageParams(
                message=error.message,
                type=_jsonrpc_error_to_message_type(error.code),
            )
        )
        logger.error("JsonRpcError [%s]: %s", error.code, error.message)
        return

    logger.error("Unhandled error from %s: %s", source, traceback.format_exc())
    ls.window_show_message(
        types.ShowMessageParams(
            message=f"Internal server error: {error}",
            type=types.MessageType.Error,
        )
    )


def register_error_handlers(ls: LanguageServer) -> None:
    ls.report_server_error = lambda error, source: _dispatch_error(ls, error, source)  # type: ignore[method-assign]
    logger.debug("Error handlers registered")
