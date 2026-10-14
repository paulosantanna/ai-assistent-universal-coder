#!/usr/bin/env python3
"""Deterministic validator for a generic female child voice profile.

Validates a voice_params.json file against the JSON schema plus a few
cross-field safety/consistency rules that a plain schema cannot express.

Usage:
    python scripts/validate_profile.py <path-to-voice_params.json>

Exit codes:
    0  valid
    1  invalid (blocking findings printed to stderr)
    2  usage / IO error

This validator performs NO audio processing and reads NO recordings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "voice_profile.schema.json"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _validate_with_jsonschema(profile: dict, schema: dict) -> list[str]:
    """Use jsonschema if available; otherwise fall back to minimal checks."""
    try:
        import jsonschema  # type: ignore

        validator = jsonschema.Draft7Validator(schema)
        return [
            f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
            for err in sorted(validator.iter_errors(profile), key=lambda e: list(e.path))
        ]
    except ModuleNotFoundError:
        return _fallback_required_check(profile, schema)


def _fallback_required_check(profile: dict, schema: dict) -> list[str]:
    """Minimal required-key check when jsonschema is not installed."""
    errors: list[str] = []
    for key in schema.get("required", []):
        if key not in profile:
            errors.append(f"<root>: missing required property '{key}'")
    return errors


def _cross_field_rules(profile: dict) -> list[str]:
    """Safety and consistency rules beyond the schema."""
    errors: list[str] = []

    if profile.get("generic_and_fictional") is not True:
        errors.append(
            "generic_and_fictional: must be true (profile must be generic/fictional, "
            "not an impersonation of a real identifiable child)"
        )

    pitch = profile.get("pitch")
    if isinstance(pitch, dict):
        lo = pitch.get("min_f0_hz")
        hi = pitch.get("max_f0_hz")
        mean = pitch.get("mean_f0_hz")
        if all(isinstance(v, (int, float)) for v in (lo, hi, mean)):
            if not (lo <= mean <= hi):
                errors.append(
                    f"pitch: mean_f0_hz ({mean}) must lie within "
                    f"[min_f0_hz={lo}, max_f0_hz={hi}]"
                )
            if lo > hi:
                errors.append("pitch: min_f0_hz cannot exceed max_f0_hz")

    engine = profile.get("engine")
    if isinstance(engine, dict) and engine.get("mapping_mode") == "mapped":
        if not engine.get("controls"):
            errors.append(
                "engine: mapping_mode 'mapped' requires a non-empty 'controls' map"
            )

    return errors


def validate(path: Path) -> list[str]:
    profile = _load_json(path)
    schema = _load_json(SCHEMA_PATH)
    return _validate_with_jsonschema(profile, schema) + _cross_field_rules(profile)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python validate_profile.py <path-to-voice_params.json>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        errors = validate(path)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {path}: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
