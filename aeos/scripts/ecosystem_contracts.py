#!/usr/bin/env python3
"""Validate AEOS language ecosystem contracts when native toolchains are absent."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Contract:
    name: str
    files: tuple[str, ...]
    required_terms: tuple[str, ...]


CONTRACTS = {
    "java-maven": Contract(
        "java-maven",
        ("templates/test-toolchains/java-junit5/pom.xml",),
        ("junit-jupiter", "cucumber-java", "maven-surefire-plugin"),
    ),
    "java-gradle": Contract(
        "java-gradle",
        (
            "templates/test-toolchains/java-gradle-junit5/build.gradle.kts",
            "templates/test-toolchains/java-gradle-junit5/settings.gradle.kts",
        ),
        ("junit-jupiter", "cucumber-java", "useJUnitPlatform"),
    ),
    "go": Contract(
        "go",
        (
            "aeos/templates/projects/go-service/go.mod",
            "aeos/templates/projects/go-service/main.go",
            "aeos/templates/projects/go-service/main_test.go",
        ),
        ("module", "testing", "otel"),
    ),
    "rust": Contract(
        "rust",
        (
            "aeos/templates/projects/rust-service/Cargo.toml",
            "aeos/templates/projects/rust-service/src/main.rs",
            "aeos/templates/projects/rust-service/tests/smoke.rs",
        ),
        ("opentelemetry", "tokio", "assert"),
    ),
    "dotnet": Contract(
        "dotnet",
        (
            "aeos/templates/projects/dotnet-service/AeosService.csproj",
            "aeos/templates/projects/dotnet-service/Program.cs",
            "aeos/templates/projects/dotnet-service/AeosService.Tests/AeosService.Tests.csproj",
        ),
        ("OpenTelemetry", "Microsoft.NET.Test.Sdk", "xunit"),
    ),
}


def validate_contract(name: str, root: Path = REPO_ROOT) -> dict[str, object]:
    if name not in CONTRACTS:
        raise KeyError(f"Unknown ecosystem contract: {name}")
    contract = CONTRACTS[name]
    findings: list[str] = []
    corpus = ""
    for rel in contract.files:
        path = root / rel
        if not path.exists():
            findings.append(f"missing file: {rel}")
            continue
        corpus += "\n" + path.read_text(encoding="utf-8")
    for term in contract.required_terms:
        if term not in corpus:
            findings.append(f"missing required ecosystem term: {term}")
    return {
        "name": name,
        "status": "PASS" if not findings else "FAIL",
        "files": list(contract.files),
        "findings": findings,
        "mode": "native-toolchain-contract-adapter",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AEOS language ecosystem contracts.")
    parser.add_argument("ecosystem", choices=sorted(CONTRACTS))
    parser.add_argument("--root", default=str(REPO_ROOT))
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = validate_contract(args.ecosystem, Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"AEOS ecosystem contract {result['name']}: {result['status']}")
        print(f"Mode: {result['mode']}")
        for file in result["files"]:
            print(f"- {file}")
        for finding in result["findings"]:
            print(f"FAIL: {finding}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
