from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aeos_lsp.configuration import LSPClientConfig

AEOS_ROOT_MARKERS = {"aeos.config.yaml", "aeos.json", "aeos.jsonc", "aeos.toml"}


@dataclass(frozen=True)
class WorkspaceFolderInfo:
    uri: str
    name: str
    trusted: bool = False
    config: LSPClientConfig = field(default_factory=LSPClientConfig)

    @property
    def path(self) -> Path:
        return Path(self.uri).resolve() if self.uri.startswith("file://") else Path(self.uri).resolve()

    @property
    def is_aeos_project(self) -> bool:
        return detect_aeos_root(self.path) is not None


def detect_aeos_root(path: Path) -> Path | None:
    resolved = path.resolve()
    for marker in ("aeos.config.yaml", "aeos.json", "aeos.jsonc", "aeos.toml"):
        candidate = resolved / marker
        if candidate.is_file():
            return resolved
    for parent in resolved.parents:
        for marker in ("aeos.config.yaml", "aeos.json", "aeos.jsonc", "aeos.toml"):
            if (parent / marker).is_file():
                return parent
    return None


def validate_folder(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, "Path does not exist"
    if not path.is_dir():
        return False, "Path is not a directory"
    if not path.is_absolute():
        return False, "Path is not absolute"
    return True, None
