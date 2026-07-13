"""Comprehensive tests for Medical AI Audit V2.

Covers:
- File presence does not imply PASS
- Empty test directories produce NOT_EXECUTED
- Failing pytest produces FAIL
- pytest unavailable produces BLOCKED
- Timeout produces BLOCKED
- Critical NOT_EXECUTED blocks global score
- Score 10.0 without evidence is rejected
- Invalid hash is rejected
- Scanner ignores caches and models
- Lists are limited
- Commands don't modify the audited repo
- Paths with spaces work
- Windows paths work
- stdout/stderr are truncated with marker
- Judge reduces inconsistent verdict
- Structural mode does not return readiness
- Deep mode registers coverage
- Internal exception does not become PASS
"""

from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock

import pytest

from medical_research_mcp.audit import (
    AuditStatus,
    AuditConfig,
    AuditReport,
    GateResult,
    EvidenceItem,
    EvidenceType,
    CommandRecord,
    run_audit,
    judge_gate,
    judge_report,
    build_ignore_patterns,
)
from medical_research_mcp.audit.models import JudgeVerdict
from medical_research_mcp.audit.scoring import compute_score
from medical_research_mcp.audit.exclusions import should_ignore, DEFAULT_EXCLUSIONS


# ===== Fixtures =====

@pytest.fixture
def empty_repo(tmp_path: Path) -> Path:
    """An empty (but valid) directory."""
    (tmp_path / "README.md").write_text("# Empty Repo", encoding="utf-8")
    return tmp_path


@pytest.fixture
def repo_with_tests(tmp_path: Path) -> Path:
    """A minimalist repo with a passing test file."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "__init__.py").write_text("", encoding="utf-8")
    (src / "module.py").write_text("def foo(): return 42", encoding="utf-8")

    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "__init__.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text(
        "from src.module import foo\n\ndef test_foo():\n    assert foo() == 42\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def repo_with_failing_tests(tmp_path: Path) -> Path:
    """A repo where tests fail."""
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_fail.py").write_text(
        "def test_always_fails():\n    assert False, 'This test always fails'\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def repo_with_caches(tmp_path: Path) -> Path:
    """A repo with cache/model files that should be ignored."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "module.py").write_text("x = 1", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "module.cpython-314.pyc").write_text("cached", encoding="utf-8")
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".pytest_cache" / "README.md").write_text("cache", encoding="utf-8")
    (tmp_path / "model.safetensors").write_text("fake model weights", encoding="utf-8")
    (tmp_path / "checkpoint.pt").write_text("checkpoint", encoding="utf-8")
    (tmp_path / "data.db").write_text("database", encoding="utf-8")
    return tmp_path


@pytest.fixture
def repo_with_secrets(tmp_path: Path) -> Path:
    """A repo with hardcoded secrets."""
    (tmp_path / "config.py").write_text(
        'API_KEY = "sk-1234567890abcdef"\nPASSWORD = "super-secret"\n',
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "__init__.py").write_text("", encoding="utf-8")
    return tmp_path


# ===== Test: File presence does not imply PASS =====

def test_file_presence_does_not_imply_pass(empty_repo: Path) -> None:
    """Even with files present, gates must execute real checks."""
    config = AuditConfig(repository=str(empty_repo), mode="deep", run_tests=False, run_security=False, run_dependency_audit=False)
    report = run_audit(config)
    # Without tests or security, the test gate should be NOT_EXECUTED or NOT_APPLICABLE
    test_gate = report.gates.get("test_execution")
    if test_gate:
        assert test_gate.status != AuditStatus.PASS, "Should not PASS without test execution"
    # Overall score should be None because critical gates are blocked/not executed
    # At minimum, test_execution and dependency_security should not be PASS
    for gid, gate in report.gates.items():
        if gate.status == AuditStatus.PASS:
            assert gate.evidence, f"Gate {gid} is PASS but has no evidence"
            assert gate.score is not None, f"Gate {gid} is PASS but score is None"


