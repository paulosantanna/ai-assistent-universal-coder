#!/usr/bin/env python3
"""Prepare AEOS for portable execution from the repository directory."""

from __future__ import annotations

import argparse
import subprocess
import sys
import venv
from pathlib import Path

from portable_env import ensure_portable_dirs, portable_venv, repo_root, venv_executable


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap AEOS portable local state.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root to prepare.")
    parser.add_argument("--install-deps", action="store_true", help="Install requirements-dev.txt into the portable venv.")
    return parser.parse_args(argv)


def create_venv(root: Path) -> Path:
    target = portable_venv(root)
    if not venv_executable(target, "python").exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(target)
    return target


def install_deps(root: Path, venv_path: Path) -> None:
    requirements = root / "requirements-dev.txt"
    if not requirements.exists():
        raise FileNotFoundError(f"Missing requirements file: {requirements}")
    python = str(venv_executable(venv_path, "python"))
    subprocess.run([python, "-m", "pip", "install", "-r", str(requirements)], cwd=root, check=True)

    editable_packages = [
        "src",
        "continuous-training-mcp[dev]",
        "medical-research-mcp[dev]",
        "packages/aeos-language-server[dev]",
        "universal-project-mcp",
    ]
    for package in editable_packages:
        subprocess.run([python, "-m", "pip", "install", "-e", package], cwd=root, check=True)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(args.root).resolve()
    for path in ensure_portable_dirs(root):
        print(f"READY {path}")
    venv_path = create_venv(root)
    print(f"READY {venv_path}")
    if args.install_deps:
        install_deps(root, venv_path)
        print("READY python dependencies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
