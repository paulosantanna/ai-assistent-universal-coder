#!/usr/bin/env python3
"""Fail-fast structural guard for repository hygiene regressions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".aeos",
    ".pytest_cache",
    ".tools",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "target",
    "__pycache__",
}
CONFLICT_MARKERS = ("<<<<<<<", ">>>>>>>")
MANIFEST_FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache", "node_modules"}
MANIFEST_FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def render(self) -> str:
        return f"{self.code}: {self.path}: {self.message}"


def iter_files(root: Path, extra_excluded_dirs: set[str] | None = None) -> list[Path]:
    excluded = DEFAULT_EXCLUDED_DIRS | (extra_excluded_dirs or set())
    files: list[Path] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in excluded for part in rel.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def git_tracked_files(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line for line in completed.stdout.splitlines() if line]


def check_no_tracked_ide_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel in git_tracked_files(root):
        if (rel == ".idea" or rel.startswith(".idea/")) and (root / rel).exists():
            findings.append(Finding("TRACKED_IDE_FILE", rel, "IDE metadata must not be tracked"))
    return findings


def check_no_nested_src(root: Path) -> list[Finding]:
    nested = root / "src" / "src"
    if not nested.exists():
        return []
    return [
        Finding("NESTED_SRC_FILE", str(path.relative_to(root)), "Use a single src root")
        for path in nested.rglob("*")
        if path.is_file()
    ]


def check_no_conflict_markers(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root, extra_excluded_dirs={"artifacts"}):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(CONFLICT_MARKERS):
                rel = path.relative_to(root)
                findings.append(Finding("MERGE_CONFLICT_MARKER", f"{rel}:{lineno}", stripped))
    return findings


def manifest_entry_path(entry: object) -> str | None:
    if isinstance(entry, dict) and isinstance(entry.get("path"), str):
        return entry["path"]
    return None


def is_forbidden_manifest_path(path: str) -> bool:
    parts = set(Path(path).parts)
    return bool(parts & MANIFEST_FORBIDDEN_PARTS) or Path(path).suffix in MANIFEST_FORBIDDEN_SUFFIXES


def check_manifests(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for manifest in root.rglob("MANIFEST.json"):
        rel_manifest = manifest.relative_to(root)
        if any(part in DEFAULT_EXCLUDED_DIRS for part in rel_manifest.parts):
            continue
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(Finding("INVALID_MANIFEST_JSON", str(rel_manifest), str(exc)))
            continue
        for entry in payload.get("files", []):
            entry_path = manifest_entry_path(entry)
            if entry_path and is_forbidden_manifest_path(entry_path):
                findings.append(
                    Finding(
                        "MANIFEST_FORBIDDEN_ARTIFACT",
                        f"{rel_manifest}:{entry_path}",
                        "manifest must not list cache/runtime artifacts",
                    )
                )
    return findings


def check_registries(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    registry_dir = root / "aeos" / "registries"
    for registry in registry_dir.glob("*.yaml"):
        try:
            payload = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            findings.append(Finding("INVALID_REGISTRY_YAML", str(registry.relative_to(root)), str(exc)))
            continue
        for key, entries in payload.items():
            if not isinstance(entries, list):
                continue
            ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
            duplicates = sorted({item for item in ids if item and ids.count(item) > 1})
            for duplicate in duplicates:
                findings.append(
                    Finding(
                        "DUPLICATE_REGISTRY_ID",
                        str(registry.relative_to(root)),
                        f"{key} contains duplicate id {duplicate}",
                    )
                )
    return findings


def run(root: Path) -> list[Finding]:
    return [
        *check_no_tracked_ide_files(root),
        *check_no_nested_src(root),
        *check_no_conflict_markers(root),
        *check_manifests(root),
        *check_registries(root),
    ]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AEOS structural guardrails.")
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(args.root).resolve()
    findings = run(root)
    if findings:
        print("AEOS structural guard: FAILED")
        for finding in findings:
            print(f"- {finding.render()}")
        return 1
    print("AEOS structural guard: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
