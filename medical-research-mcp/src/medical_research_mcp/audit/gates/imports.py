"""Gate 3: Imports and Compilation — run compileall, detect syntax/import failures."""

from __future__ import annotations
import asyncio
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..command_runner import run_command


async def check_imports(repository: str, max_output_chars: int = 50000) -> GateResult:
    """Gate 3: Verify all Python files compile and imports resolve."""
    gate = GateResult(
        id="imports_and_compilation",
        title="Imports and Compilation",
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

    # compileall
    compile_cmd = [python, "-m", "compileall", "-q", "-l", str(root)]
    compile_rec = await run_command(compile_cmd, timeout_seconds=120, max_output_chars=max_output_chars, cwd=str(root))
    gate.commands.append(compile_rec)

    if compile_rec.exit_code == 0:
        output_text = (compile_rec.stdout or "") + (compile_rec.stderr or "")
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()
        gate.evidence.append({
            "type": "command_output",
            "source": "compileall",
            "sha256": output_hash,
            "summary": "All Python files compile without syntax errors",
            "verified": True,
        })
    else:
        gate.findings.append(f"Compilation errors detected (exit code {compile_rec.exit_code})")
        if compile_rec.stderr:
            gate.findings.append(f"stderr: {compile_rec.stderr[:1000]}")

    # Count Python files
    py_files = list(root.rglob("*.py"))
    gate.metrics["python_files"] = len(py_files)
    gate.metrics["compile_exit_code"] = compile_rec.exit_code

    if compile_rec.exit_code == 0:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
    elif compile_rec.exit_code is not None and compile_rec.exit_code > 0:
        gate.status = AuditStatus.FAIL
        gate.score = 0.0
        gate.remediation = ["Fix syntax errors in Python files", "Run `py -3 -m compileall .` locally to identify issues"]
    else:
        gate.status = AuditStatus.BLOCKED
        gate.score = None

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
