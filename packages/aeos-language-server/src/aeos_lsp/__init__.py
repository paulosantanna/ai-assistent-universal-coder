from __future__ import annotations

__version__ = "1.0.0"
__all__ = [
    "__version__",
    "AEOSLanguageServer",
    "get_server",
    "build_server_capabilities",
    "LSPClientConfig",
    "WorkspaceManager",
    "SemanticModel",
    "WorkspaceIndexer",
    "DiagnosticsEngine",
    "CommandRegistry",
    "SchemaRegistry",
]

import importlib
import typing as _t

_A: _t.Dict[str, _t.Any] = {}


def __getattr__(name: str) -> _t.Any:
    if name in _A:
        return _A[name]
    _lazy_map: _t.Dict[str, str] = {
        "AEOSLanguageServer": "aeos_lsp.server",
        "get_server": "aeos_lsp.server",
        "build_server_capabilities": "aeos_lsp.capabilities",
        "LSPClientConfig": "aeos_lsp.configuration",
        "WorkspaceManager": "aeos_lsp.workspace",
        "SemanticModel": "aeos_lsp.semantic.semantic_model",
        "WorkspaceIndexer": "aeos_lsp.index",
        "DiagnosticsEngine": "aeos_lsp.diagnostics",
        "CommandRegistry": "aeos_lsp.commands",
        "SchemaRegistry": "aeos_lsp.schemas",
    }
    if name in _lazy_map:
        mod = importlib.import_module(_lazy_map[name])
        attr = getattr(mod, name, None)
        if attr is not None:
            _A[name] = attr
            return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
