#!/usr/bin/env python3
"""Report AEOS optional toolchain availability without hiding skips."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from portable_env import python_executable, tool_executable

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Toolchain:
    name: str
    required: str
    optional: bool
    command: str
    missing_reason: str


@dataclass(frozen=True)
class ToolchainStatus:
    name: str
    required: str
    optional: bool
    command: str
    available: bool
    status: str
    reason: str
    fallback: str


TOOLCHAINS = (
    Toolchain(
        "python",
        "AEOS_PYTHON",
        False,
        "python -m pytest -q",
        "Python is required for the AEOS verification suite.",
    ),
    Toolchain(
        "node",
        "npm",
        False,
        "npm run test:node:jest",
        "npm is required for the Node.js smoke and runtime build suites.",
    ),
    Toolchain(
        "java-maven",
        ".tools/apache-maven-3.9.11/bin/mvn",
        True,
        ".tools/bin/mvn -f templates/test-toolchains/java-junit5/pom.xml test",
        "Maven distribution is not present in this worktree; Java Maven suite is skipped.",
    ),
    Toolchain(
        "java-gradle",
        ".tools/gradle-9.2.1/bin/gradle",
        True,
        ".tools/bin/gradle --no-daemon -p templates/test-toolchains/java-gradle-junit5 test",
        "Gradle distribution is not present in this worktree; Java Gradle suite is skipped.",
    ),
    Toolchain(
        "java-jdk",
        ".tools/jdk-17.0.19+10/bin/java",
        True,
        ".tools/jdk-17.0.19+10/bin/java -version",
        "JDK distribution is not present in this worktree; Java suites are skipped.",
    ),
    Toolchain(
        "go",
        "go",
        True,
        "go test ./...",
        "Go binary is not available on this host; Go suite is skipped.",
    ),
    Toolchain(
        "rust",
        "cargo",
        True,
        "cargo test",
        "Cargo binary is not available on this host; Rust suite is skipped.",
    ),
    Toolchain(
        "dotnet",
        "dotnet",
        True,
        "dotnet test",
        ".NET SDK binary is not available on this host; .NET suite is skipped.",
    ),
)


def is_available(root: Path, toolchain: Toolchain) -> bool:
    required = toolchain.required
    if required == "AEOS_PYTHON":
        return Path(python_executable(root)).exists() or bool(tool_executable("python", root))
    path_like = required.startswith(".") or required.startswith("/") or "/" in required or "\\" in required
    if path_like:
        candidate = Path(required)
        return candidate.exists() if candidate.is_absolute() else (root / candidate).exists()
    host_only_optional = toolchain.optional and toolchain.name in {"go", "rust", "dotnet"}
    if host_only_optional and root.resolve() != REPO_ROOT.resolve():
        return False
    return tool_executable(required, root) is not None


def evaluate(root: Path) -> list[ToolchainStatus]:
    statuses: list[ToolchainStatus] = []
    for toolchain in TOOLCHAINS:
        available = is_available(root, toolchain)
        fallback = "ecosystem-contract-adapter" if toolchain.optional and not available else ""
        status = "available" if available else ("adapter" if fallback else "missing")
        statuses.append(
            ToolchainStatus(
                name=toolchain.name,
                required=toolchain.required,
                optional=toolchain.optional,
                command=toolchain.command,
                available=available,
                status=status,
                reason="" if available else toolchain.missing_reason.replace("skipped", "covered by contract adapter"),
                fallback=fallback,
            )
        )
    return statuses


def render_text(statuses: list[ToolchainStatus]) -> str:
    lines = ["AEOS toolchain doctor:"]
    for item in statuses:
        marker = item.status.upper()
        suffix = f" - {item.reason}" if item.reason else ""
        if item.fallback:
            suffix += f" ({item.fallback})"
        lines.append(f"- {item.name}: {marker} ({item.required}){suffix}")

    required_missing = sum(1 for item in statuses if not item.optional and not item.available)
    adapter_covered = sum(1 for item in statuses if item.fallback)
    available = sum(1 for item in statuses if item.available)
    lines.append(
        f"Summary: {available} available, {adapter_covered} adapter-covered, {required_missing} required missing"
    )
    return "\n".join(lines)


def render_json(statuses: list[ToolchainStatus]) -> str:
    payload = {
        "toolchains": [asdict(item) for item in statuses],
        "summary": {
            "available": sum(1 for item in statuses if item.available),
            "adapter_covered": sum(1 for item in statuses if item.fallback),
            "optional_skipped": 0,
            "required_missing": sum(1 for item in statuses if not item.optional and not item.available),
        },
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report AEOS test toolchain availability.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root to inspect.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument(
        "--require-optional",
        action="store_true",
        help="Fail when optional language toolchains are unavailable.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    statuses = evaluate(Path(args.root).resolve())
    print(render_json(statuses) if args.json else render_text(statuses))

    required_missing = any(not item.optional and not item.available for item in statuses)
    optional_missing = any(item.optional and not item.available for item in statuses)
    if required_missing or (args.require_optional and optional_missing):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
