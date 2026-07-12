from __future__ import annotations

import logging
import os
import re
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_ALLOWED_COMMANDS: set[str] = {
    "git", "python", "python3", "node", "npm", "npx",
    "dotnet", "cargo", "go", "rustc", "gcc", "g++", "clang",
    "make", "cmake", "cat", "head", "tail", "echo", "printf",
    "ls", "find", "grep", "rg", "sed", "awk", "wc", "sort",
    "uniq", "cut", "tr", "tee", "diff", "patch", "tar", "gzip",
    "gunzip", "zip", "unzip", "curl", "wget", "jq", "yq",
    "pwd", "whoami", "date", "env", "mkdir", "cp", "mv", "rm",
    "chmod", "ln", "realpath", "readlink", "stat", "du", "df",
    "file", "basename", "dirname", "true", "false", "sleep",
    "timeout", "xargs", "which", "type",
}

_DANGEROUS_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\brm\s+(-rf?|--recursive)\s+[/\\]?\s*$"),
    re.compile(r"\bmkfs\s"),
    re.compile(r"\bdd\s+if="),
    re.compile(r"\bchmod\s+777\s"),
    re.compile(r"\bchown\s+-R\s"),
    re.compile(r"\bsudo\b"),
    re.compile(r"\bsu\s+-"),
    re.compile(r"\bpasswd\b"),
    re.compile(r"\biptables\b"),
    re.compile(r"\bsystemctl\b"),
    re.compile(r"\bjournalctl\b"),
    re.compile(r"\bwget\s+http://[^\s]+\s*\|\s*(bash|sh)"),
    re.compile(r"\bcurl\s+http://[^\s]+\s*\|\s*(bash|sh)"),
    re.compile(r"\bbash\s+-c\b"),
    re.compile(r"\bsh\s+-c\b"),
    re.compile(r"\beval\s+"),
    re.compile(r"\bexec\s+"),
    re.compile(r"\bsource\s+"),
    re.compile(r"\b>[/\\]dev[/\\]"),
    re.compile(r":\s*\(\s*\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;"),
]

_DENIED_ARG_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^--no-preserve-root$"),
    re.compile(r"^--exclude-from="),
    re.compile(r"^-rf$"),
    re.compile(r"^-r\s+f$"),
    re.compile(r"^-f\s+r$"),
]

_CRITICAL_ENV_VARS: set[str] = {
    "PATH", "HOME", "USER", "SHELL", "LD_LIBRARY_PATH",
    "DYLD_LIBRARY_PATH", "LD_PRELOAD",
}


class CommandNotAllowedError(Exception):
    def __init__(self, command: str, reason: str) -> None:
        self.command = command
        self.reason = reason
        super().__init__(f"Command not allowed: {command} ({reason})")


class CommandPolicy:
    def __init__(
        self,
        allowed_commands: set[str] | None = None,
        allow_shell: bool = False,
        max_args: int = 100,
        max_arg_length: int = 4096,
    ) -> None:
        self._allowed_commands = allowed_commands or _DEFAULT_ALLOWED_COMMANDS
        self._allow_shell = allow_shell
        self._max_args = max_args
        self._max_arg_length = max_arg_length

    def check_command(self, command: str) -> str:
        if not command or not command.strip():
            raise CommandNotAllowedError(command, "Empty command")

        if not self._allow_shell:
            for pattern in _DANGEROUS_PATTERNS:
                if pattern.search(command):
                    raise CommandNotAllowedError(command, f"Matches dangerous pattern")

        import shlex
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            raise CommandNotAllowedError(command, f"Invalid shell syntax: {exc}")

        if not parts:
            raise CommandNotAllowedError(command, "No command parts after parsing")

        if len(parts) > self._max_args:
            raise CommandNotAllowedError(
                command,
                f"Too many arguments ({len(parts)} > {self._max_args})",
            )

        base_name = os.path.basename(parts[0])

        if base_name not in self._allowed_commands:
            resolved = self._resolve_command(base_name)
            if resolved is None:
                raise CommandNotAllowedError(
                    command,
                    f"Command '{base_name}' not in allowlist",
                )

        for i, arg in enumerate(parts[1:], 1):
            if len(arg) > self._max_arg_length:
                raise CommandNotAllowedError(
                    command,
                    f"Argument {i} exceeds max length ({len(arg)} > {self._max_arg_length})",
                )
            for denied in _DENIED_ARG_PATTERNS:
                if denied.search(arg):
                    raise CommandNotAllowedError(
                        command,
                        f"Argument {i} matches denied pattern: {arg[:50]}",
                    )

        return base_name

    def check_env(self, env: dict[str, str] | None) -> None:
        if env is None:
            return
        for key in env:
            if key.upper() in _CRITICAL_ENV_VARS and key.upper() != "PATH":
                logger.warning("Attempted to override critical env var: %s", key)

    def is_command_allowed(self, command: str) -> bool:
        try:
            self.check_command(command)
            return True
        except CommandNotAllowedError:
            return False

    def add_allowed_command(self, command: str) -> None:
        self._allowed_commands.add(command)
        logger.debug("Added allowed command: %s", command)

    def remove_allowed_command(self, command: str) -> None:
        self._allowed_commands.discard(command)
        logger.debug("Removed allowed command: %s", command)

    def list_allowed_commands(self) -> list[str]:
        return sorted(self._allowed_commands)

    def validate_arguments(self, args: list[str]) -> list[str]:
        validated: list[str] = []
        for arg in args:
            if any(p.search(arg) for p in _DENIED_ARG_PATTERNS):
                raise CommandNotAllowedError(
                    arg, f"Argument matches denied pattern: {arg[:100]}"
                )
            validated.append(arg)
        return validated

    @staticmethod
    def _resolve_command(name: str) -> str | None:
        import sys
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

    def __repr__(self) -> str:
        return (
            f"CommandPolicy(allowed={len(self._allowed_commands)}, "
            f"shell={self._allow_shell})"
        )
