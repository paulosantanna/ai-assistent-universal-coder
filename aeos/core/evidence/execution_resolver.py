from __future__ import annotations

from pathlib import Path
from typing import Optional

RESOLVE_LATEST_ANY = "latest-any"
RESOLVE_LATEST_COMPLETE = "latest-complete"
RESOLVE_LATEST_JUDGE = "latest-judge"
RESOLVE_LATEST_RUNTIME = "latest-runtime"

RESOLVE_MODES = (
    RESOLVE_LATEST_ANY,
    RESOLVE_LATEST_COMPLETE,
    RESOLVE_LATEST_JUDGE,
    RESOLVE_LATEST_RUNTIME,
)

RESOLVE_ALIASES: dict[str, str] = {
    "latest": RESOLVE_LATEST_COMPLETE,
}


def normalize_mode(mode: str) -> str:
    return RESOLVE_ALIASES.get(mode, mode)


def resolve_execution(
    workspace_root: Path,
    mode: str = RESOLVE_LATEST_COMPLETE,
) -> tuple[str, Path]:
    mode = normalize_mode(mode)
    evidence_dir = workspace_root / ".aeos" / "evidence"
    if not evidence_dir.exists():
        return "unknown", evidence_dir

    dirs = sorted(
        [d for d in evidence_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if not dirs:
        return "unknown", evidence_dir

    if mode == RESOLVE_LATEST_ANY:
        best = dirs[0]
        return best.name, best

    checks: dict[str, list[str]] = {
        RESOLVE_LATEST_COMPLETE: ["evidence-manifest.json"],
        RESOLVE_LATEST_JUDGE: ["judge-result.json"],
        RESOLVE_LATEST_RUNTIME: ["runtime-evidence-manifest.json"],
    }

    required = checks.get(mode, [])
    for d in dirs:
        if all((d / f).exists() for f in required):
            return d.name, d

    return "unknown", evidence_dir


def format_resolved(execution_id: str, execution_dir: Path) -> str:
    if execution_id == "unknown":
        return f"Resolved execution: unknown (no matching execution found in {execution_dir})"
    return f"Resolved execution: {execution_dir}"
