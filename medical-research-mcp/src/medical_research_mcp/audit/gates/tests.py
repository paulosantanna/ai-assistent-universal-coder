"""Gate 4: Test Execution — run pytest with timeout, capture results."""

from __future__ import annotations
import asyncio
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..command_runner import run_command


async def check_tests(
    repository: str,
    timeout_seconds: int = 300,
    max_output_chars: int = 50000,
) -> GateResult:
    """Gate 4: Execute pytest and collect real test results — NOT just check for test dir existence."""
    gate = GateResult(
        id="test_execution",
        title="Test Execution",
        critical=True,
        weight=1.0,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    root = Path(repository).resolve()
    if not root.is_dir():
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"Repository path not found: {repository}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    python = sys.executable

    # Check if pytest is available
    pytest_check = await run_command([python, "-m", "pytest", "--version"], timeout_seconds=30, max_output_chars=1000)
    if pytest_check.exit_code != 0:
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"pytest not available: {pytest_check.stderr[:500]}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Check if tests directory exists (structural info only — not counted as PASS)
    test_dir = root / "tests"
    has_test_dir = test_dir.is_dir()
    gate.metrics["has_tests_directory"] = has_test_dir
    if not has_test_dir:
        gate.status = AuditStatus.NOT_EXECUTED
        gate.findings.append("No tests/ directory found — cannot execute tests")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    test_files = list(test_dir.rglob("test_*.py")) + list(test_dir.rglob("*_test.py"))
    gate.metrics["test_files_found"] = len(test_files)
    if not test_files:
        gate.status = AuditStatus.NOT_EXECUTED
        gate.findings.append("tests/ directory exists but contains no test files")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Run pytest
    pytest_args = [python, "-m", "pytest", "-ra", "--tb=short", "-q", str(test_dir)]
    pytest_rec = await run_command(pytest_args, timeout_seconds=timeout_seconds, max_output_chars=max_output_chars, cwd=str(root))
    gate.commands.append(pytest_rec)

    # Parse results from stdout
    output = pytest_rec.stdout + "\n" + pytest_rec.stderr
    lines = output.splitlines()

    total = 0
    passed = 0
    failed = 0
    skipped = 0
    xfailed = 0
    errors = 0

    import re
    for line in lines:
        if "==" in line and "passed" in line:
            m = re.search(r"(\d+) passed", line)
            if m:
                passed = int(m.group(1))
            m = re.search(r"(\d+) failed", line)
            if m:
                failed = int(m.group(1))
            m = re.search(r"(\d+) skipped", line)
            if m:
                skipped = int(m.group(1))
            m = re.search(r"(\d+) xfailed", line)
            if m:
                xfailed = int(m.group(1))
            m = re.search(r"(\d+) error", line)
            if m:
                errors = int(m.group(1))
        elif re.search(r"\d+ (passed|failed|skipped|errors?) in \d", line):
            m = re.search(r"(\d+) passed", line)
            if m:
                passed = int(m.group(1))
            m = re.search(r"(\d+) failed", line)
            if m:
                failed = int(m.group(1))
            m = re.search(r"(\d+) skipped", line)
            if m:
                skipped = int(m.group(1))
            m = re.search(r"(\d+) errors?", line)
            if m:
                errors = int(m.group(1))

    if not total and passed + failed + skipped + xfailed + errors > 0:
        total = passed + failed + skipped + xfailed + errors

    gate.metrics["total"] = total
    gate.metrics["passed"] = passed
    gate.metrics["failed"] = failed
    gate.metrics["skipped"] = skipped
    gate.metrics["xfailed"] = xfailed
    gate.metrics["errors"] = errors
    gate.metrics["exit_code"] = pytest_rec.exit_code

    # Hash the test output
    output_hash = hashlib.sha256(output.encode()).hexdigest()
    gate.evidence.append(
        {
            "type": "test_report",
            "source": "pytest output",
            "sha256": output_hash,
            "summary": f"pytest: {passed} passed, {failed} failed, {skipped} skipped, {errors} errors (exit {pytest_rec.exit_code})",
            "verified": pytest_rec.exit_code == 0,
        }
    )

    if pytest_rec.timed_out:
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"pytest timed out after {timeout_seconds}s")
        gate.score = None
    elif pytest_rec.exit_code == 0:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.findings.append(f"All {total} tests passed" if total else "Tests passed")
    elif pytest_rec.exit_code is not None and pytest_rec.exit_code > 0:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 * (1.0 - failed / max(total, 1)))
        gate.findings.append(f"{failed} test(s) failed out of {total}")
        gate.remediation = ["Fix failing tests before proceeding", "Run `py -3 -m pytest -ra` locally for details"]
    else:
        gate.status = AuditStatus.BLOCKED
        gate.score = None
        gate.findings.append(f"pytest failed with exit code {pytest_rec.exit_code}")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
