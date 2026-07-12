from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SchemaLoadError(Exception):
    ...


class SchemaNotFoundError(SchemaLoadError):
    ...


class SchemaParseError(SchemaLoadError):
    ...


class SchemaLoader:
    def __init__(
        self,
        schema_dirs: list[str | Path] | None = None,
        package_resource: str | None = None,
    ) -> None:
        self._cache: dict[str, dict[str, Any]] = {}
        self._ref_cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._schema_dirs: list[Path] = []
        self._package_resource = package_resource

        if schema_dirs:
            for d in schema_dirs:
                p = Path(d)
                if p.is_dir():
                    self._schema_dirs.append(p.resolve())
                else:
                    logger.warning("Schema directory does not exist: %s", p)

        self._resolve_stack: set[str] = set()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_schema(self, name: str) -> dict[str, Any]:
        normalized = self._normalize_name(name)
        with self._lock:
            cached = self._cache.get(normalized)
            if cached is not None:
                return cached
        schema = self._load_schema_unlocked(normalized)
        resolved = self._resolve_refs(schema, normalized)
        with self._lock:
            self._cache[normalized] = resolved
        return resolved

    def load_schema_from_path(self, path: str | Path) -> dict[str, Any]:
        p = Path(path).resolve()
        if not p.is_file():
            raise SchemaNotFoundError(f"Schema file not found: {p}")
        try:
            with p.open("r", encoding="utf-8") as f:
                schema: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise SchemaParseError(f"Failed to parse schema {p}: {e}") from e
        resolved = self._resolve_refs(schema, str(p))
        with self._lock:
            self._cache[self._normalize_name(p.stem)] = resolved
        return resolved

    def load_schema_from_data(self, data: dict[str, Any], name: str) -> dict[str, Any]:
        resolved = self._resolve_refs(data, name)
        with self._lock:
            self._cache[self._normalize_name(name)] = resolved
        return resolved

    def get_cached(self, name: str) -> dict[str, Any] | None:
        with self._lock:
            return self._cache.get(self._normalize_name(name))

    def list_available(self) -> list[str]:
        names: list[str] = []
        seen: set[str] = set()
        for d in self._schema_dirs:
            if d.is_dir():
                for entry in d.iterdir():
                    if entry.suffix in {".json", ".jsonc"}:
                        stem = entry.stem
                        if stem not in seen:
                            seen.add(stem)
                            names.append(stem)
        if self._package_resource:
            try:
                from importlib.resources import contents

                for res in contents(self._package_resource):
                    if res.endswith((".json", ".jsonc")):
                        stem = Path(res).stem
                        if stem not in seen:
                            seen.add(stem)
                            names.append(stem)
            except Exception:
                pass
        return sorted(names)

    def clear_cache(self) -> None:
        with self._lock:
            self._cache.clear()
            self._ref_cache.clear()

    def prefetch(self, names: list[str]) -> None:
        for name in names:
            try:
                self.load_schema(name)
            except SchemaLoadError:
                logger.debug("Failed to prefetch schema '%s'", name)

    def validate_schema_structure(self, schema: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        if not isinstance(schema, dict):
            errors.append("Schema root must be a JSON object")
            return errors
        if "type" not in schema and "properties" not in schema and "$ref" not in schema:
            errors.append("Schema missing 'type', 'properties', or '$ref'")
        return errors

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _normalize_name(self, name: str) -> str:
        name = name.replace("\\", "/")
        for suffix in (".json", ".jsonc", ".schema"):
            if name.endswith(suffix):
                name = name[: -len(suffix)]
        return name.strip().lower()

    def _load_schema_unlocked(self, name: str) -> dict[str, Any]:
        for d in self._schema_dirs:
            for ext in (".json", ".jsonc"):
                candidate = d / f"{name}{ext}"
                if candidate.is_file():
                    try:
                        with candidate.open("r", encoding="utf-8") as f:
                            return self._checked(json.load(f), candidate)
                    except json.JSONDecodeError as e:
                        raise SchemaParseError(
                            f"Failed to parse {candidate}: {e}"
                        ) from e

        if self._package_resource:
            try:
                from importlib.resources import open_text

                for ext in (".json", ".jsonc"):
                    resource_name = f"{name}{ext}"
                    try:
                        with open_text(self._package_resource, resource_name) as f:
                            return self._checked(json.load(f), resource_name)
                    except (FileNotFoundError, ModuleNotFoundError):
                        continue
            except Exception:
                pass

        raise SchemaNotFoundError(
            f"Schema '{name}' not found in any configured location"
        )

    @staticmethod
    def _checked(data: Any, source: str | Path) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise SchemaParseError(
                f"Schema root must be a JSON object, got {type(data).__name__} in {source}"
            )
        return data

    def _resolve_refs(
        self,
        schema: dict[str, Any],
        origin: str,
    ) -> dict[str, Any]:
        return _RefResolver(self, origin, self._resolve_stack).resolve(schema)


class _RefResolver:
    def __init__(
        self,
        loader: SchemaLoader,
        origin: str,
        resolve_stack: set[str],
    ) -> None:
        self._loader = loader
        self._origin = origin
        self._resolve_stack = resolve_stack

    def resolve(self, node: Any) -> Any:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if ref is not None and isinstance(ref, str):
                return self._resolve_ref(ref)
            return {k: self.resolve(v) for k, v in node.items()}
        if isinstance(node, list):
            return [self.resolve(item) for item in node]
        return node

    def _resolve_ref(self, ref: str) -> Any:
        if ref in self._resolve_stack:
            logger.warning("Circular $ref detected: %s", ref)
            return {"$ref": ref}

        if ref.startswith("#"):
            logger.debug("Local $ref '%s' not resolved at schema level", ref)
            return {"$ref": ref}

        fragment = ""
        if "#" in ref:
            ref_path, fragment = ref.split("#", 1)

        resolved: dict[str, Any]
        if ref_path:
            cache_key = f"{ref_path}::{self._origin}"
            cached = self._loader._ref_cache.get(cache_key)
            if cached is not None:
                resolved = cached
            else:
                resolved = self._loader._load_schema_unlocked(ref_path)
                self._loader._ref_cache[cache_key] = resolved
        else:
            resolved = self._loader._load_schema_unlocked(
                self._loader._normalize_name(self._origin)
            )

        if fragment:
            parts = fragment.strip("/").split("/")
            current: Any = resolved
            for part in parts:
                part = part.replace("~1", "/").replace("~0", "~")
                if isinstance(current, dict):
                    current = current.get(part)
                elif isinstance(current, list):
                    try:
                        idx = int(part)
                        current = current[idx]
                    except (ValueError, IndexError):
                        current = None
                else:
                    current = None
                if current is None:
                    logger.warning("Fragment '%s' not found in $ref '%s'", fragment, ref)
                    return {"$ref": ref}
            return current

        return resolved
