from __future__ import annotations

from aeos_lsp.schemas.loader import (
    SchemaLoader,
    SchemaLoadError,
    SchemaNotFoundError,
    SchemaParseError,
)
from aeos_lsp.schemas.registry import (
    SchemaRegistry,
    ArtifactType,
    schema_extension_map,
    extension_schema_map,
)
from aeos_lsp.schemas.validator import (
    SchemaValidator,
    ValidationError,
    Severity,
    ValidationResult,
)
from aeos_lsp.schemas.migrations import (
    SchemaMigrator,
    MigrationPlan,
    MigrationStep,
    MigrationAction,
    BreakingChange,
    FieldRename,
    auto_suggest_migration,
    detect_schema_version,
    CURRENT_SCHEMA_VERSION,
)

__all__ = [
    "SchemaLoader",
    "SchemaLoadError",
    "SchemaNotFoundError",
    "SchemaParseError",
    "SchemaRegistry",
    "ArtifactType",
    "schema_extension_map",
    "extension_schema_map",
    "SchemaValidator",
    "ValidationError",
    "Severity",
    "ValidationResult",
    "SchemaMigrator",
    "MigrationPlan",
    "MigrationStep",
    "MigrationAction",
    "BreakingChange",
    "FieldRename",
    "auto_suggest_migration",
    "detect_schema_version",
    "CURRENT_SCHEMA_VERSION",
]
