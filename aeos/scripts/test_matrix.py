#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MAVEN = str(REPO_ROOT / ".tools/bin/mvn")
GRADLE = str(REPO_ROOT / ".tools/bin/gradle")


@dataclass(frozen=True)
class TestCommand:
    name: str
    command: list[str]
    required_binary: str | None = None
    optional: bool = False


def build_commands(include_optional: bool = False) -> list[TestCommand]:
    commands = [
        TestCommand("python-pytest", ["/tmp/aeos-venv/bin/python", "-m", "pytest", "-q"], "/tmp/aeos-venv/bin/python"),
        TestCommand("python-behave", ["/tmp/aeos-venv/bin/behave", "-q"], "/tmp/aeos-venv/bin/behave"),
        TestCommand("python-robot", ["/tmp/aeos-venv/bin/robot", "--outputdir", "/tmp/aeos-robot-results", "tests/robot"], "/tmp/aeos-venv/bin/robot"),
        TestCommand("node-jest", ["npm", "run", "test:node:jest"], "npm"),
        TestCommand("node-vitest", ["npm", "run", "test:node:vitest"], "npm"),
        TestCommand("node-mocha", ["npm", "run", "test:node:mocha"], "npm"),
        TestCommand("node-cucumber", ["npm", "run", "test:node:cucumber"], "npm"),
        TestCommand(
            "java-maven-junit-cucumber",
            [MAVEN, "-f", "templates/test-toolchains/java-junit5/pom.xml", "test"],
            MAVEN,
            optional=True,
        ),
        TestCommand(
            "java-gradle-junit",
            [GRADLE, "--no-daemon", "-p", "templates/test-toolchains/java-gradle-junit5", "test"],
            GRADLE,
            optional=True,
        ),
        TestCommand("go-test", ["go", "test", "./..."], "go", optional=True),
        TestCommand("rust-cargo-test", ["cargo", "test"], "cargo", optional=True),
        TestCommand("dotnet-test", ["dotnet", "test"], "dotnet", optional=True),
    ]
    return commands if include_optional else [cmd for cmd in commands if not cmd.optional]


def is_available(binary: str | None) -> bool:
    if not binary:
        return True
    if "/" in binary:
        return Path(binary).exists()
    return shutil.which(binary) is not None


def run_command(command: TestCommand) -> int:
    if not is_available(command.required_binary):
        print(f"SKIP {command.name}: missing {command.required_binary}")
        return 0 if command.optional else 1
    print(f"RUN {command.name}: {' '.join(command.command)}")
    completed = subprocess.run(command.command, cwd=REPO_ROOT)
    if completed.returncode:
        print(f"FAIL {command.name}: {completed.returncode}")
    else:
        print(f"PASS {command.name}")
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run AEOS configured test matrix.")
    parser.add_argument("--include-optional", action="store_true", help="Run optional language suites when host tools exist.")
    args = parser.parse_args(argv)

    failures = 0
    for command in build_commands(include_optional=args.include_optional):
        failures += 1 if run_command(command) else 0
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
