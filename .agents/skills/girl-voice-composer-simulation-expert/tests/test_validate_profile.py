#!/usr/bin/env python3
"""Tests for the voice profile validator.

Run: python tests/test_validate_profile.py
Exit code 0 = all tests passed.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import validate_profile  # noqa: E402


def _write_tmp(data: dict) -> Path:
    tmp = Path(tempfile.mkdtemp()) / "voice_params.json"
    tmp.write_text(json.dumps(data), encoding="utf-8")
    return tmp


def _valid_profile() -> dict:
    example = SKILL_ROOT / "templates" / "example_voice_params.json"
    return json.loads(example.read_text(encoding="utf-8"))


def test_example_is_valid() -> None:
    path = _write_tmp(_valid_profile())
    errors = validate_profile.validate(path)
    assert errors == [], f"expected valid, got: {errors}"


def test_rejects_non_fictional() -> None:
    p = _valid_profile()
    p["generic_and_fictional"] = False
    errors = validate_profile.validate(_write_tmp(p))
    assert any("generic_and_fictional" in e for e in errors), errors


def test_rejects_mean_out_of_range() -> None:
    p = _valid_profile()
    p["pitch"]["mean_f0_hz"] = 999  # above schema max and outside min/max
    errors = validate_profile.validate(_write_tmp(p))
    assert errors, "expected errors for out-of-range mean_f0_hz"


def test_rejects_mean_outside_min_max() -> None:
    p = _valid_profile()
    p["pitch"]["mean_f0_hz"] = 210
    p["pitch"]["min_f0_hz"] = 250
    p["pitch"]["max_f0_hz"] = 300
    errors = validate_profile.validate(_write_tmp(p))
    assert any("must lie within" in e for e in errors), errors


def test_rejects_bad_age() -> None:
    p = _valid_profile()
    p["target_age"] = 12
    errors = validate_profile.validate(_write_tmp(p))
    assert errors, "expected errors for out-of-band age"


def test_mapped_requires_controls() -> None:
    p = _valid_profile()
    p["engine"] = {"id": "someEngine", "mapping_mode": "mapped"}
    errors = validate_profile.validate(_write_tmp(p))
    assert any("controls" in e for e in errors), errors


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {t.__name__}: {exc}", file=sys.stderr)
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_run())