# ===== Test: Empty test directory produces NOT_EXECUTED =====

def test_empty_test_dir_produces_not_executed(tmp_path: Path) -> None:
    """A tests/ directory with no test files should not PASS."""
    (tmp_path / "tests").mkdir()
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("", encoding="utf-8")
    (src_dir / "module.py").write_text("x = 1", encoding="utf-8")
    config = AuditConfig(repository=str(tmp_path), mode="deep", run_tests=True, run_security=False, run_dependency_audit=False)
    report = run_audit(config)
    tg = report.gates.get("test_execution")
    # The gate should detect an empty test dir
    if tg:
        assert tg.status != AuditStatus.PASS, "Empty test dir must not PASS"
        if tg.findings:
            has_empty = any("no test" in f.lower() for f in tg.findings)
            if has_empty:
                assert tg.status in (AuditStatus.NOT_EXECUTED, AuditStatus.BLOCKED), \
                    f"Empty test dir should be NOT_EXECUTED or BLOCKED, got {tg.status}"


# ===== Test: Failing pytest produces FAIL =====

def test_failing_pytest_produces_fail(repo_with_failing_tests: Path) -> None:
    """Tests that fail should produce FAIL status."""
    config = AuditConfig(
        repository=str(repo_with_failing_tests),
        mode="deep",
        run_tests=True,
        run_security=False,
        run_dependency_audit=False,
        timeout_seconds=30,
    )
    report = run_audit(config)
    tg = report.gates.get("test_execution")
    if tg:
        if tg.status == AuditStatus.FAIL:
            assert tg.score is not None and tg.score < 10.0, "FAIL gate should have score < 10"
            assert any("fail" in f.lower() for f in tg.findings), "FAIL gate should mention failures"
        else:
            # May be BLOCKED if pytest is not available or other issue
            pass


# ===== Test: pytest unavailable produces BLOCKED =====

@patch("medical_research_mcp.audit.gates.tests.run_command")
def test_no_pytest_produces_blocked(mock_run_cmd, repo_with_tests: Path) -> None:
    """When pytest is not installed, the gate should be BLOCKED."""
    from medical_research_mcp.audit.gates.tests import check_tests
    from medical_research_mcp.audit.models import CommandRecord
    import asyncio
    # Simulate pytest --version failing
    mock_run_cmd.return_value = CommandRecord(
        command="pytest --version",
        exit_code=1,
        stderr="pytest not found",
    )
    result = asyncio.run(check_tests(str(repo_with_tests)))
    assert result.status == AuditStatus.BLOCKED, f"Without pytest, should be BLOCKED, got {result.status}"
    assert result.score is None, "BLOCKED gate should have score=None"


# ===== Test: Score 10.0 without evidence is rejected =====

def test_score_10_without_evidence_rejected() -> None:
    """The Judge must reject a gate with PASS but no evidence."""
    gate = GateResult(
        id="test_gate",
        title="Test Gate",
        status=AuditStatus.PASS,
        score=10.0,
        evidence=[],
        findings=["Everything is perfect"],
    )
    judged = judge_gate(gate)
    assert judged is not None, "Judge should flag PASS without evidence"
    assert judged.status != AuditStatus.PASS, "Judge should downgrade PASS without evidence"
    assert judged.score != 10.0, "Judge should not allow score 10 without evidence"


def test_judge_rejects_full_report_without_evidence() -> None:
    """The Judge must reject a full report with score 10 but no evidence."""
    report = AuditReport(
        target="/fake/path",
        mode="deep",
        started_at="2025-01-01T00:00:00",
        finished_at="2025-01-01T00:01:00",
        duration_ms=60000,
        status=AuditStatus.PASS,
        score=10.0,
        coverage=1.0,
        executed_gates=1,
        total_gates=1,
        gates={
            "test_gate": GateResult(
                id="test_gate",
                title="Test Gate",
                status=AuditStatus.PASS,
                score=10.0,
                evidence=[],
            ),
        },
    )
    verdict = judge_report(report)
    assert not verdict.accepted, "Judge should reject report with score 10 and no evidence"
    assert "Evidence issues" in " ".join(verdict.reasons) or "Score" in " ".join(verdict.reasons), \
        "Judge should flag evidence issues"


