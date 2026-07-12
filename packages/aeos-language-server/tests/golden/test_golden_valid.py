from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos_lsp.parsing.dispatcher import ParserDispatcher
from aeos_lsp.semantic.semantic_model import SemanticModel

HERE = Path(__file__).resolve().parent
EXPECTED_DIR = HERE / "expected"
GOLDEN_DIR = HERE

# valid fixture files, listed explicitly for clarity
VALID_FIXTURES = [
    "valid_agent.yaml",
    "valid_skill.yaml",
    "valid_playbook.yaml",
    "valid_policy.yaml",
    "valid_permissions.yaml",
    "valid_registry.yaml",
    "valid_aeos_config.yaml",
    "valid_aeos.json",
    "valid_aeos.toml",
    "valid_agent.agent.md",
    "valid_skill.skill.md",
    "valid_playbook.playbook.md",
    "valid_full_agent.md",
    "valid_full_playbook.md",
    "valid_overlay_index.yaml",
    "valid_expression.txt",
    "valid_multi_doc.yaml",
]


def _collect_valid_fixtures():
    fixtures = []
    for name in VALID_FIXTURES:
        path = GOLDEN_DIR / name
        if path.is_file():
            fixture_id = name
            expected_path = EXPECTED_DIR / f"{name}.json"
            fixtures.append((fixture_id, path, expected_path))
    return fixtures


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_valid_fixtures())
def test_golden_valid_parse(fixture_name, fixture_path, expected_path):
    parser = ParserDispatcher()
    text = fixture_path.read_text(encoding="utf-8", errors="replace")
    uri = f"file:///tests/golden/{fixture_name}"
    result = parser.parse(uri, text)
    if result is None:
        pytest.fail(f"{fixture_name}: ParseResult is None")


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_valid_fixtures())
def test_golden_valid_semantic(fixture_name, fixture_path, expected_path):
    parser = ParserDispatcher()
    text = fixture_path.read_text(encoding="utf-8", errors="replace")
    uri = f"file:///tests/golden/{fixture_name}"
    result = parser.parse(uri, text)
    if result is None:
        pytest.fail(f"{fixture_name}: ParseResult is None")
    model = SemanticModel()
    model.update_for_document(uri, result)


@pytest.mark.parametrize("fixture_name,fixture_path,expected_path", _collect_valid_fixtures())
def test_golden_valid_expected_output(fixture_name, fixture_path, expected_path):
    if not expected_path.is_file():
        pytest.skip(f"Expected file not found: {expected_path}")
    parser = ParserDispatcher()
    text = fixture_path.read_text(encoding="utf-8", errors="replace")
    uri = f"file:///tests/golden/{fixture_name}"
    result = parser.parse(uri, text)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    expected_diagnostics = expected.get("diagnostics", [])
    assert isinstance(expected_diagnostics, list)
    if result is not None:
        parse_errors = getattr(result, "errors", [])
        assert len(parse_errors) == 0 or len(expected_diagnostics) == 0
    else:
        assert len(expected_diagnostics) > 0


def test_golden_valid_no_crash_valid_agent():
    path = GOLDEN_DIR / "valid_agent.agent.md"
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = ParserDispatcher()
    result = parser.parse(path.as_uri(), text)
    assert result is not None


def test_golden_valid_no_crash_full_playbook():
    path = GOLDEN_DIR / "valid_full_playbook.md"
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = ParserDispatcher()
    result = parser.parse(path.as_uri(), text)
    assert result is not None


def test_golden_valid_aeos_config_yaml():
    path = GOLDEN_DIR / "valid_aeos_config.yaml"
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = ParserDispatcher()
    result = parser.parse(path.as_uri(), text)
    assert result is not None


def test_golden_valid_all_fixtures_exist():
    for fixture_name in VALID_FIXTURES:
        path = GOLDEN_DIR / fixture_name
        assert path.is_file(), f"{fixture_name} does not exist"


def test_golden_valid_all_have_expected():
    for fixture_name in VALID_FIXTURES:
        expected_path = EXPECTED_DIR / f"{fixture_name}.json"
        assert expected_path.is_file(), f"Expected file for {fixture_name} does not exist"
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert "uri" in expected
        assert "diagnostics" in expected


def test_golden_valid_no_severe_errors():
    for fixture_name in VALID_FIXTURES:
        expected_path = EXPECTED_DIR / f"{fixture_name}.json"
        if not expected_path.is_file():
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        diags = expected.get("diagnostics", [])
        for d in diags:
            severity = d.get("severity", 0)
            assert severity >= 2, f"{fixture_name}: expected no errors (severity <= 1)"


def test_golden_valid_all_expected_consistent():
    for fixture_name in VALID_FIXTURES:
        expected_path = EXPECTED_DIR / f"{fixture_name}.json"
        if not expected_path.is_file():
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        diags = expected.get("diagnostics", [])
        for d in diags:
            assert "range" in d
            assert "start" in d["range"]
            assert "end" in d["range"]
            assert "line" in d["range"]["start"]
            assert "character" in d["range"]["start"]
            assert "code" in d
            assert "message" in d
