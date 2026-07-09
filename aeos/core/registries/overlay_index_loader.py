from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml


class OverlayRegistryIndexLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.generated_at: Optional[str] = None
        self.note: Optional[str] = None
        self.fragment_paths: list[str] = []
        self.raw_data: Optional[dict] = None

    def load(self, index_path: str) -> list[str]:
        full_path = self.workspace_root / index_path
        if not full_path.exists():
            raise FileNotFoundError(f"Overlay index not found: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            self.raw_data = yaml.safe_load(f)

        if not self.raw_data:
            raise ValueError(f"Empty overlay index: {full_path}")

        self.generated_at = self.raw_data.get("generated_at")
        self.note = self.raw_data.get("note")

        fragments = self.raw_data.get("registry_fragments", [])
        if not fragments:
            raise ValueError(f"No registry_fragments found in overlay index: {full_path}")

        self.fragment_paths = []
        for entry in fragments:
            path = entry.get("path", "")
            if path:
                resolved = str((self.workspace_root / path).resolve())
                self.fragment_paths.append(resolved)

        return self.fragment_paths

    def get_fragment_count(self) -> int:
        return len(self.fragment_paths)