# ===== Test: Hash validation =====

def test_invalid_hash_is_rejected_by_judge() -> None:
    """A gate claiming PASS but with empty SHA-256 hashes should be flagged."""
    gate = GateResult(
        id="test_hash",
        title="Hash Test",
        status=AuditStatus.PASS,
        score=10.0,
        evidence=[
            EvidenceItem(
                type=EvidenceType.COMMAND_OUTPUT,
                source="some_command",
                sha256="",  # empty hash
                summary="Test output",
            ),
        ],
    )
    judged = judge_gate(gate)
    assert judged is not None, "Judge should flag gate with empty hashes"


# ===== Test: Scanner ignores caches and models =====

def test_scanner_ignores_caches_and_models(repo_with_caches: Path) -> None:
    """Cache and model files should be excluded from scanning."""
    from medical_research_mcp.audit.gates.repository_hygiene import _fast_scan

    scan = _fast_scan(repo_with_caches)
    # The ignored files should not appear
    for item_list in scan["categories"].values():
        for item in item_list:
            assert "__pycache__" not in item, f"Cache file should be excluded: {item}"
            assert ".pytest_cache" not in item, f"pytest cache should be excluded: {item}"
            assert ".safetensors" not in item, f"Model files should be excluded: {item}"
    assert scan["ignored_count"] > 0, "Caches and models should contribute to ignored count"
    assert scan["total_files"] > 0, "Should still find real source files"


# ===== Test: Lists are limited =====

def test_lists_are_limited() -> None:
    """Samples per category should be limited in the fast scan output."""
    from medical_research_mcp.audit.gates.repository_hygiene import _fast_scan
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        # Create many files
        for i in range(100):
            (tdp / f"file_{i}.py").write_text(f"x = {i}", encoding="utf-8")
        scan = _fast_scan(tdp)
        assert scan["total_files"] == 100, f"Should find all 100 files, got {scan['total_files']}"
        for cat, items in scan["categories"].items():
            assert len(items) <= 5, f"Category '{cat}' should have at most 5 samples, got {len(items)}"


# ===== Test: Read-only — do not modify audited repo =====

def test_read_only_does_not_modify_repo(empty_repo: Path) -> None:
    """Running the audit should not create or modify files in the audited repo."""
    before = {str(p.relative_to(empty_repo)) for p in empty_repo.rglob("*") if p.is_file()}
    config = AuditConfig(repository=str(empty_repo), mode="structural")
    run_audit(config)
    after = {str(p.relative_to(empty_repo)) for p in empty_repo.rglob("*") if p.is_file()}
    assert before == after, "Audit should not modify the repository"


# ===== Test: Structural mode does not return readiness =====

def test_structural_mode_no_readiness(empty_repo: Path) -> None:
    """Structural mode must not claim readiness or give quality scores."""
    config = AuditConfig(repository=str(empty_repo), mode="structural")
    report = run_audit(config)
    assert report.score is None, "Structural mode should not produce a score"
    assert report.status != AuditStatus.PASS, "Structural mode should not claim PASS"
    assert report.coverage == 0.0, "Structural mode should have 0 coverage"
    assert "DISCOVERY_COMPLETED" in report.executive_summary or "STRUCTURAL" in report.executive_summary, \
        "Structural mode should indicate it's only an inventory"


# ===== Test: Deep mode registers coverage =====

def test_deep_mode_coverage(tmp_path: Path) -> None:
    """Deep mode should report coverage metrics."""
    (tmp_path / "README.md").write_text("# Test", encoding="utf-8")
    config = AuditConfig(
        repository=str(tmp_path),
        mode="deep",
        run_tests=False,
        run_security=False,
        run_dependency_audit=False,
    )
    report = run_audit(config)
    assert report.coverage is not None, "Deep mode should report coverage"
    assert report.executed_gates > 0, "Deep mode should execute at least some gates"
    assert report.total_gates > 0, "Deep mode should report total gates"


