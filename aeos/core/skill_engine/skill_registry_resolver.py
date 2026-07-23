from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


class SkillRegistryResolver:
    _shared_cache: dict[tuple[str, tuple[tuple[str, int, int], ...]], dict[str, dict[str, Any]]] = {}

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self._registry: dict[str, dict[str, Any]] = {}
        self._fingerprint: tuple[str, tuple[tuple[str, int, int], ...]] | None = None

    def load(self) -> dict[str, dict[str, Any]]:
        paths = self._find_registry_paths()
        if not paths:
            return self._registry

        fingerprint = self._fingerprint_for(paths)
        if self._fingerprint == fingerprint and self._registry:
            return self._registry

        cached = self._shared_cache.get(fingerprint)
        if cached is not None:
            self._registry = dict(cached)
            self._fingerprint = fingerprint
            return self._registry

        registry: dict[str, dict[str, Any]] = {}
        for path in paths:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for entry in data.get("skills", []):
                eid = entry.get("id")
                if eid:
                    registry[eid] = entry
        self._registry = registry
        self._fingerprint = fingerprint
        self._shared_cache[fingerprint] = dict(registry)
        return self._registry

    def resolve(self, skill_id: str) -> Optional[dict[str, Any]]:
        if not self._registry:
            self.load()
        return self._registry.get(skill_id)

    def list_skills(self) -> list[str]:
        if not self._registry:
            self.load()
        return list(self._registry.keys())

    def get_skill_path(self, skill_id: str) -> Optional[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("path")
        return None

    def get_owner_agent(self, skill_id: str) -> Optional[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("owner_agent")
        return None

    def get_capabilities(self, skill_id: str) -> list[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("capabilities", [])
        return []

    @classmethod
    def clear_cache(cls) -> None:
        cls._shared_cache.clear()

    @classmethod
    def cache_size(cls) -> int:
        return len(cls._shared_cache)

    def _find_registry_paths(self) -> list[Path]:
        candidates = [
            self.workspace_root / ".aeos" / "derived" / "registries" / "skills.consolidated.yaml",
            self.workspace_root / "aeos" / "registries" / "skills.registry.yaml",
        ]
        return [path for path in candidates if path.exists()]

    def _fingerprint_for(self, paths: list[Path]) -> tuple[str, tuple[tuple[str, int, int], ...]]:
        files: list[tuple[str, int, int]] = []
        for path in paths:
            stat = path.stat()
            files.append((str(path.resolve()), stat.st_mtime_ns, stat.st_size))
        return (str(self.workspace_root), tuple(files))
