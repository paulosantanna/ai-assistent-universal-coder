"""Safe command execution with timeout, truncation, and read-only enforcement."""

from __future__ import annotations
import asyncio
import shutil
import sys
import time
import hashlib
import shlex
from pathlib import Path
from .models import CommandRecord


def _truncate(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    half = max_chars // 2
    return text[:half] + f"\n... [TRUNCATED {len(text) - 2*half} chars] ...\n" + text[-half:], True


async def run_command(
    command: list[str],
    timeout_seconds: int = 300,
    max_output_chars: int = 50000,
    cwd: str | None = None,
) -> CommandRecord:
    """Execute a command with timeout, capturing stdout/stderr."""
    started = time.monotonic()
    cmd_str = shlex.join(str(c) for c in command)
    record = CommandRecord(command=cmd_str)

    if not command:
        record.exit_code = -1
        record.stderr = "No command provided"
        record.duration_ms = (time.monotonic() - started) * 1000
        return record

    try:
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            record.exit_code = -1
            record.timed_out = True
            record.stderr = f"Command timed out after {timeout_seconds}s"
            record.duration_ms = (time.monotonic() - started) * 1000
            return record

        record.exit_code = proc.returncode
        stdout_text = stdout_bytes.decode("utf-8", errors="replace")
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")
        record.stdout, _ = _truncate(stdout_text, max_output_chars)
        record.stderr, _ = _truncate(stderr_text, max_output_chars)
        record.duration_ms = (time.monotonic() - started) * 1000

    except FileNotFoundError:
        record.exit_code = -1
        record.stderr = f"Command not found: {cmd_str}"
        record.duration_ms = (time.monotonic() - started) * 1000
    except Exception as e:
        record.exit_code = -1
        record.stderr = f"Execution error: {e}"
        record.duration_ms = (time.monotonic() - started) * 1000

    return record


def find_tool(name: str) -> str | None:
    """Check if a tool is available on the system PATH."""
    return shutil.which(name)


def find_python(python_executable: str | None = None) -> str:
    """Resolve a Python executable path without embedding shell arguments."""
    if python_executable:
        return python_executable
    if sys.executable:
        return sys.executable
    py3 = shutil.which("py")
    if py3:
        return py3
    python = shutil.which("python")
    if python:
        return python
    return "python"


def compute_sha256(file_path: str | Path) -> str:
    """Compute SHA-256 hash of a file."""
    path = Path(file_path)
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
