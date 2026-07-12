from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)


class Severity(int, Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    HINT = 4


@dataclass
class ValidationError:
    message: str
    path: str = ""
    range: tuple[int, int, int, int] | None = None
    code: str = ""
    severity: Severity = Severity.ERROR
    schema_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "path": self.path,
            "range": self.range,
            "code": self.code,
            "severity": self.severity.value,
            "schema_path": self.schema_path,
        }


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    infos: list[ValidationError] = field(default_factory=list)
    hints: list[ValidationError] = field(default_factory=list)

    @property
    def all(self) -> list[ValidationError]:
        return self.errors + self.warnings + self.infos + self.hints

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def merge(self, other: ValidationResult) -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.infos.extend(other.infos)
        self.hints.extend(other.hints)


CustomValidator = Callable[[str, dict[str, Any], str], list[ValidationError]]


class SchemaValidator:
    SUPPORTED_DRAFTS = {
        "https://json-schema.org/draft/2020-12/schema",
        "https://json-schema.org/draft/2019-09/schema",
        "https://json-schema.org/draft/07/schema",
        "https://json-schema.org/draft-07/schema#",
        "https://json-schema.org/draft-06/schema",
        "https://json-schema.org/draft-06/schema#",
        "https://json-schema.org/draft-04/schema",
        "https://json-schema.org/draft-04/schema#",
        "http://json-schema.org/draft-07/schema#",
        "http://json-schema.org/draft-06/schema#",
        "http://json-schema.org/draft-04/schema#",
    }

    def __init__(self, registry: Any | None = None) -> None:
        self._custom_validators: dict[str, list[CustomValidator]] = {}
        self._external_validator: Any = None
        self._registry = registry
        self._init_external()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(
        self,
        artifact_type: str,
        data: dict[str, Any],
        uri: str = "",
    ) -> ValidationResult:
        result = ValidationResult()

        schema = self._resolve_schema(artifact_type)
        if schema is None:
            result.errors.append(
                ValidationError(
                    message=f"No schema found for artifact type '{artifact_type}'",
                    code="schema-not-found",
                    severity=Severity.ERROR,
                )
            )
            return result

        return self.validate_against(schema, data, uri, artifact_type)

    def validate_against(
        self,
        schema: dict[str, Any],
        data: dict[str, Any],
        uri: str = "",
        artifact_type: str = "",
    ) -> ValidationResult:
        result = ValidationResult()

        if not isinstance(data, dict):
            result.errors.append(
                ValidationError(
                    message="Root value must be a JSON object",
                    code="type-error",
                    severity=Severity.ERROR,
                )
            )
            return result

        draft = schema.get("$schema", "")
        if draft and draft not in self.SUPPORTED_DRAFTS:
            result.warnings.append(
                ValidationError(
                    message=f"Unsupported schema draft: {draft}",
                    code="unsupported-draft",
                    severity=Severity.WARNING,
                )
            )

        if self._external_validator is not None:
            try:
                ext_result = self._validate_external(schema, data, uri)
                result.merge(ext_result)
            except Exception as e:
                logger.debug("External validation failed, falling back to basic: %s", e)
                basic = self._validate_basic(schema, data, "", artifact_type)
                result.merge(basic)
        else:
            basic = self._validate_basic(schema, data, "", artifact_type)
            result.merge(basic)

        custom_rules = self._custom_validators.get(artifact_type, [])
        custom_rules.extend(self._custom_validators.get("*", []))
        for validator in custom_rules:
            try:
                errors = validator(artifact_type, data, uri)
                for err in errors:
                    if err.severity == Severity.ERROR:
                        result.errors.append(err)
                    elif err.severity == Severity.WARNING:
                        result.warnings.append(err)
                    elif err.severity == Severity.INFO:
                        result.infos.append(err)
                    else:
                        result.hints.append(err)
            except Exception as e:
                logger.exception("Custom validator failed for '%s': %s", artifact_type, e)

        return result

    def register_custom_validator(
        self,
        artifact_type: str,
        validator: CustomValidator,
    ) -> None:
        if artifact_type not in self._custom_validators:
            self._custom_validators[artifact_type] = []
        self._custom_validators[artifact_type].append(validator)

    def register_global_validator(self, validator: CustomValidator) -> None:
        self.register_custom_validator("*", validator)

    # ------------------------------------------------------------------
    # External validation (jsonschema library)
    # ------------------------------------------------------------------

    def _init_external(self) -> None:
        try:
            import jsonschema  # type: ignore[import-untyped]
            self._external_validator = jsonschema
        except ImportError:
            self._external_validator = None

    def _validate_external(
        self,
        schema: dict[str, Any],
        data: dict[str, Any],
        uri: str,
    ) -> ValidationResult:
        result = ValidationResult()
        validator_cls = self._pick_validator_cls(schema.get("$schema", ""))
        try:
            v = validator_cls(schema)
            for error in v.iter_errors(data):
                result.errors.append(self._convert_external_error(error, uri))
        except Exception as e:
            result.errors.append(
                ValidationError(
                    message=f"External validation error: {e}",
                    code="external-validation-error",
                    severity=Severity.ERROR,
                )
            )
        return result

    def _pick_validator_cls(self, draft: str) -> Any:
        if self._external_validator is None:
            raise RuntimeError("jsonschema not available")
        if "2020-12" in draft:
            return self._external_validator.Draft202012Validator
        if "2019-09" in draft:
            return self._external_validator.Draft201909Validator
        if "draft-07" in draft or "draft/07" in draft:
            return self._external_validator.Draft7Validator
        if "draft-06" in draft or "draft/06" in draft:
            return self._external_validator.Draft6Validator
        if "draft-04" in draft or "draft/04" in draft:
            return self._external_validator.Draft4Validator
        return self._external_validator.Draft202012Validator

    @staticmethod
    def _convert_external_error(error: Any, uri: str) -> ValidationError:
        path_parts = list(error.absolute_path)
        path = "/" + "/".join(str(p) for p in path_parts) if path_parts else "/"
        return ValidationError(
            message=error.message,
            path=path,
            code=error.validator if hasattr(error, "validator") else "validation-error",
            severity=Severity.ERROR,
            schema_path="/" + "/".join(str(p) for p in error.absolute_schema_path) if hasattr(error, "absolute_schema_path") else "",
        )

    # ------------------------------------------------------------------
    # Basic built-in validation
    # ------------------------------------------------------------------

    def _validate_basic(
        self,
        schema: dict[str, Any],
        data: dict[str, Any],
        path: str = "",
        artifact_type: str = "",
    ) -> ValidationResult:
        return self._validate_node(schema, data, path)

    def _validate_node(
        self,
        schema: Any,
        data: Any,
        path: str,
    ) -> ValidationResult:
        result = ValidationResult()

        if not isinstance(schema, dict):
            return result

        if "$ref" in schema:
            return result

        if schema.get("type") == "object" and isinstance(data, dict):
            self._validate_object(schema, data, path, result)
        elif schema.get("type") == "array" and isinstance(data, list):
            self._validate_array(schema, data, path, result)
        elif "type" in schema and schema["type"] not in ("object", "array"):
            self._validate_primitive_type(schema, data, path, result)

        self._validate_enums(schema, data, path, result)
        self._validate_pattern(schema, data, path, result)
        self._validate_min_max(schema, data, path, result)
        self._validate_format(schema, data, path, result)
        self._validate_logical(schema, data, path, result)

        return result

    def _validate_object(
        self,
        schema: dict[str, Any],
        data: dict[str, Any],
        path: str,
        result: ValidationResult,
    ) -> None:
        if not isinstance(data, dict):
            result.errors.append(
                ValidationError(
                    message=f"Expected object, got {type(data).__name__}",
                    path=path,
                    code="type-error",
                    severity=Severity.ERROR,
                )
            )
            return

        properties = schema.get("properties", {})
        additional_props = schema.get("additionalProperties", True)
        pattern_props = schema.get("patternProperties", {})

        if additional_props is False:
            allowed = set(properties.keys())
            for key in data:
                matched = key in allowed
                if not matched:
                    for pat in pattern_props:
                        if re.search(pat, key):
                            matched = True
                            break
                if not matched:
                    result.errors.append(
                        ValidationError(
                            message=f"Additional property '{key}' not allowed",
                            path=f"{path}/{key}",
                            code="additional-properties",
                            severity=Severity.ERROR,
                        )
                    )

        required = schema.get("required", [])
        for req_key in required:
            if req_key not in data:
                result.errors.append(
                    ValidationError(
                        message=f"Required property '{req_key}' is missing",
                        path=f"{path}/{req_key}",
                        code="required",
                        severity=Severity.ERROR,
                    )
                )

        dependencies = schema.get("dependencies", {})
        for key, deps in dependencies.items():
            if key in data:
                if isinstance(deps, list):
                    for dep_key in deps:
                        if dep_key not in data:
                            result.errors.append(
                                ValidationError(
                                    message=f"Property '{key}' requires '{dep_key}'",
                                    path=f"{path}/{dep_key}",
                                    code="dependency",
                                    severity=Severity.ERROR,
                                )
                            )
                elif isinstance(deps, dict):
                    sub = self._validate_node(deps, data, path)
                    result.merge(sub)

        for key, prop_schema in properties.items():
            if key in data:
                sub = self._validate_node(prop_schema, data[key], f"{path}/{key}")
                result.merge(sub)

        if not_schema := schema.get("not"):
            for key in data:
                sub_result = self._validate_node(not_schema, data[key], f"{path}/{key}")
                if sub_result.is_valid:
                    result.errors.append(
                        ValidationError(
                            message=f"Property '{key}' matches 'not' schema",
                            path=f"{path}/{key}",
                            code="not",
                            severity=Severity.ERROR,
                        )
                    )

    def _validate_array(
        self,
        schema: dict[str, Any],
        data: list[Any],
        path: str,
        result: ValidationResult,
    ) -> None:
        if not isinstance(data, list):
            result.errors.append(
                ValidationError(
                    message=f"Expected array, got {type(data).__name__}",
                    path=path,
                    code="type-error",
                )
            )
            return

        if "minItems" in schema and len(data) < schema["minItems"]:
            result.errors.append(
                ValidationError(
                    message=f"Array has {len(data)} items, minimum is {schema['minItems']}",
                    path=path,
                    code="min-items",
                )
            )

        if "maxItems" in schema and len(data) > schema["maxItems"]:
            result.errors.append(
                ValidationError(
                    message=f"Array has {len(data)} items, maximum is {schema['maxItems']}",
                    path=path,
                    code="max-items",
                )
            )

        if "uniqueItems" in schema and schema["uniqueItems"]:
            seen: list[Any] = []
            for i, item in enumerate(data):
                if item in seen:
                    result.errors.append(
                        ValidationError(
                            message=f"Duplicate item at index {i}",
                            path=f"{path}/{i}",
                            code="unique-items",
                        )
                    )
                else:
                    seen.append(item)

        if "prefixItems" in schema:
            prefix = schema["prefixItems"]
            for i in range(min(len(data), len(prefix))):
                sub = self._validate_node(prefix[i], data[i], f"{path}/{i}")
                result.merge(sub)

        if "items" in schema:
            items_schema = schema["items"]
            if isinstance(items_schema, dict):
                for i in range(len(data)):
                    sub = self._validate_node(items_schema, data[i], f"{path}/{i}")
                    result.merge(sub)
            elif isinstance(items_schema, list):
                for i in range(min(len(data), len(items_schema))):
                    sub = self._validate_node(items_schema[i], data[i], f"{path}/{i}")
                    result.merge(sub)

        if "contains" in schema:
            contains_schema = schema["contains"]
            found = False
            for i, item in enumerate(data):
                sub = self._validate_node(contains_schema, item, f"{path}/{i}")
                if sub.is_valid:
                    found = True
                    break
            if not found and data:
                result.errors.append(
                    ValidationError(
                        message="No item matches 'contains' schema",
                        path=path,
                        code="contains",
                    )
                )

    def _validate_primitive_type(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        expected = schema["type"]
        actual = self._typeof(data)
        if not self._type_matches(expected, actual):
            result.errors.append(
                ValidationError(
                    message=f"Expected type '{expected}', got '{actual}'",
                    path=path,
                    code="type-error",
                )
            )

        if "const" in schema and data != schema["const"]:
            result.errors.append(
                ValidationError(
                    message=f"Expected const value {schema['const']!r}, got {data!r}",
                    path=path,
                    code="const",
                )
            )

    def _validate_enums(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        if "enum" not in schema:
            return
        if data not in schema["enum"]:
            result.errors.append(
                ValidationError(
                    message=f"Value {data!r} not in enum {schema['enum']}",
                    path=path,
                    code="enum",
                )
            )

    def _validate_pattern(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        if "pattern" not in schema:
            return
        if not isinstance(data, str):
            return
        if not re.search(schema["pattern"], data):
            result.errors.append(
                ValidationError(
                    message=f"String does not match pattern '{schema['pattern']}'",
                    path=path,
                    code="pattern",
                )
            )

    def _validate_min_max(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        if isinstance(data, (int, float)):
            if "minimum" in schema and data < schema["minimum"]:
                result.errors.append(
                    ValidationError(
                        message=f"Value {data} is less than minimum {schema['minimum']}",
                        path=path,
                        code="minimum",
                    )
                )
            if "maximum" in schema and data > schema["maximum"]:
                result.errors.append(
                    ValidationError(
                        message=f"Value {data} is greater than maximum {schema['maximum']}",
                        path=path,
                        code="maximum",
                    )
                )
            if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
                result.errors.append(
                    ValidationError(
                        message=f"Value {data} is not strictly greater than {schema['exclusiveMinimum']}",
                        path=path,
                        code="exclusive-minimum",
                    )
                )
            if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
                result.errors.append(
                    ValidationError(
                        message=f"Value {data} is not strictly less than {schema['exclusiveMaximum']}",
                        path=path,
                        code="exclusive-maximum",
                    )
                )

        if isinstance(data, str):
            if "minLength" in schema and len(data) < schema["minLength"]:
                result.errors.append(
                    ValidationError(
                        message=f"String length {len(data)} is less than minimum {schema['minLength']}",
                        path=path,
                        code="min-length",
                    )
                )
            if "maxLength" in schema and len(data) > schema["maxLength"]:
                result.errors.append(
                    ValidationError(
                        message=f"String length {len(data)} exceeds maximum {schema['maxLength']}",
                        path=path,
                        code="max-length",
                    )
                )

        if isinstance(data, (int, float)) and "multipleOf" in schema:
            mult = schema["multipleOf"]
            if mult != 0 and data % mult != 0:
                result.errors.append(
                    ValidationError(
                        message=f"Value {data} is not a multiple of {mult}",
                        path=path,
                        code="multiple-of",
                    )
                )

    def _validate_format(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        fmt = schema.get("format")
        if fmt is None or not isinstance(data, str):
            return

        validators: dict[str, Callable[[str], bool]] = {
            "date": lambda s: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", s)),
            "date-time": lambda s: bool(re.match(
                r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$", s
            )),
            "time": lambda s: bool(re.match(r"^\d{2}:\d{2}:\d{2}(\.\d+)?$", s)),
            "email": lambda s: bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s)),
            "uri": lambda s: bool(re.match(r"^[a-z][a-z0-9+\-.]*://", s)),
            "uuid": lambda s: bool(re.match(
                r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", s, re.I
            )),
            "hostname": lambda s: bool(re.match(
                r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$", s
            )),
            "ipv4": lambda s: bool(re.match(
                r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", s
            )) and all(0 <= int(x) <= 255 for x in s.split(".")),
            "ipv6": lambda s: bool(re.match(
                r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$", s
            )),
        }

        validator = validators.get(fmt)
        if validator is not None and not validator(data):
            result.errors.append(
                ValidationError(
                    message=f"String does not match format '{fmt}'",
                    path=path,
                    code="format",
                )
            )

    def _validate_logical(
        self,
        schema: dict[str, Any],
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        if "allOf" in schema:
            for i, subschema in enumerate(schema["allOf"]):
                sub = self._validate_node(subschema, data, f"{path}/allOf/{i}")
                result.merge(sub)

        if "anyOf" in schema:
            any_valid = False
            for i, subschema in enumerate(schema["anyOf"]):
                sub = self._validate_node(subschema, data, f"{path}/anyOf/{i}")
                if sub.is_valid:
                    any_valid = True
                    break
            if not any_valid:
                result.errors.append(
                    ValidationError(
                        message="Data does not match any schema in 'anyOf'",
                        path=path,
                        code="any-of",
                    )
                )

        if "oneOf" in schema:
            valid_count = 0
            for i, subschema in enumerate(schema["oneOf"]):
                sub = self._validate_node(subschema, data, f"{path}/oneOf/{i}")
                if sub.is_valid:
                    valid_count += 1
            if valid_count != 1:
                result.errors.append(
                    ValidationError(
                        message=f"Data matches {valid_count} schemas in 'oneOf' (expected exactly 1)",
                        path=path,
                        code="one-of",
                    )
                )

        if "if" in schema:
            if_result = self._validate_node(schema["if"], data, f"{path}/if")
            if if_result.is_valid:
                then_schema = schema.get("then")
                if then_schema is not None:
                    then_result = self._validate_node(then_schema, data, f"{path}/then")
                    result.merge(then_result)
            else:
                else_schema = schema.get("else")
                if else_schema is not None:
                    else_result = self._validate_node(else_schema, data, f"{path}/else")
                    result.merge(else_result)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _typeof(value: Any) -> str:
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        if isinstance(value, float):
            return "number"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "object"
        if value is None:
            return "null"
        return type(value).__name__

    @staticmethod
    def _type_matches(expected: str, actual: str) -> bool:
        if expected == actual:
            return True
        if expected == "number" and actual == "integer":
            return True
        return False

    def _resolve_schema(self, artifact_type: str) -> dict[str, Any] | None:
        if self._registry is not None:
            return self._registry.get_schema(artifact_type)
        from aeos_lsp.schemas.registry import SchemaRegistry

        reg = SchemaRegistry()
        reg.register_builtins()
        return reg.get_schema(artifact_type)