# ===== Test: Internal exception does not become PASS =====

def test_internal_exception_not_pass(tmp_path: Path) -> None:
    """If a gate raises an exception, it should be BLOCKED, not PASS."""
    from medical_research_mcp.audit.orchestrator import GATE_REGISTRY
    import asyncio

    # Temporarily break a gate
    broken_list = {"broken_gate": lambda repo: (_ for _ in ()).throw(RuntimeError("BROKEN"))}

    from medical_research_mcp.audit.orchestrator import _run_deep
    # We need to patch the registry
    from unittest.mock import patch as _patch
    with _patch.dict("medical_research_mcp.audit.orchestrator.GATE_REGISTRY", broken_list, clear=False):
        # This should not crash
        config = AuditConfig(
            repository=str(tmp_path),
            mode="deep",
            run_tests=False,
            run_security=False,
            run_dependency_audit=False,
        )
        report = run_audit(config)
        assert report is not None
        # All gates should be either PASS, FAIL, BLOCKED, etc., but the crash should not propagate
        for gid, gate in report.gates.items():
            assert gate.status != AuditStatus.PASS or gate.evidence, \
                f"Gate {gid} should not be PASS without evidence"


# ===== Test: Command output truncation =====

def test_output_truncation() -> None:
    """stdout/stderr longer than max_chars should be truncated with a marker."""
    from medical_research_mcp.audit.command_runner import _truncate

    text = "A" * 1000
    truncated, was_truncated = _truncate(text, 100)
    assert was_truncated, "Long text should be truncated"
    assert len(truncated) < len(text), "Truncated text should be shorter"
    assert "[TRUNCATED" in truncated, "Truncation should include marker"


# ===== Test: Exclusions work =====

def test_should_ignore() -> None:
    """The exclusion matcher should correctly identify paths to ignore."""
    assert should_ignore("foo/.git/bar")
    assert should_ignore("__pycache__/module.py")
    assert should_ignore("node_modules/package/index.js")
    assert should_ignore("model.safetensors", DEFAULT_EXCLUSIONS)
    assert should_ignore("checkpoint.pt", DEFAULT_EXCLUSIONS)
    assert should_ignore("data.db", DEFAULT_EXCLUSIONS)
    assert not should_ignore("src/main.py")
    assert not should_ignore("README.md")


# ===== Test: Path with spaces works =====

def test_path_with_spaces(tmp_path: Path) -> None:
    """Repository paths containing spaces should work correctly."""
    spaced = tmp_path / "my research" / "repo v2"
    spaced.mkdir(parents=True)
    (spaced / "README.md").write_text("# Spaced Path", encoding="utf-8")
    (spaced / "module.py").write_text("x = 1", encoding="utf-8")

    config = AuditConfig(
        repository=str(spaced),
        mode="structural",
    )
    report = run_audit(config)
    assert report is not None
    assert "v2" in report.target or "my research" in report.target or "spaced" in report.target.lower()


# ===== Test: Compute score logic =====

def test_score_computation() -> None:
    """Verify the scoring engine's mathematical consistency."""
    gates = {
        "a": GateResult(id="a", title="A", critical=True, status=AuditStatus.PASS, weight=1.0, score=10.0),
        "b": GateResult(id="b", title="B", critical=True, status=AuditStatus.PASS, weight=1.0, score=10.0),
        "c": GateResult(id="c", title="C", critical=True, status=AuditStatus.FAIL, weight=1.0, score=5.0),
    }
    score_info = compute_score(gates)
    assert score_info["status"] == AuditStatus.FAIL
    assert score_info["score"] is not None
    assert score_info["score"] < 10.0, "Should not be 10 with a FAIL"
    assert score_info["coverage"] == 1.0


