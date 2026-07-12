#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import py_compile
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
required = [
    "SKILL.md", "AGENT.md",
    "agents/WHITE_AGENT.md", "agents/BLUE_AGENT.md", "agents/RED_AGENT.md",
    "agents/GREEN_AGENT.md", "agents/YELLOW_AGENT.md", "agents/PURPLE_AGENT.md",
    "agents/ORANGE_AGENT.md", "agents/BLACK_AGENT.md",
    "agents/SYNTHESIS_AGENT.md", "agents/JUDGE_AGENT.md",
    "scripts/chromatic_brain.py",
    "schemas/chromatic-run.schema.json",
    "knowledge/KNOWLEDGE.md",
    "knowledge/NEGATIVE_KNOWLEDGE.md",
    "knowledge/POSITIVE_KNOWLEDGE.md",
]
errors = []
for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing: {rel}")

for py in root.rglob("*.py"):
    try:
        py_compile.compile(str(py), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(str(exc))

try:
    json.loads((root / "schemas/chromatic-run.schema.json").read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"Invalid schema: {exc}")

if errors:
    print("\n".join(errors))
    print(f"FAILED: {len(errors)} error(s)")
    raise SystemExit(1)

print("PASS: 0 errors")
