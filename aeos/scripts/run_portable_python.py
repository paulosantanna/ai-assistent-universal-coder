#!/usr/bin/env python3
"""Run a Python command with the AEOS portable interpreter resolver."""

from __future__ import annotations

import argparse
import subprocess
import sys

from portable_env import python_executable, repo_root


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Python command through the AEOS portable resolver.")
    parser.add_argument("--require-module", action="append", default=[], help="Module that must import in the selected Python.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to Python. Use -- before the command.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    parsed = parse_args(argv or sys.argv[1:])
    command_args = parsed.args[1:] if parsed.args[:1] == ["--"] else parsed.args
    if not command_args:
        print("ERROR: missing Python command arguments", file=sys.stderr)
        return 2
    python = python_executable(repo_root(), required_modules=parsed.require_module)
    completed = subprocess.run([python, *command_args], cwd=repo_root())
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
