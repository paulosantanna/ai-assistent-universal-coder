#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REQUIRED_FILES = ["SKILL.md", "README.md", "schemas/output.schema.json", "templates/OUTPUT.template.md"]
REQUIRED_TERMS = [
    "Mandatory Deep Bug Analysis Before Planning",
    "HANDOFF.md",
    "LEARNING.md",
    "MEMORY.md",
    "PROGRESS.md",
    "README.md",
    "linha-do-tempo-runs.md",
    "Diagnostico.md",
    "PROPOSTA_CORRECAO.md",
    "worktree",
    "GitHub Actions",
    "subagents",
    "top-down exception-chain",
    "root cause",
]
REQUIRED_SCHEMA_FIELDS = [
    "target_workspace",
    "handoff",
    "learning",
    "memory",
    "progress",
    "evidence_bundle",
    "analysis_bundle",
    "subagent_handoffs",
    "exception_chain",
    "root_cause",
    "fix_proposal",
    "verification_plan",
    "blocking_conditions",
]

errors = []
for rel in REQUIRED_FILES:
    if not (ROOT / rel).exists():
        errors.append(f"missing file: {rel}")

skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").exists() else ""
for term in REQUIRED_TERMS:
    if term not in skill_text:
        errors.append(f"SKILL.md missing term: {term}")

schema_path = ROOT / "schemas/output.schema.json"
if schema_path.exists():
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in required:
            errors.append(f"schema missing required field: {field}")

if errors:
    print("FAIL: " + "; ".join(errors))
    raise SystemExit(1)

print("PASS")