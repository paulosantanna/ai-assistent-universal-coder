"""Path resolution for AEOS root vs target project."""

import os
from pathlib import Path


def resolve_aeos_root(args) -> Path:
    explicit = getattr(args, "aeos_root", None)
    if explicit:
        return Path(explicit).resolve()

    env_root = os.environ.get("AEOS_ROOT", "")
    if env_root:
        return Path(env_root).resolve()

    return _autodetect_aeos_root()


def resolve_target_path(args) -> Path:
    target = getattr(args, "target", ".")
    return Path(target).resolve()


def _autodetect_aeos_root() -> Path:
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / "aeos" / "config" / "aeos.config.yaml"
        if candidate.exists():
            return parent
    return cwd


def validate_aeos_root(path: Path) -> str | None:
    config_file = path / "aeos" / "config" / "aeos.config.yaml"
    if not config_file.exists():
        return (
            f"AEOS config not found at {config_file}. "
            f"Use --aeos-root or set AEOS_ROOT environment variable."
        )
    return None


def validate_target_path(path: Path) -> str | None:
    if not path.exists():
        return f"Target path does not exist: {path}"
    return None


def ensure_target_is_not_aeos_root(aeos_root: Path, target_path: Path) -> str | None:
    if aeos_root.resolve() == target_path.resolve():
        return (
            f"Target path is the same as AEOS root: {target_path}. "
            f"Use --aeos-root to point to the AEOS installation directory, "
            f"and --target to point to the project to analyze."
        )
    return None
