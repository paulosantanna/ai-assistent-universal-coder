from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from aeos_lsp.schemas.loader import SchemaLoader
from aeos_lsp.schemas.registry import SchemaRegistry, ArtifactType
from aeos_lsp.schemas.validator import SchemaValidator, ValidationResult, ValidationError, Severity
from aeos_lsp.schemas.migrations import (
    SchemaMigrator, MigrationPlan, MigrationStep, MigrationAction,
    FieldRename, detect_schema_version, CURRENT_SCHEMA_VERSION,
)


class TestSchemaLoader:
    def test_loader_initialization(self):
        loader = SchemaLoader()
        assert loader is not None

    def test_load_schema(self):
        loader = SchemaLoader(schema_dirs=[])
        with pytest.raises((FileNotFoundError, Exception)):
            loader.load_schema("agent")

    def test_list_available(self):
        loader = SchemaLoader(schema_dirs=[])
        available = loader.list_available()
        assert isinstance(available, list)


class TestSchemaRegistry:
    def test_registry_initialization(self):
        registry = SchemaRegistry()
        assert registry is not None

    def test_artifact_type_enum(self):
        assert ArtifactType.AGENT.value == "agent"
        assert ArtifactType.SKILL.value == "skill"


class TestSchemaValidator:
    @pytest.fixture
    def validator(self) -> SchemaValidator:
        return SchemaValidator(registry=MagicMock())

    def test_validate(self, validator):
        doc = {"agent": {"name": "test-agent"}}
        result = validator.validate("agent", doc)
        assert isinstance(result, ValidationResult)

    def test_validate_invalid(self, validator):
        result = validator.validate("agent", {"name": "test"})
        assert isinstance(result, ValidationResult)


class TestValidationResult:
    def test_validation_result(self):
        result = ValidationResult()
        assert result.is_valid
        assert len(result.errors) == 0

    def test_with_errors(self):
        error = ValidationError(path="name", message="Missing required", severity=Severity.ERROR)
        result = ValidationResult(errors=[error])
        assert not result.is_valid

    def test_error_count(self):
        errors = [
            ValidationError(path="a", message="e1"),
            ValidationError(path="b", message="e2", severity=Severity.WARNING),
        ]
        result = ValidationResult(errors=errors)
        assert len(result.errors) == 2


class TestSchemaMigrator:
    def test_detect_version(self):
        assert detect_schema_version({"schema_version": "1.0.0"}) == "1.0.0"

    def test_detect_version_no_version(self):
        assert detect_schema_version({"name": "test"}) is not None

    def test_create_migration_plan(self):
        plan = MigrationPlan(from_version="0.9.0", to_version="1.0.0")
        assert plan.from_version == "0.9.0"

    def test_migration_step_rename(self):
        step = MigrationStep(
            action=MigrationAction.RENAME_FIELD,
            path="old_name",
            new_value="new_name",
        )
        doc = {"old_name": "test", "other": "value"}
        result = step.apply(doc)
        assert "new_name" in result
        assert result["new_name"] == "test"

    def test_migration_step_add(self):
        step = MigrationStep(
            action=MigrationAction.ADD_FIELD,
            path="new_field",
            new_value="default",
        )
        doc = {"existing": "value"}
        result = step.apply(doc)
        assert result["new_field"] == "default"

    def test_migration_step_remove(self):
        step = MigrationStep(
            action=MigrationAction.REMOVE_FIELD,
            path="to_remove",
        )
        doc = {"to_remove": "value", "keep": "value"}
        result = step.apply(doc)
        assert "to_remove" not in result
        assert "keep" in result

    def test_field_rename(self):
        fr = FieldRename(
            old_path="skill_ref",
            new_path="skill_id",
            description="Renamed for consistency",
        )
        assert fr.old_path == "skill_ref"

    def test_migration_plan_apply(self):
        step = MigrationStep(
            action=MigrationAction.ADD_FIELD,
            path="version",
            new_value="2.0.0",
        )
        plan = MigrationPlan(from_version="1.0.0", to_version="2.0.0", steps=[step])
        doc = {"name": "test"}
        result = plan.apply(doc)
        assert result["version"] == "2.0.0"
