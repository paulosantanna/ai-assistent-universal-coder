#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from portable_env import python_executable, robot_output_dir, tool_executable


REPO_ROOT = Path(__file__).resolve().parents[2]
MAVEN = str(REPO_ROOT / ".tools/bin/mvn")
GRADLE = str(REPO_ROOT / ".tools/bin/gradle")
MAVEN_BINARY = str(REPO_ROOT / ".tools/apache-maven-3.9.11/bin/mvn")
GRADLE_BINARY = str(REPO_ROOT / ".tools/gradle-9.2.1/bin/gradle")


@dataclass(frozen=True)
class TestCommand:
    name: str
    command: list[str]
    required_binary: str | None = None
    optional: bool = False
    fallback_command: list[str] | None = None


def build_commands(include_optional: bool = False, only: set[str] | None = None) -> list[TestCommand]:
    python = python_executable(REPO_ROOT, required_modules=["pytest"])
    behave = tool_executable("behave", REPO_ROOT)
    robot = tool_executable("robot", REPO_ROOT)
    commands = [
        TestCommand("python-pytest", [python, "-m", "pytest", "-q"], python),
        TestCommand("python-behave", [behave or "behave", "-q"], behave or "behave"),
        TestCommand("python-robot", [robot or "robot", "--outputdir", str(robot_output_dir(REPO_ROOT)), "tests/robot"], robot or "robot"),
        TestCommand("node-jest", ["npm", "run", "test:node:jest"], "npm"),
        TestCommand("node-vitest", ["npm", "run", "test:node:vitest"], "npm"),
        TestCommand("node-mocha", ["npm", "run", "test:node:mocha"], "npm"),
        TestCommand("node-cucumber", ["npm", "run", "test:node:cucumber"], "npm"),
        TestCommand(
            "java-maven-junit-cucumber",
            [MAVEN, "-f", "templates/test-toolchains/java-junit5/pom.xml", "test"],
            MAVEN_BINARY,
            optional=True,
            fallback_command=[python, "aeos/scripts/ecosystem_contracts.py", "java-maven"],
        ),
        TestCommand(
            "java-gradle-junit",
            [GRADLE, "--no-daemon", "-p", "templates/test-toolchains/java-gradle-junit5", "test"],
            GRADLE_BINARY,
            optional=True,
            fallback_command=[python, "aeos/scripts/ecosystem_contracts.py", "java-gradle"],
        ),
        TestCommand("go-test", ["go", "test", "./..."], "go", optional=True, fallback_command=[python, "aeos/scripts/ecosystem_contracts.py", "go"]),
        TestCommand("rust-cargo-test", ["cargo", "test"], "cargo", optional=True, fallback_command=[python, "aeos/scripts/ecosystem_contracts.py", "rust"]),
        TestCommand("dotnet-test", ["dotnet", "test"], "dotnet", optional=True, fallback_command=[python, "aeos/scripts/ecosystem_contracts.py", "dotnet"]),
    ]
    selected = commands if include_optional else [cmd for cmd in commands if not cmd.optional]
    if only:
        selected = [cmd for cmd in selected if cmd.name in only]
    return selected


def is_available(binary: str | None) -> bool:
    if not binary:
        return True
    if "/" in binary:
        return Path(binary).exists()
    return tool_executable(binary, REPO_ROOT) is not None


def run_command(command: TestCommand) -> int:
    if not is_available(command.required_binary):
        if command.fallback_command:
            print(f"RUN {command.name} contract adapter: {' '.join(command.fallback_command)}")
            completed = subprocess.run(command.fallback_command, cwd=REPO_ROOT)
            if completed.returncode:
                print(f"FAIL {command.name} contract adapter: {completed.returncode}")
            else:
                print(f"PASS {command.name} contract adapter")
            return completed.returncode
        print(f"FAIL {command.name}: missing {command.required_binary}")
        return 1
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
    parser.add_argument("--only", action="append", default=[], help="Run only the named matrix entry. Can be passed more than once.")
    args = parser.parse_args(argv)

    failures = 0
    only = set(args.only) if args.only else None
    for command in build_commands(include_optional=args.include_optional, only=only):
        failures += 1 if run_command(command) else 0
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
