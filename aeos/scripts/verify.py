#!/usr/bin/env python3
"""Run AEOS verification suites from one stable entrypoint."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]
    cwd: Path = REPO_ROOT
    env: dict[str, str] | None = None


def _env_with_pythonpath(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) if not existing else f"{REPO_ROOT}{os.pathsep}{existing}"
    if extra:
        env.update(extra)
    return env


def _pytest(python: str, *paths: str) -> list[str]:
    return [python, "-m", "pytest", *paths, "-q"]


def build_steps(args: argparse.Namespace) -> list[Step]:
    python = args.python
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
                        "/tmp/aeos-performance-verify",
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
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS LSP doctor",
                    [python, "-m", "aeos_lsp.cli", "doctor", "."],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS LSP validate",
                    [python, "-m", "aeos_lsp.cli", "validate", "."],
                    env=_env_with_pythonpath(),
                ),
                Step(
                    "AEOS LSP index",
                    [python, "-m", "aeos_lsp.cli", "index", "."],
                    env=_env_with_pythonpath(),
                ),
            ]
        )

        if not args.skip_node:
            steps.append(Step("AEOS runtime build", ["npm", "run", "build"], cwd=REPO_ROOT / "runtime"))

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
        default=sys.executable,
        help="Python interpreter to use for pytest and AEOS CLI commands.",
    )
    parser.add_argument(
        "--skip-node",
        action="store_true",
        help="Skip runtime npm build during the full suite.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    failures = 0
    for step in build_steps(args):
        failures += 1 if run_step(step) else 0

    print("\nAEOS verification complete.")
    if failures:
        print(f"Result: FAILED ({failures} step(s) failed)")
        return 1
    print("Result: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
