from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

CURRENT_SCHEMA_VERSION = "1.0.0"


class MigrationAction(str, Enum):
    RENAME_FIELD = "rename_field"
    ADD_FIELD = "add_field"
    REMOVE_FIELD = "remove_field"
    CHANGE_TYPE = "change_type"
    CHANGE_REQUIRED = "change_required"
    CHANGE_ENUM = "change_enum"
    CHANGE_PATTERN = "change_pattern"
    CHANGE_DEFAULT = "change_default"
    FLATTEN = "flatten"
    UNFLATTEN = "unflatten"
    WRAP = "wrap"
    UNWRAP = "unwrap"
    CUSTOM = "custom"


@dataclass
class FieldRename:
    old_path: str
    new_path: str
    description: str = ""
    backwards_compatible: bool = True


@dataclass
class BreakingChange:
    path: str
    description: str
    change_type: str = "unknown"
    migration_available: bool = False
    migration_plan: MigrationPlan | None = None


@dataclass
class MigrationStep:
    action: MigrationAction
    path: str
    old_value: Any = None
    new_value: Any = None
    description: str = ""

    def apply(self, document: dict[str, Any]) -> dict[str, Any]:
        from copy import deepcopy

        result = deepcopy(document)

        if self.action == MigrationAction.RENAME_FIELD:
            self._apply_rename(result)
        elif self.action == MigrationAction.ADD_FIELD:
            self._apply_add(result)
        elif self.action == MigrationAction.REMOVE_FIELD:
            self._apply_remove(result)
        elif self.action == MigrationAction.CHANGE_DEFAULT:
            self._apply_set_default(result)
        elif self.action == MigrationAction.FLATTEN:
            self._apply_flatten(result)
        elif self.action == MigrationAction.UNFLATTEN:
            self._apply_unflatten(result)
        elif self.action == MigrationAction.WRAP:
            self._apply_wrap(result)
        elif self.action == MigrationAction.UNWRAP:
            self._apply_unwrap(result)

        return result

    def _get_value(self, doc: dict[str, Any], path: str) -> Any:
        parts = path.strip("/").split("/") if path else []
        current: Any = doc
        for part in parts:
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return current

    def _set_value(self, doc: dict[str, Any], path: str, value: Any) -> None:
        parts = path.strip("/").split("/") if path else []
        current: Any = doc
        for i, part in enumerate(parts[:-1]):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict):
                current = current.setdefault(part, {})
            elif isinstance(current, list):
                try:
                    p = int(part)
                    while len(current) <= p:
                        current.append({})
                    current = current[p]
                except (ValueError, IndexError):
                    return
            else:
                return
        last = parts[-1].replace("~1", "/").replace("~0", "~") if parts else ""
        if isinstance(current, dict):
            current[last] = value

    def _del_value(self, doc: dict[str, Any], path: str) -> None:
        parts = path.strip("/").split("/") if path else []
        current: Any = doc
        for i, part in enumerate(parts[:-1]):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict):
                current = current.get(part, {})
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return
            else:
                return
        last = parts[-1].replace("~1", "/").replace("~0", "~") if parts else ""
        if isinstance(current, dict) and last in current:
            del current[last]

    def _apply_rename(self, doc: dict[str, Any]) -> None:
        value = self._get_value(doc, self.path)
        if value is not None:
            self._del_value(doc, self.path)
            self._set_value(doc, str(self.new_value), value)

    def _apply_add(self, doc: dict[str, Any]) -> None:
        existing = self._get_value(doc, self.path)
        if existing is None:
            self._set_value(doc, self.path, self.new_value)

    def _apply_remove(self, doc: dict[str, Any]) -> None:
        self._del_value(doc, self.path)

    def _apply_set_default(self, doc: dict[str, Any]) -> None:
        existing = self._get_value(doc, self.path)
        if existing is None:
            self._set_value(doc, self.path, self.new_value)

    def _apply_flatten(self, doc: dict[str, Any]) -> None:
        container = self._get_value(doc, self.path)
        if isinstance(container, dict):
            for key, val in container.items():
                self._set_value(doc, f"{self.path}/{key}", val)

    def _apply_unflatten(self, doc: dict[str, Any]) -> None:
        parts = self.path.strip("/").split("/")
        if len(parts) < 2:
            return
        target_key = parts[-1]
        parent_path = "/".join(parts[:-1])
        value = self._get_value(doc, self.path)
        if value is not None:
            self._del_value(doc, self.path)
            parent = self._get_value(doc, parent_path)
            if isinstance(parent, dict):
                parent[target_key] = value

    def _apply_wrap(self, doc: dict[str, Any]) -> None:
        value = self._get_value(doc, self.path)
        if value is not None:
            wrapped = {str(self.new_value): value}
            self._set_value(doc, self.path, wrapped)

    def _apply_unwrap(self, doc: dict[str, Any]) -> None:
        container = self._get_value(doc, self.path)
        if isinstance(container, dict) and len(container) == 1:
            inner = next(iter(container.values()))
            self._set_value(doc, self.path, inner)


