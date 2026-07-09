from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import Any

from aeos.core.tool_router.adapters.base_adapter import BaseToolAdapter


SUSPICIOUS_SECRET_NAMES = {
    ".env", ".secret", "credentials", "credential", "password",
    "token", "secret", "id_rsa", "id_dsa", ".npmrc", ".netrc",
}

BLOCKED_DIR_PREFIXES = {".git", "__pycache__", "node_modules"}


class PackageLocalAdapter(BaseToolAdapter):
    tool_id = "package-local"

    def execute(self, action: str, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        if action == "package.verify":
            return self._verify(resource, input_data)
        elif action == "package.inspect":
            return self._inspect_manifest(resource)
        elif action == "package.create":
            return {"error": "Package create not implemented in this phase"}
        elif action == "package.extract_staging":
            return self._verify(resource, input_data)
        else:
            return {"error": f"Unknown action '{action}' for package-local adapter"}

    def _verify(self, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        raw = input_data.get("content") or input_data.get("data")
        if not raw and resource:
            try:
                p = Path(resource)
                if p.exists():
                    raw = p.read_bytes()
            except OSError:
                return {"verified": False, "errors": ["Cannot read file"]}

        if not raw:
            return {"verified": False, "errors": ["No package data provided"]}

        if isinstance(raw, list):
            raw = bytes(raw)
        elif isinstance(raw, str):
            raw = raw.encode("utf-8")

        errors: list[str] = []
        try:
            with zipfile.ZipFile(BytesIO(raw)) as zf:
                for name in zf.namelist():
                    err = self._check_entry(name)
                    if err:
                        errors.append(err)
        except zipfile.BadZipFile:
            return {"verified": False, "errors": ["Invalid zip file"]}

        return {"verified": len(errors) == 0, "errors": errors}

    def _check_entry(self, name: str) -> str | None:
        normalized = name.replace("\\", "/")

        if normalized.startswith("/"):
            return f"Absolute path detected: {name}"

        resolved = PurePosixPath(normalized)
        if ".." in resolved.parts:
            return f"Path traversal detected: {name}"

        for blocked in BLOCKED_DIR_PREFIXES:
            if normalized.startswith(blocked) or f"/{blocked}" in normalized:
                return f"Blocked path prefix '{blocked}': {name}"

        stem = Path(normalized).name
        if stem.lower() in SUSPICIOUS_SECRET_NAMES:
            return f"Suspicious secret file name: {name}"

        return None

    def _inspect_manifest(self, resource: str) -> dict[str, Any]:
        raw = None
        if resource:
            try:
                p = Path(resource)
                if p.exists():
                    raw = p.read_bytes()
            except OSError:
                return {"error": "Cannot read file"}

        if not raw:
            return {"error": "No file path provided"}

        if isinstance(raw, list):
            raw = bytes(raw)
        elif isinstance(raw, str):
            raw = raw.encode("utf-8")

        entries = []
        try:
            with zipfile.ZipFile(BytesIO(raw)) as zf:
                for info in zf.infolist():
                    entry = {
                        "name": info.filename,
                        "size": info.file_size,
                        "compress_size": info.compress_size,
                        "is_dir": info.filename.endswith("/"),
                    }
                    entries.append(entry)
        except zipfile.BadZipFile:
            return {"error": "Invalid zip file"}

        return {"entries": entries, "count": len(entries)}
