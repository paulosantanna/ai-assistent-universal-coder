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
    "memory/OPEN_RISKS.md",
    "evaluation/HONEST_EVALUATOR.md",
    "schemas/output.schema.json",
    "templates/OUTPUT.template.md",
    "templates/SPEC.template.md",
    "references/SPEC_DRIVEN_SOURCES.md",
]

REQUIRED_TERMS = [
    "before any AEOS skill",
    "requirements",
    "acceptance criteria",
    "design",
    "tasks",
    "test applicability matrix",
    "approval gates",
    "evidence gates",
    "BLOCKED",
]

REQUIRED_SCHEMA_FIELDS = [
    "spec_id",
    "requirements",
    "acceptance_criteria",
    "design",
    "tasks",
    "test_matrix",
    "approval_gates",
    "evidence_gates",
    "blocking_conditions",
]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            failures.append(f"missing path: {rel}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    lowered = skill_text.lower()
    for term in REQUIRED_TERMS:
        if term.lower() not in lowered:
            failures.append(f"missing skill term: {term}")

    schema_path = root / "schemas" / "output.schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid schema json: {exc}")
        else:
            required = set(schema.get("required", []))
            for field in REQUIRED_SCHEMA_FIELDS:
                if field not in required:
                    failures.append(f"schema field is not required: {field}")

    print("PASS" if not failures else "FAIL")
    for failure in failures:
        print(f"- {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
