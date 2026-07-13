#!/usr/bin/env python3
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md", "README.md", "AGENT.md", "schemas/output.schema.json",
    "templates/REPORT.template.md", "knowledge/KNOWLEDGE.md",
    "knowledge/NEGATIVE_KNOWLEDGE.md", "knowledge/POSITIVE_KNOWLEDGE.md",
    "memory/EXECUTIONS.md", "memory/LESSONS.md", "memory/FAILURES.md",
    "memory/PATTERNS.md"
]
missing = [p for p in required if not (root / p).exists()]
text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
sections = ["Identity", "Mission", "Activation", "Non-activation", "Scope", "Inputs",
            "Outputs", "Workflow", "Evidence", "Stop conditions", "Completion"]
missing_sections = [
    s for s in sections
    if not re.search(rf"^##+\s+\d*\.?\s*{re.escape(s)}\b", text, re.M | re.I)
]
try:
    json.loads((root / "schemas/output.schema.json").read_text(encoding="utf-8"))
except Exception as exc:
    print(f"INVALID_SCHEMA: {exc}")
    raise SystemExit(1)
if missing or missing_sections:
    print({"missing": missing, "missing_sections": missing_sections})
    raise SystemExit(1)
print("PASS")