@dataclass
class MigrationPlan:
    from_version: str
    to_version: str
    steps: list[MigrationStep] = field(default_factory=list)
    backwards_compatible: bool = True
    description: str = ""
    field_renames: list[FieldRename] = field(default_factory=list)
    breaking_changes: list[BreakingChange] = field(default_factory=list)

    def apply(self, document: dict[str, Any]) -> dict[str, Any]:
        result = document
        for step in self.steps:
            try:
                result = step.apply(result)
            except Exception:
                logger.exception("Migration step failed: %s", step)
                raise
        return result

    def is_applicable(self, document: dict[str, Any]) -> bool:
        for step in self.steps:
            if step.action in (MigrationAction.RENAME_FIELD, MigrationAction.REMOVE_FIELD):
                continue
            if step.path:
                from aeos_lsp.schemas.migrations import _get_nested

                val = _get_nested(document, step.path)
                if val is None and step.action == MigrationAction.ADD_FIELD:
                    continue
        return True


def _get_nested(doc: dict[str, Any], path: str) -> Any:
    parts = path.strip("/").split("/") if path else []
    current: Any = doc
    for part in parts:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def detect_schema_version(document: dict[str, Any]) -> str:
    direct = document.get("schema_version") or document.get("version")
    if direct is not None:
        return str(direct)

    metadata = document.get("metadata", {})
    if isinstance(metadata, dict):
        sv = metadata.get("schema_version") or metadata.get("version")
        if sv is not None:
            return str(sv)

    if "agent_id" in document:
        return "1.0.0"
    if "skill_id" in document or "name" in document:
        return "1.0.0"
    if "steps" in document:
        return "1.0.0"

    return "0.0.0"


def detect_breaking_changes(
    old_schema: dict[str, Any],
    new_schema: dict[str, Any],
) -> list[BreakingChange]:
    changes: list[BreakingChange] = []

    old_props = old_schema.get("properties", {}) if isinstance(old_schema, dict) else {}
    new_props = new_schema.get("properties", {}) if isinstance(new_schema, dict) else {}

    if not isinstance(old_props, dict) or not isinstance(new_props, dict):
        return changes

    old_required = set(old_schema.get("required", []) if isinstance(old_schema, dict) else [])
    new_required = set(new_schema.get("required", []) if isinstance(new_schema, dict) else [])

    removed = set(old_props.keys()) - set(new_props.keys())
    for prop in removed:
        changes.append(
            BreakingChange(
                path=f"/{prop}",
                description=f"Property '{prop}' has been removed",
                change_type="removed_property",
            )
        )

    newly_required = new_required - old_required
    for prop in newly_required:
        changes.append(
            BreakingChange(
                path=f"/{prop}",
                description=f"Property '{prop}' is now required",
                change_type="newly_required",
            )
        )

    for prop in old_props:
        if prop in new_props:
            old_type = old_props[prop].get("type") if isinstance(old_props[prop], dict) else None
            new_type = new_props[prop].get("type") if isinstance(new_props[prop], dict) else None
            if old_type and new_type and old_type != new_type:
                narrowing = {"integer": "number"}
                if narrowing.get(old_type) != new_type:
                    changes.append(
                        BreakingChange(
                            path=f"/{prop}",
                            description=f"Property '{prop}' type changed from '{old_type}' to '{new_type}'",
                            change_type="type_change",
                        )
                    )

            old_enum = old_props[prop].get("enum") if isinstance(old_props[prop], dict) else None
            new_enum = new_props[prop].get("enum") if isinstance(new_props[prop], dict) else None
            if old_enum and new_enum and isinstance(old_enum, list) and isinstance(new_enum, list):
                removed_enums = set(old_enum) - set(new_enum)
                for val in removed_enums:
                    changes.append(
                        BreakingChange(
                            path=f"/{prop}",
                            description=f"Enum value '{val}' removed from property '{prop}'",
                            change_type="enum_value_removed",
                        )
                    )

    return changes


def auto_suggest_migration(
    document: dict[str, Any],
    target_version: str = CURRENT_SCHEMA_VERSION,
) -> MigrationPlan | None:
    from_version = detect_schema_version(document)

    steps: list[MigrationStep] = []
    field_renames: list[FieldRename] = []
    breaking_changes: list[BreakingChange] = []

    _add_common_migrations(from_version, target_version, document, steps, field_renames, breaking_changes)

    if not steps and not field_renames:
        return None

    return MigrationPlan(
        from_version=from_version,
        to_version=target_version,
        steps=steps,
        backwards_compatible=not bool(breaking_changes),
        description=f"Auto-generated migration from {from_version} to {target_version}",
        field_renames=field_renames,
        breaking_changes=breaking_changes,
    )


