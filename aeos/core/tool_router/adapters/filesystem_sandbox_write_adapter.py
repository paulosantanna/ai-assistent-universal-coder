from __future__ import annotations

from pathlib import Path
from typing import Any

from aeos.core.tool_router.adapters.base_adapter import BaseToolAdapter


SANDBOX_BASE = ".aeos/sandbox"


class FilesystemSandboxWriteAdapter(BaseToolAdapter):
    tool_id = "filesystem-write-sandbox"

    def __init__(self, sandbox_base: str = SANDBOX_BASE):
        self.sandbox_base = Path(sandbox_base)

    def execute(self, action: str, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        if action == "filesystem.write_sandbox":
            return self._write_text_file(resource, input_data.get("content", ""))
        elif action == "filesystem.mkdir_sandbox":
            return self._mkdir(resource)
        else:
            return {"error": f"Unknown action '{action}' for filesystem-write-sandbox adapter"}

    def _resolve_and_validate(self, resource: str) -> tuple[Path, str | None]:
        target = Path(resource)
        if target.is_absolute():
            return target, "Absolute paths are not allowed in sandbox write"

        sandbox = self.sandbox_base.resolve()
        full_path = (sandbox / target).resolve()

        sandbox_str = str(sandbox).replace("\\", "/")
        full_str = str(full_path).replace("\\", "/")

        if not full_str.startswith(sandbox_str):
            return full_path, f"Write target '{resource}' is outside sandbox '{self.sandbox_base}'"

        if ".." in resource.split("/") or ".." in resource.split("\\"):
            return full_path, "Path traversal detected"

        return full_path, None

    def _write_text_file(self, resource: str, content: str) -> dict[str, Any]:
        full_path, error = self._resolve_and_validate(resource)
        if error:
            return {"error": error}

        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return {
                "written": True,
                "path": str(full_path),
                "size": len(content.encode("utf-8")),
            }
        except OSError as e:
            return {"error": f"Write failed: {e}"}

    def _mkdir(self, resource: str) -> dict[str, Any]:
        full_path, error = self._resolve_and_validate(resource)
        if error:
            return {"error": error}

        try:
            full_path.mkdir(parents=True, exist_ok=True)
            return {"created": True, "path": str(full_path)}
        except OSError as e:
            return {"error": f"Mkdir failed: {e}"}