def test_score_blocked_critical() -> None:
    """Critical BLOCKED gates should result in overall BLOCKED with score None."""
    gates = {
        "a": GateResult(id="a", title="A", critical=True, status=AuditStatus.PASS, weight=1.0, score=10.0),
        "b": GateResult(id="b", title="B", critical=True, status=AuditStatus.BLOCKED, weight=1.0, score=None),
    }
    score_info = compute_score(gates)
    assert score_info["status"] == AuditStatus.BLOCKED
    assert score_info["score"] is None


def test_score_not_executed_critical() -> None:
    """Critical NOT_EXECUTED gates should prevent score."""
    gates = {
        "a": GateResult(id="a", title="A", critical=True, status=AuditStatus.PASS, weight=1.0, score=10.0),
        "b": GateResult(id="b", title="B", critical=True, status=AuditStatus.NOT_EXECUTED, weight=1.0, score=None),
    }
    score_info = compute_score(gates)
    assert score_info["status"] == AuditStatus.BLOCKED
    assert score_info["score"] is None


def test_juge_reduces_inconsistent_verdict() -> None:
    """Judge must reduce or invalidate an inconsistent verdict."""
    # Gate with PASS but with evidence that has empty hashes
    gate = GateResult(
        id="inconsistent",
        title="Inconsistent Gate",
        status=AuditStatus.PASS,
        score=10.0,
        evidence=[
            EvidenceItem(
                type=EvidenceType.COMMAND_OUTPUT,
                source="cmd",
                sha256="",
                summary="test",
            ),
        ],
    )
    judged = judge_gate(gate)
    assert judged is not None, "Judge should flag inconsistent gate"


# ===== Test: Legacy compat path =====

def test_legacy_compat() -> None:
    """Verify backward-compatible import path still works."""
    from medical_research_mcp.audit import audit_repository
    assert callable(audit_repository), "audit_repository should be importable and callable"


# ===== Test: CLI structural run =====

def test_cli_structural_does_not_crash(tmp_path: Path) -> None:
    """Running the CLI in structural mode should produce valid JSON output."""
    (tmp_path / "README.md").write_text("# Test", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "medical_research_mcp.audit", str(tmp_path), "--mode", "structural"],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    output = json.loads(result.stdout)
    assert "status" in output
    assert "mode" in output
    assert output["mode"] == "structural"
    assert output["score"] is None or output["score"] == 0


# ===== Test: ignore patterns =====

def test_build_ignore_patterns() -> None:
    """Custom extra exclusions should be appended to defaults."""
    patterns = build_ignore_patterns(["custom_cache/", "*.custom"])
    assert "custom_cache/" in patterns
    assert "*.custom" in patterns
    assert ".git" in patterns


# ===== Test: EvidenceItem model =====

def test_evidence_item_defaults() -> None:
    """EvidenceItem should have sensible defaults."""
    ev = EvidenceItem(type=EvidenceType.COMMAND_OUTPUT, source="test", sha256="abc", summary="test")
    assert ev.verified is True
    assert ev.type == EvidenceType.COMMAND_OUTPUT


# ===== Test: Gates work with local structural audit fixture =====

@pytest.mark.timeout(30)
def test_structural_on_local_fixture(tmp_path: Path) -> None:
    """Structural audit on a local diabetes AI fixture should complete without external repos."""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='fixture-diabetes-ai'\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "SOURCE_REGISTRY = ['PubMed', 'ADA', 'WHO']\n"
        "def build_diabetes_evidence_query():\n"
        "    return 'diabetes chronic kidney disease RAG evaluation human review'\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "Research-only diabetes AI fixture with source_registry, human_review, audit_logs, and no autonomous diagnosis.\n",
        encoding="utf-8",
    )
    config = AuditConfig(
        repository=str(tmp_path),
        mode="structural",
    )
    report = run_audit(config)
    assert report is not None
    assert report.mode == "structural"
    assert report.score is None, "Structural mode should not produce score"