def _add_common_migrations(
    from_version: str,
    to_version: str,
    document: dict[str, Any],
    steps: list[MigrationStep],
    field_renames: list[FieldRename],
    breaking_changes: list[BreakingChange],
) -> None:
    _maybe_version_add(steps, document, from_version, to_version)

    _maybe_rename(steps, field_renames, document, "agent_id", "name")
    _maybe_rename(steps, field_renames, document, "skill_id", "name")
    _maybe_rename(steps, field_renames, document, "playbook_id", "name")
    _maybe_rename(steps, field_renames, document, "allowed_actions", "capabilities")
    _maybe_rename(steps, field_renames, document, "forbidden_actions", "restrictions")
    _maybe_rename(steps, field_renames, document, "evidence_requirements", "evidence")

    _maybe_flatten(steps, document, "metadata/config", "config")
    _maybe_flatten(steps, document, "metadata/settings", "settings")

    deprecated_fields = _find_deprecated_fields(document)
    for dep in deprecated_fields:
        steps.append(
            MigrationStep(
                action=MigrationAction.REMOVE_FIELD,
                path=dep,
                description=f"Removing deprecated field '{dep}'",
            )
        )


def _maybe_version_add(
    steps: list[MigrationStep],
    document: dict[str, Any],
    from_version: str,
    to_version: str,
) -> None:
    if "schema_version" not in document:
        steps.append(
            MigrationStep(
                action=MigrationAction.ADD_FIELD,
                path="/schema_version",
                new_value=to_version,
                description="Add schema_version field",
            )
        )


def _maybe_rename(
    steps: list[MigrationStep],
    field_renames: list[FieldRename],
    document: dict[str, Any],
    old_path: str,
    new_path: str,
) -> None:
    value = _get_nested(document, old_path)
    if value is not None and _get_nested(document, new_path) is None:
        steps.append(
            MigrationStep(
                action=MigrationAction.RENAME_FIELD,
                path=f"/{old_path}",
                new_value=new_path,
                description=f"Rename '{old_path}' to '{new_path}'",
            )
        )
        field_renames.append(
            FieldRename(
                old_path=f"/{old_path}",
                new_path=f"/{new_path}",
                description=f"Field '{old_path}' renamed to '{new_path}'",
            )
        )


def _maybe_flatten(
    steps: list[MigrationStep],
    document: dict[str, Any],
    source_path: str,
    target_field: str,
) -> None:
    container = _get_nested(document, source_path)
    if isinstance(container, dict) and _get_nested(document, target_field) is None:
        steps.append(
            MigrationStep(
                action=MigrationAction.FLATTEN,
                path=f"/{source_path}",
                new_value=target_field,
                description=f"Flatten '{source_path}' into '{target_field}'",
            )
        )


def _find_deprecated_fields(document: dict[str, Any]) -> list[str]:
    deprecated: list[str] = []
    _scan_deprecated(document, "", deprecated)
    return deprecated


def _scan_deprecated(data: Any, prefix: str, results: list[str]) -> None:
    if isinstance(data, dict):
        for key, val in data.items():
            path = f"{prefix}/{key}" if prefix else f"/{key}"
            if key == "deprecated" and val is True:
                continue
            if isinstance(val, dict):
                if val.get("deprecated") is True or val.get("x-deprecated") is True:
                    results.append(path)
                _scan_deprecated(val, path, results)
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    _scan_deprecated(item, f"{path}/{i}", results)


class SchemaMigrator:
    def __init__(self) -> None:
        self._migrations: dict[str, list[MigrationPlan]] = {}

    def register_migration(self, plan: MigrationPlan) -> None:
        key = f"{plan.from_version}->{plan.to_version}"
        if key not in self._migrations:
            self._migrations[key] = []
        self._migrations[key].append(plan)

    def get_migration_plan(
        self,
        from_version: str,
        to_version: str = CURRENT_SCHEMA_VERSION,
    ) -> MigrationPlan | None:
        key = f"{from_version}->{to_version}"
        plans = self._migrations.get(key)
        if plans:
            return plans[0]

        direct = auto_suggest_migration(
            {"schema_version": from_version},
            to_version,
        )
        return direct

    def migrate(self, document: dict[str, Any], target_version: str = CURRENT_SCHEMA_VERSION) -> dict[str, Any]:
        from_version = detect_schema_version(document)
        if from_version == target_version:
            return document

        plan = self.get_migration_plan(from_version, target_version)
        if plan is None:
            logger.warning(
                "No migration path from %s to %s. Returning document unchanged.",
                from_version, target_version,
            )
            return document

        logger.info(
            "Migrating document from %s to %s (%d steps)",
            from_version, target_version, len(plan.steps),
        )
        return plan.apply(document)

    def list_registered_migrations(self) -> list[str]:
        return list(self._migrations.keys())

    def clear_migrations(self) -> None:
        self._migrations.clear()
