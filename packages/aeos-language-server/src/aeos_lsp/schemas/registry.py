from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from aeos_lsp.schemas.loader import SchemaLoader

logger = logging.getLogger(__name__)


class ArtifactType(str, Enum):
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"
    POLICY = "policy"
    PERMISSION = "permission"
    REGISTRY = "registry"
    MODEL_PROFILE = "model_profile"
    TOKEN_BUDGET = "token_budget"
    QUALITY_GATE = "quality_gate"
    JUDGE_RULE = "judge_rule"
    EVIDENCE_REQUIREMENT = "evidence_requirement"
    TOOL = "tool"
    COMMAND = "command"
    WORKSPACE = "workspace"
    REPOSITORY = "repository"
    CONFIG = "config"
    TASK = "task"
    JUDGE_REPORT = "judge_report"
    EVIDENCE = "evidence"
    CHECKPOINT = "checkpoint"
    CUSTOM = "custom"


schema_extension_map: dict[ArtifactType, list[str]] = {
    ArtifactType.AGENT: [".agent.md", ".agent.yaml", ".agent.yml", ".agent.json"],
    ArtifactType.SKILL: [".skill.md", ".skill.yaml", ".skill.yml", ".skill.json"],
    ArtifactType.PLAYBOOK: [".playbook.md", ".playbook.yaml", ".playbook.yml", ".playbook.json"],
    ArtifactType.POLICY: [".policy.yaml", ".policy.yml", "policies.yaml"],
    ArtifactType.PERMISSION: [".permission.yaml", ".permission.yml", "permissions.yaml"],
    ArtifactType.REGISTRY: [".registry.yaml", ".registry.yml", ".registry.json"],
    ArtifactType.MODEL_PROFILE: [".model.yaml", ".model.yml", ".model.json"],
    ArtifactType.TOKEN_BUDGET: [".token-budget.yaml", ".token-budget.yml"],
    ArtifactType.QUALITY_GATE: [".quality-gate.yaml", ".quality-gate.yml"],
    ArtifactType.JUDGE_RULE: [".judge-rule.yaml", ".judge-rule.yml"],
    ArtifactType.EVIDENCE_REQUIREMENT: [".evidence.yaml", ".evidence.yml"],
    ArtifactType.TOOL: [".tool.yaml", ".tool.yml", ".tool.json"],
    ArtifactType.COMMAND: [".command.yaml", ".command.yml"],
    ArtifactType.CONFIG: ["aeos.config.yaml", ".aeos.yaml", ".aeos.yml", ".aeos.json", ".aeos.jsonc", ".aeos.toml"],
    ArtifactType.TASK: [".task.json", ".task.schema.json"],
    ArtifactType.JUDGE_REPORT: ["judge_report.schema.json"],
    ArtifactType.EVIDENCE: ["evidence.schema.json"],
    ArtifactType.CHECKPOINT: ["checkpoint.schema.json"],
}

extension_schema_map: dict[str, ArtifactType] = {}
for atype, exts in schema_extension_map.items():
    for ext in exts:
        extension_schema_map[ext] = atype


@dataclass
class SchemaEntry:
    artifact_type: ArtifactType
    schema_name: str
    version: str = "1.0.0"
    description: str = ""
    aliases: list[str] = field(default_factory=list)

    @property
    def schema_key(self) -> str:
        return f"{self.artifact_type.value}@{self.version}"


