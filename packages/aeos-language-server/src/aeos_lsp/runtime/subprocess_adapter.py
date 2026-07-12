from __future__ import annotations

import logging
import os
import shlex
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30.0
_MAX_OUTPUT_BYTES = 1_048_576
_ALLOWED_COMMANDS: set[str] = {
    "git",
    "python",
    "python3",
    "node",
    "npm",
    "npx",
    "dotnet",
    "cargo",
    "go",
    "rustc",
    "gcc",
    "g++",
    "make",
    "cmake",
    "cat",
    "head",
    "tail",
    "echo",
    "printf",
    "ls",
    "find",
    "grep",
    "rg",
    "sed",
    "awk",
    "wc",
    "sort",
    "uniq",
    "cut",
    "tr",
    "tee",
    "diff",
    "patch",
    "tar",
    "gzip",
    "gunzip",
    "zip",
    "unzip",
    "curl",
    "wget",
    "jq",
    "yq",
    "pwd",
    "whoami",
    "date",
    "env",
    "mkdir",
    "cp",
    "mv",
    "rm",
    "chmod",
    "chown",
    "ln",
    "realpath",
    "readlink",
    "stat",
    "du",
    "df",
    "file",
    "basename",
    "dirname",
    "true",
    "false",
}

_DANGEROUS_PATTERNS: list[str] = [
    "rm -rf /",
    "rm -rf /*",
    "mkfs",
    "dd if=",
    "> /dev/",
    ":(){ :|:& };:",
    "chmod 777 /",
    "chown -R",
    "wget http://",
    "curl http://",
    "bash -c",
    "sh -c",
    "eval ",
    "exec ",
    "source ",
    "sudo ",
    "su ",
    "passwd",
    "iptables",
    "systemctl",
]


class CommandNotAllowedError(Exception):
    def __init__(self, command: str, reason: str) -> None:
        self.command = command
        self.reason = reason
        super().__init__(f"Command not allowed: {command} ({reason})")


class SubprocessAdapter:
    def __init__(
        self,
        allowlist: set[str] | None = None,
        max_output_bytes: int = _MAX_OUTPUT_BYTES,
        default_timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        self._allowlist = set(allowlist) if allowlist else _ALLOWED_COMMANDS
        self._max_output_bytes = max_output_bytes
        self._default_timeout = default_timeout

    def check_command(self, command: str) -> None:
        if not command or not command.strip():
            raise CommandNotAllowedError(command, "Empty command")

        for pattern in _DANGEROUS_PATTERNS:
            if pattern in command:
                raise CommandNotAllowedError(command, f"Matches dangerous pattern: {pattern}")

        parts = shlex.split(command)
        base_name = os.path.basename(parts[0]) if parts else ""

        if base_name not in self._allowlist:
            if os.path.sep not in parts[0]:
                resolved = self._resolve_command(base_name)
                if resolved is None:
                    raise CommandNotAllowedError(command, f"Command '{base_name}' not in allowlist and not found in PATH")

    def run(
        self,
        command: str,
        args: list[str] | None = None,
        cwd: str | Path | None = None,
        timeout: float | None = None,
        env: dict[str, str] | None = None,
        check_command: bool = True,
    ) -> dict[str, Any]:
        if check_command:
            self.check_command(command)

        timeout = timeout or self._default_timeout

        cmd_parts = [command]
        if args:
            cmd_parts.extend(args)

        logger.debug("Running subprocess: %s (timeout=%s, cwd=%s)", " ".join(cmd_parts), timeout, cwd)

        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        start = time.monotonic()
        try:
            proc = subprocess.Popen(
                cmd_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(cwd) if cwd else None,
                env=process_env,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )

            stdout_bytes = b""
            stderr_bytes = b""
            timed_out = False

            try:
                stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
                stdout_bytes, stderr_bytes = proc.communicate()

            elapsed = time.monotonic() - start

            stdout_str = self._truncate_output(stdout_bytes)
            stderr_str = self._truncate_output(stderr_bytes)

            result = {
                "returncode": proc.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "elapsed_seconds": elapsed,
                "timed_out": timed_out,
                "command": command,
                "args": args,
            }

            if proc.returncode != 0 and not timed_out:
                logger.debug(
                    "Subprocess exited with code %d: %s",
                    proc.returncode, stderr_str[:200],
                )

            return result

        except FileNotFoundError:
            elapsed = time.monotonic() - start
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command not found: {command}",
                "elapsed_seconds": elapsed,
                "timed_out": False,
                "command": command,
                "args": args,
                "error": f"Executable '{command}' not found on system PATH",
            }
        except Exception as exc:
            elapsed = time.monotonic() - start
            logger.exception("Subprocess failed: %s", command)
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(exc),
                "elapsed_seconds": elapsed,
                "timed_out": False,
                "command": command,
                "args": args,
                "error": str(exc),
            }

    def run_shell(
        self,
        command_line: str,
        cwd: str | Path | None = None,
        timeout: float | None = None,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        logger.warning("shell=True execution requested. This is restricted for security.")
        raise CommandNotAllowedError(
            command_line,
            "shell=True execution is prohibited by subprocess security policy",
        )

    def _truncate_output(self, data: bytes) -> str:
        if len(data) > self._max_output_bytes:
            data = data[: self._max_output_bytes]
            logger.warning("Output truncated at %d bytes", self._max_output_bytes)
        return data.decode("utf-8", errors="replace")

    @staticmethod
    def _resolve_command(name: str) -> str | None:
        path_ext = os.environ.get("PATHEXT", ".EXE;.CMD;.BAT;.COM") if sys.platform == "win32" else ""
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            if not path_dir:
                continue
            full = os.path.join(path_dir, name)
            if os.path.isfile(full) and os.access(full, os.X_OK):
                return full
            if sys.platform == "win32":
                for ext in path_ext.split(";"):
                    if ext:
                        full_ext = full + ext
                        if os.path.isfile(full_ext) and os.access(full_ext, os.X_OK):
                            return full_ext
        return None
