from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "portable_env.py"
spec = importlib.util.spec_from_file_location("portable_env", MODULE_PATH)
portable_env = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["portable_env"] = portable_env
spec.loader.exec_module(portable_env)


def test_portable_home_defaults_to_repo_local_aeos(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("AEOS_PORTABLE_HOME", raising=False)

    assert portable_env.portable_home(tmp_path) == tmp_path / ".aeos"


def test_portable_home_can_be_overridden(tmp_path: Path, monkeypatch):
    custom = tmp_path / "portable-state"
    monkeypatch.setenv("AEOS_PORTABLE_HOME", str(custom))

    assert portable_env.portable_home(tmp_path) == custom


def test_python_executable_prefers_repo_local_venv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("AEOS_PYTHON", raising=False)
    python = portable_env.venv_executable(portable_env.portable_venv(tmp_path), "python")
    python.parent.mkdir(parents=True)
    python.write_text("#!/usr/bin/env python\n", encoding="utf-8")

    assert portable_env.python_executable(tmp_path) == str(python)


def test_python_executable_skips_venv_without_required_modules(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("AEOS_PYTHON", raising=False)
    python = portable_env.venv_executable(portable_env.portable_venv(tmp_path), "python")
    python.parent.mkdir(parents=True)
    python.write_text("#!/usr/bin/env python\n", encoding="utf-8")

    assert portable_env.python_executable(tmp_path, required_modules=["definitely_missing_aeos_module"]) != str(python)


def test_ensure_portable_dirs_creates_local_state(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("AEOS_PORTABLE_HOME", raising=False)

    paths = portable_env.ensure_portable_dirs(tmp_path)

    assert tmp_path / ".aeos" in paths
    assert (tmp_path / ".aeos" / "tmp").is_dir()
    assert (tmp_path / ".aeos" / "cache").is_dir()
