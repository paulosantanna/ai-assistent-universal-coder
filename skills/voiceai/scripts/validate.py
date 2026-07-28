#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "AGENT.md",
    "knowledge/NEGATIVE_KNOWLEDGE.md",
    "knowledge/POSITIVE_KNOWLEDGE.md",
    "knowledge/KNOWLEDGE.md",
    "memory/OPEN_RISKS.md",
    "evaluation/HONEST_EVALUATOR.md",
    "schemas/output.schema.json",
    "templates/OUTPUT.template.md",
]

REQUIRED_SKILL_TERMS = [
    "consent",
    "literal transcript",
    "mixed-language",
    "video",
    "drive",
    "language tags",
    "joke",
    "out-of-scope",
    "actionable intent",
    "AEOS handoff",
    "skills, MCPs, LSPs, playbooks, guardrails",
]

REQUIRED_SCHEMA_FIELDS = [
    "media_sources",
    "literal_transcript",
    "segments",
    "actionable_intent",
    "out_of_scope_ledger",
    "handoff",
]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            failures.append(f"missing path: {rel}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    lowered = skill_text.lower()
    for term in REQUIRED_SKILL_TERMS:
        if term.lower() not in lowered:
            failures.append(f"missing skill contract term: {term}")

    schema_path = root / "schemas" / "output.schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid output schema json: {exc}")
        else:
            required = set(schema.get("required", []))
            for field in REQUIRED_SCHEMA_FIELDS:
                if field not in required:
                    failures.append(f"schema field is not required: {field}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

