#!/usr/bin/env python3
"""Portable path resolution for AEOS scripts.

The repository can run from a fixed workstation path, a cloned worktree or a
removable drive. Keep environment discovery here so individual scripts do not
hard-code host-local paths.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_TMP_VENV = Path("/tmp/aeos-venv")


def repo_root() -> Path:
    return REPO_ROOT


def portable_home(root: Path | None = None) -> Path:
    configured = os.environ.get("AEOS_PORTABLE_HOME")
    return Path(configured).expanduser().resolve() if configured else (root or REPO_ROOT) / ".aeos"


def portable_tmp(root: Path | None = None) -> Path:
    configured = os.environ.get("AEOS_TMP")
    return Path(configured).expanduser().resolve() if configured else portable_home(root) / "tmp"


def portable_venv(root: Path | None = None) -> Path:
    configured = os.environ.get("AEOS_PYTHON_VENV")
    return Path(configured).expanduser().resolve() if configured else portable_home(root) / "venv"


def bin_dir(venv: Path) -> Path:
    return venv / ("Scripts" if os.name == "nt" else "bin")


def executable_name(name: str) -> str:
    return f"{name}.exe" if os.name == "nt" else name


def venv_executable(venv: Path, name: str) -> Path:
    return bin_dir(venv) / executable_name(name)


def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def python_supports(python: Path, modules: list[str]) -> bool:
    if not modules:
        return True
    if not python.exists():
        return False
    checks = [f"import {module}" for module in modules]
    try:
        completed = subprocess.run(
            [str(python), "-c", "; ".join(checks)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return False
    return completed.returncode == 0


def python_executable(root: Path | None = None, required_modules: list[str] | None = None) -> str:
    configured = os.environ.get("AEOS_PYTHON")
    if configured:
        return configured

    root = root or REPO_ROOT
    required_modules = required_modules or []
    candidates = [
        venv_executable(portable_venv(root), "python"),
        venv_executable(LEGACY_TMP_VENV, "python"),
    ]
    for candidate in candidates:
        if candidate.exists() and python_supports(candidate, required_modules):
            return str(candidate)
    if not required_modules or python_supports(Path(sys.executable), required_modules):
        return sys.executable
    return sys.executable


def tool_executable(name: str, root: Path | None = None) -> str | None:
    configured = os.environ.get(f"AEOS_{name.upper().replace('-', '_')}")
    if configured:
        return configured

    root = root or REPO_ROOT
    candidates = [
        venv_executable(portable_venv(root), name),
        venv_executable(LEGACY_TMP_VENV, name),
    ]
    existing = first_existing(candidates)
    if existing:
        return str(existing)
    return shutil.which(name)


def robot_output_dir(root: Path | None = None) -> Path:
    return portable_tmp(root) / "robot-results"


def performance_target(root: Path | None = None) -> Path:
    return portable_tmp(root) / "performance-verify"


def ensure_portable_dirs(root: Path | None = None) -> list[Path]:
    root = root or REPO_ROOT
    paths = [
        portable_home(root),
        portable_tmp(root),
        portable_home(root) / "cache",
        portable_home(root) / "evidence",
        portable_home(root) / "reports",
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    return paths
