import os
from pathlib import Path
from unittest.mock import MagicMock

from aeos.core.runtime.path_resolver import (
    resolve_aeos_root,
    resolve_target_path,
    validate_aeos_root,
    validate_target_path,
    ensure_target_is_not_aeos_root,
)


def test_resolve_aeos_root_from_arg(tmp_path: Path):
    args = MagicMock()
    args.aeos_root = str(tmp_path)
    result = resolve_aeos_root(args)
    assert result == tmp_path.resolve()


def test_resolve_aeos_root_not_set(tmp_path: Path):
    args = MagicMock()
    del args.aeos_root
    result = resolve_aeos_root(args)
    assert isinstance(result, Path)


def test_resolve_target_path(tmp_path: Path):
    args = MagicMock()
    args.target = str(tmp_path)
    result = resolve_target_path(args)
    assert result == tmp_path.resolve()


def test_resolve_target_path_default():
    args = MagicMock()
    if hasattr(args, "target"):
        del args.target
    result = resolve_target_path(args)
    assert result == Path.cwd().resolve()


def test_validate_aeos_root_found(tmp_path: Path):
    config = tmp_path / "aeos" / "config" / "aeos.config.yaml"
    config.parent.mkdir(parents=True)
    config.write_text("aeos:\n  name: test")
    assert validate_aeos_root(tmp_path) is None


def test_validate_aeos_root_missing(tmp_path: Path):
    err = validate_aeos_root(tmp_path)
    assert err is not None
    assert "AEOS config not found" in err
    assert "--aeos-root" in err


def test_validate_target_path_exists(tmp_path: Path):
    assert validate_target_path(tmp_path) is None


def test_validate_target_path_missing(tmp_path: Path):
    err = validate_target_path(tmp_path / "nonexistent")
    assert err is not None
    assert "Target path does not exist" in err


def test_ensure_target_not_aeos_root_different(tmp_path: Path):
    other = tmp_path / "other"
    other.mkdir()
    assert ensure_target_is_not_aeos_root(tmp_path, other) is None


def test_ensure_target_not_aeos_root_same(tmp_path: Path):
    err = ensure_target_is_not_aeos_root(tmp_path, tmp_path)
    assert err is not None
    assert "same as AEOS root" in err