class SchemaRegistry:
    def __init__(self, loader: SchemaLoader | None = None) -> None:
        self._loader = loader or SchemaLoader()
        self._entries: dict[str, SchemaEntry] = {}
        self._type_index: dict[str, str] = {}
        self._extension_index: dict[str, str] = {}
        self._version_index: dict[str, dict[str, str]] = {}
        self._initialized = False

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_builtins(self) -> None:
        for atype in ArtifactType:
            if atype == ArtifactType.CUSTOM:
                continue
            schema_name = f"{atype.value}.schema"
            self.register(
                SchemaEntry(
                    artifact_type=atype,
                    schema_name=schema_name,
                    version="1.0.0",
                )
            )

    def register(self, entry: SchemaEntry) -> None:
        key = entry.schema_key
        self._entries[key] = entry
        self._type_index[entry.artifact_type.value] = key

        if entry.artifact_type.value not in self._version_index:
            self._version_index[entry.artifact_type.value] = {}
        self._version_index[entry.artifact_type.value][entry.version] = key

        for ext in schema_extension_map.get(entry.artifact_type, []):
            self._extension_index[ext] = key

        for alias in entry.aliases:
            self._extension_index[alias] = key

    def register_custom(
        self,
        name: str,
        schema_data: dict[str, Any],
        extensions: list[str] | None = None,
        version: str = "1.0.0",
    ) -> SchemaEntry:
        self._loader.load_schema_from_data(schema_data, name)
        entry = SchemaEntry(
            artifact_type=ArtifactType.CUSTOM,
            schema_name=name,
            version=version,
            description=f"Custom schema: {name}",
            aliases=extensions or [],
        )
        self.register(entry)
        return entry

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_schema(self, artifact_type: str) -> dict[str, Any] | None:
        key = self._type_index.get(artifact_type)
        if key is None:
            logger.warning("No schema registered for artifact type '%s'", artifact_type)
            return None
        entry = self._entries.get(key)
        if entry is None:
            return None
        return self._try_load(entry)

    def get_schema_for_extension(self, ext: str) -> dict[str, Any] | None:
        key = self._extension_index.get(ext)
        if key is None:
            key = self._extension_index.get(ext.lower())
        if key is None:
            return None
        entry = self._entries.get(key)
        if entry is None:
            return None
        return self._try_load(entry)

    def get_schema_for_uri(self, uri: str) -> dict[str, Any] | None:
        from urllib.parse import urlparse

        parsed = urlparse(uri)
        path = parsed.path or parsed.netloc
        lower_path = path.lower()
        for ext, key in self._extension_index.items():
            if lower_path.endswith(ext):
                entry = self._entries.get(key)
                if entry is not None:
                    return self._try_load(entry)
        stem = Path(path).stem
        for entry in self._entries.values():
            if entry.schema_name == stem or entry.schema_name == f"{stem}.schema":
                return self._try_load(entry)
        return None

    def get_schema_version(self, artifact_type: str) -> str | None:
        key = self._type_index.get(artifact_type)
        if key is None:
            return None
        entry = self._entries.get(key)
        return entry.version if entry else None

    def get_entry(self, artifact_type: str) -> SchemaEntry | None:
        key = self._type_index.get(artifact_type)
        return self._entries.get(key) if key else None

    def list_schemas(self) -> list[SchemaEntry]:
        return list(self._entries.values())

    def list_artifact_types(self) -> list[str]:
        return sorted(
            {entry.artifact_type.value for entry in self._entries.values()}
        )

    def resolve_artifact_type(self, uri_or_ext: str) -> str | None:
        entry = self.get_schema_for_uri(uri_or_ext)
        if entry is not None:
            return None
        atype = extension_schema_map.get(uri_or_ext)
        if atype is not None:
            return atype.value
        for ext, atype in extension_schema_map.items():
            if uri_or_ext.endswith(ext) or uri_or_ext.endswith(ext.lower()):
                return atype.value
        return None

    # ------------------------------------------------------------------
    # Versions
    # ------------------------------------------------------------------

    def list_versions(self, artifact_type: str) -> list[str]:
        versions = self._version_index.get(artifact_type, {})
        return sorted(versions.keys(), key=self._parse_version, reverse=True)

    def get_schema_at_version(self, artifact_type: str, version: str) -> dict[str, Any] | None:
        versions = self._version_index.get(artifact_type)
        if versions is None:
            return None
        key = versions.get(version)
        if key is None:
            return None
        entry = self._entries.get(key)
        if entry is None:
            return None
        return self._try_load(entry)

    def has_breaking_changes(self, artifact_type: str, from_version: str, to_version: str) -> bool:
        from aeos_lsp.schemas.migrations import detect_breaking_changes

        old_schema = self.get_schema_at_version(artifact_type, from_version)
        new_schema = self.get_schema_at_version(artifact_type, to_version)
        if old_schema is None or new_schema is None:
            return True
        return bool(detect_breaking_changes(old_schema, new_schema))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _try_load(self, entry: SchemaEntry) -> dict[str, Any] | None:
        try:
            return self._loader.load_schema(entry.schema_name)
        except Exception:
            logger.exception("Failed to load schema '%s'", entry.schema_name)
            return None

    @staticmethod
    def _parse_version(v: str) -> tuple[int, ...]:
        try:
            return tuple(int(p) for p in v.split("."))
        except Exception:
            return (0,)


