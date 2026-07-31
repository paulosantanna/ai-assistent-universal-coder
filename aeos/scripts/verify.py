#!/usr/bin/env python3
"""Run AEOS verification suites from one stable entrypoint."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import shutil
import sys
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from portable_env import ensure_portable_dirs, performance_target, portable_tmp, python_executable


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]
    cwd: Path = REPO_ROOT
    env: dict[str, str] | None = None


def _env_with_pythonpath(extra: dict[str, str] | None = None) -> dict[str, str]:
    ensure_portable_dirs(REPO_ROOT)
    configured_pytest_tmp = os.environ.get("AEOS_PYTEST_TMP")
    temp_root = (
        Path(configured_pytest_tmp).expanduser().resolve()
        if configured_pytest_tmp
        else portable_tmp(REPO_ROOT) / "pytest"
    )
    temp_root.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) if not existing else f"{REPO_ROOT}{os.pathsep}{existing}"
    env["AEOS_TMP"] = str(portable_tmp(REPO_ROOT))
    env["TMP"] = str(temp_root)
    env["TEMP"] = str(temp_root)
    env["TMPDIR"] = str(temp_root)
    if extra:
        env.update(extra)
    return env


def _env_with_lsp_pythonpath() -> dict[str, str]:
    return _env_with_pythonpath(
        {"PYTHONPATH": f"{REPO_ROOT / 'packages' / 'aeos-language-server' / 'src'}{os.pathsep}{REPO_ROOT}"}
    )

def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value).strip("-") or "suite"


def _pytest_basetemp(*paths: str) -> Path:
    root = portable_tmp(REPO_ROOT) / "pytest-basetemp"
    name = _safe_name("-".join(paths))[:80]
    target = root / f"{name}-{uuid4().hex[:8]}"
    target.mkdir(parents=True, exist_ok=False)
    return target


def _pytest(python: str, *paths: str) -> list[str]:
    return [
        python,
        "-m",
        "pytest",
        *paths,
        "-q",
        "-p",
        "no:cacheprovider",
        "--basetemp",
        str(_pytest_basetemp(*paths)),
    ]


def _npm_executable() -> str:
    return shutil.which("npm.cmd") or shutil.which("npm") or "npm"


def build_steps(args: argparse.Namespace) -> list[Step]:
    python = args.python or python_executable(REPO_ROOT, required_modules=["pytest"])
    steps: list[Step] = []

    if args.suite in {"quick", "full"}:
        steps.extend(
            [
                Step(
                    "AEOS doctor",
                    [python, "-m", "aeos.cli.main", "doctor", "--aeos-root", "."],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS registry",
                    [python, "-m", "aeos.cli.main", "registry", "validate"],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS structural guard",
                    [python, "aeos/scripts/structural_guard.py", "--root", "."],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS toolchain doctor",
                    [python, "aeos/scripts/toolchain_doctor.py", "--root", "."],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS performance benchmark",
                    [
                        python,
                        "-m",
                        "aeos.cli.main",
                        "performance",
                        "benchmark",
                        "--aeos-root",
                        ".",
                        "--target",
                        str(performance_target(REPO_ROOT)),
                        "--iterations",
                        "1",
                        "--fail-on",
                        "breach",
                    ],
                    env=_env_with_pythonpath(),
                ),
                Step("AEOS core tests", _pytest(python, "aeos/tests"), env=_env_with_pythonpath()),
            ]
        )

    if args.suite == "full":
        steps.extend(
            [
                Step(
                    "AEOS skills tests",
                    _pytest(
                        python,
                        "skills/chromatic-mega-brain/tests",
                        "skills/skill-factory/tests",
                        "skills/java-bug-solver/tests",
                        "skills/java-bug-solver-skill/tests",
                        "skills/python-bug-solver-skill/tests",
                        "skills/security-audit/tests",
                        "java-bug-solver/tests",
                    ),
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS MCP tests",
                    _pytest(python, "continuous-training-mcp/tests", "medical-research-mcp/tests"),
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS universal project MCP tests",
                    _pytest(python, "universal-project-mcp/tests"),
                    env=_env_with_pythonpath(
                        {"PYTHONPATH": f"{REPO_ROOT / 'universal-project-mcp' / 'src'}{os.pathsep}{REPO_ROOT}"}
                    ),
                ),
                Step(
                    "AEOS LSP tests",
                    _pytest(python, "packages/aeos-language-server/tests"),
                    env=_env_with_lsp_pythonpath(),
                ),
                Step(
                    "AEOS LSP doctor",
                    [python, "-m", "aeos_lsp.cli", "doctor", "."],
                    env=_env_with_lsp_pythonpath(),
                ),
                Step(
                    "AEOS LSP validate",
                    [python, "-m", "aeos_lsp.cli", "validate", "."],
                    env=_env_with_lsp_pythonpath(),
                ),
                Step(
                    "AEOS LSP index",
                    [python, "-m", "aeos_lsp.cli", "index", "."],
                    env=_env_with_lsp_pythonpath(),
                ),
            ]
        )

        if not args.skip_node:
            steps.append(Step("AEOS runtime build", [_npm_executable(), "run", "build"], cwd=REPO_ROOT / "runtime"))

    return steps


def run_step(step: Step) -> int:
    print(f"\n==> {step.name}")
    print(f"$ {' '.join(step.command)}")
    completed = subprocess.run(step.command, cwd=step.cwd, env=step.env)
    if completed.returncode:
        print(f"FAILED: {step.name} exited with {completed.returncode}")
    else:
        print(f"OK: {step.name}")
    return completed.returncode


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AEOS verification suites.")
    parser.add_argument(
        "--suite",
        choices=("quick", "full"),
        default="quick",
        help="quick validates core health; full also runs skills, MCP, LSP and runtime build.",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Python interpreter to use for pytest and AEOS CLI commands. Defaults to the portable AEOS venv when available.",
    )
    parser.add_argument(
        "--skip-node",
        action="store_true",
        help="Skip runtime npm build during the full suite.",
    )
    return parser.parse_args(argv)


def _write_verification_evidence(args: argparse.Namespace, failures: int, total_steps: int) -> Path:
    execution_id = f"verify-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
    evidence_dir = REPO_ROOT / ".aeos" / "evidence" / execution_id
    evidence_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "execution_id": execution_id,
        "status": "PASS" if failures == 0 else "FAIL",
        "suite": args.suite,
        "steps_total": total_steps,
        "steps_failed": failures,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": args.python or python_executable(REPO_ROOT, required_modules=["pytest"]),
    }
    fp = evidence_dir / "verification-result.json"
    fp.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return fp


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    failures = 0
    steps = build_steps(args)
    for step in steps:
        failures += 1 if run_step(step) else 0

    evidence_path = _write_verification_evidence(args, failures, len(steps))
    print(f"Verification evidence: {evidence_path}")

    print("\nAEOS verification complete.")
    if failures:
        print(f"Result: FAILED ({failures} step(s) failed)")
        return 1
    print("Result: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
