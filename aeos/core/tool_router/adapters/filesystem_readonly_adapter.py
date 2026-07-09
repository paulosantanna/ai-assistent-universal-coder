from __future__ import annotations

from pathlib import Path
from typing import Any

from aeos.core.tool_router.adapters.base_adapter import BaseToolAdapter
from aeos.core.evidence.hash_utils import sha256


class FilesystemReadonlyAdapter(BaseToolAdapter):
    tool_id = "filesystem-readonly"

    MAX_FILE_BYTES = 1_048_576  # 1MB default limit

    def __init__(self, max_file_bytes: int = 0):
        self.max_file_bytes = max_file_bytes or self.MAX_FILE_BYTES

    def execute(self, action: str, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        if action == "filesystem.list":
            return self._list_dir(resource)
        elif action == "filesystem.read":
            return self._read_text_file(resource)
        elif action == "filesystem.exists":
            return self._stat_file(resource)
        elif action == "filesystem.stat":
            return self._stat_file(resource)
        else:
            return {"error": f"Unknown action '{action}' for filesystem-readonly adapter"}

    def _list_dir(self, path_str: str) -> dict[str, Any]:
        p = Path(path_str)
        if not p.exists():
            return {"error": f"Path not found: {path_str}", "entries": []}
        if not p.is_dir():
            return {"error": f"Not a directory: {path_str}", "entries": []}
        entries = []
        for child in sorted(p.iterdir()):
            try:
                is_dir = child.is_dir()
                entries.append({
                    "name": child.name,
                    "path": str(child),
                    "is_dir": is_dir,
                    "size": child.stat().st_size if not is_dir else 0,
                })
            except OSError:
                pass
        return {"entries": entries, "count": len(entries)}

    def _read_text_file(self, path_str: str) -> dict[str, Any]:
        p = Path(path_str)
        if not p.exists():
            return {"error": f"File not found: {path_str}"}
        if not p.is_file():
            return {"error": f"Not a file: {path_str}"}
        try:
            size = p.stat().st_size
            if size > self.max_file_bytes:
                return {"error": f"File exceeds size limit ({size} > {self.max_file_bytes} bytes)"}
            content = p.read_text(encoding="utf-8")
            return {
                "content": content,
                "size": size,
                "sha256": sha256(content),
                "path": str(p.resolve()),
            }
        except (OSError, UnicodeDecodeError) as e:
            return {"error": f"Cannot read file: {e}"}

    def _stat_file(self, path_str: str) -> dict[str, Any]:
        p = Path(path_str)
        if not p.exists():
            return {"exists": False, "path": path_str}
        try:
            stat = p.stat()
            return {
                "exists": True,
                "path": str(p.resolve()),
                "is_dir": p.is_dir(),
                "is_file": p.is_file(),
                "size": stat.st_size,
                "modified": stat.st_mtime,
            }
        except OSError as e:
            return {"error": f"Stat failed: {e}"}
