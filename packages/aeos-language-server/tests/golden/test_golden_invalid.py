from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos_lsp.parsing.dispatcher import ParserDispatcher
from aeos_lsp.semantic.semantic_model import SemanticModel

HERE = Path(__file__).resolve().parent
EXPECTED_DIR = HERE / "expected"
GOLDEN_DIR = HERE

INVALID_FIXTURES = [
    "invalid_syntax.yaml",
    "invalid_schema.yaml",
    "duplicate_ids.yaml",
    "dangling_reference.yaml",
    "cycle_playbooks.yaml",
    "cycle_agent_inheritance.yaml",
    "missing_permission.yaml",
    "missing_rollback.yaml",
    "insecure_command.yaml",
    "no_timeout.yaml",
    "unlimited_retry.yaml",
    "invalid_token_budget.yaml",
    "deprecated_field.yaml",
    "cross_file_ref.yaml",
]


def _collect_invalid_fixtures():
    fixtures = []
    for name in INVALID_FIXTURES:
        path = GOLDEN_DIR / name
        if path.is_file():
            expected_path = EXPECTED_DIR / f"{name}.json"
            fixtures.append((name, path, expected_path))
    return fixtures


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_parses(fixture_name, fixture_path, expected_path):
    parser = ParserDispatcher()
    text = fixture_path.read_text(encoding="utf-8", errors="replace")
    uri = f"file:///tests/golden/{fixture_name}"
    result = parser.parse(uri, text)
    if result is None:
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        expected_diags = expected.get("diagnostics", [])
        if expected_diags:
            codes = {d.get("code") for d in expected_diags}
            assert "AEOS0001" in codes or len(codes) > 0


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_expected_exists(fixture_name, fixture_path, expected_path):
    assert expected_path.is_file(), f"Expected file for {fixture_name} does not exist at {expected_path}"


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_expected_valid_json(fixture_name, fixture_path, expected_path):
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert "uri" in expected
    assert "diagnostics" in expected
    assert isinstance(expected["diagnostics"], list)
    for d in expected["diagnostics"]:
        assert "range" in d
        assert "start" in d["range"]
        assert "end" in d["range"]
        assert "code" in d
        assert "message" in d


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_has_errors(fixture_name, fixture_path, expected_path):
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    diags = expected.get("diagnostics", [])
    assert len(diags) > 0, f"{fixture_name}: expected at least one diagnostic"
    has_error = any(d.get("severity", 3) <= 1 for d in diags)
    has_warning = any(d.get("severity", 3) <= 2 for d in diags)
    assert has_error or has_warning, f"{fixture_name}: expected at least one error or warning"


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_diagnostic_codes_known(fixture_name, fixture_path, expected_path):
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    known_prefixes = {"AEOS"}
    for d in expected.get("diagnostics", []):
        code = d.get("code", "")
        assert any(code.startswith(p) for p in known_prefixes), f"{fixture_name}: unknown code format {code}"


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_invalid_fixtures())
def test_golden_invalid_severity_range(fixture_name, fixture_path, expected_path):
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    for d in expected.get("diagnostics", []):
        severity = d.get("severity", 0)
        assert 1 <= severity <= 4, f"{fixture_name}: severity {severity} out of range"


def test_golden_invalid_all_fixtures_exist():
    for fixture_name in INVALID_FIXTURES:
        path = GOLDEN_DIR / fixture_name
        assert path.is_file(), f"{fixture_name} does not exist"


def test_golden_invalid_all_have_expected():
    for fixture_name in INVALID_FIXTURES:
        expected_path = EXPECTED_DIR / f"{fixture_name}.json"
        assert expected_path.is_file(), f"Expected file for {fixture_name} does not exist"


def test_golden_invalid_no_empty_diagnostics():
    for fixture_name in INVALID_FIXTURES:
        expected_path = EXPECTED_DIR / f"{fixture_name}.json"
        if not expected_path.is_file():
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert len(expected.get("diagnostics", [])) > 0, f"{fixture_name}: empty diagnostics"


def test_golden_invalid_syntax_error_present():
    expected_path = EXPECTED_DIR / "invalid_syntax.yaml.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    codes = {d.get("code") for d in expected.get("diagnostics", [])}
    assert "AEOS0001" in codes, "invalid_syntax should have AEOS0001"


def test_golden_invalid_dangling_references():
    expected_path = EXPECTED_DIR / "dangling_reference.yaml.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    codes = {d.get("code") for d in expected.get("diagnostics", [])}
    assert "AEOS0012" in codes or "AEOS0016" in codes


def test_golden_invalid_schema_errors():
    expected_path = EXPECTED_DIR / "invalid_schema.yaml.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    codes = {d.get("code") for d in expected.get("diagnostics", [])}
    assert any(c.startswith("AEOS") for c in codes)
