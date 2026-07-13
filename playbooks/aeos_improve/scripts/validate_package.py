#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REQUIRED_SECTIONS = [
    "Identity", "Mission", "Activation", "Non-activation", "Scope", "Inputs",
    "Outputs", "Workflow", "Evidence", "Stop conditions", "Completion"
]
FORBIDDEN_ACTIVE = [
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"\bFIXME\b", re.I),
    re.compile(r"retry forever", re.I),
    re.compile(r"auto[_ -]?deploy:\s*true", re.I),
    re.compile(r"auto[_ -]?merge:\s*true", re.I),
]
findings = []

def error(code, detail):
    findings.append({"severity": "ERROR", "code": code, "detail": detail})

def check_json(path: Path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error("INVALID_JSON", f"{path.relative_to(ROOT)}: {exc}")

for required in [
    "README.md", "aeos.pack.yaml", "FULL_EXECUTION_PROMPT.md",
    "playbooks/aidiabetic-urgent-improvement.playbook.yaml",
    "playbooks/AIDIABETIC_URGENT_IMPROVEMENT_FULL.md",
    "config/execution-policy.yaml", "config/quality-gates.yaml",
    "config/clinical-safety-policy.yaml", "config/token-budget.yaml",
    "registries/skills.registry.overlay.yaml",
    "registries/agents.registry.overlay.yaml",
    "registries/enterprise-playbooks.registry.overlay.yaml",
    "schemas/evidence.schema.json", "schemas/finding.schema.json",
    "schemas/handoff.schema.json", "schemas/gate-result.schema.json",
]:
    if not (ROOT / required).exists():
        error("MISSING_REQUIRED", required)

skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.exists() else []
if len(skill_dirs) != 19:
    error("SKILL_COUNT", f"expected 19, found {len(skill_dirs)}")

slugs = set()
for skill in skill_dirs:
    for rel in ["SKILL.md", "README.md", "AGENT.md", "scripts", "schemas", "templates", "tests", "knowledge", "memory"]:
        if not (skill / rel).exists():
            error("SKILL_STRUCTURE", f"{skill.name}/{rel}")
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"slug:\s*([a-z0-9-]+)", text)
    if not m:
        error("MISSING_SLUG", skill.name)
    else:
        slug = m.group(1)
        if slug in slugs:
            error("DUPLICATE_SLUG", slug)
        slugs.add(slug)
        if slug != skill.name:
            error("SLUG_PATH_MISMATCH", f"{slug} != {skill.name}")
    if not re.search(r"version:\s*1\.0\.0", text):
        error("INVALID_VERSION", skill.name)
    if not re.search(r"architecture_level:\s*3", text):
        error("INVALID_LEVEL", skill.name)
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##+\s+\d*\.?\s*{re.escape(section)}\b", text, re.M | re.I):
            error("MISSING_SECTION", f"{skill.name}: {section}")

for path in ROOT.rglob("*.json"):
    if path.name != "VALIDATION_REPORT.json":
        check_json(path)

for path in ROOT.rglob("*.py"):
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    except (SyntaxError, UnicodeDecodeError) as exc:
        error("PYTHON_SYNTAX", f"{path.relative_to(ROOT)}: {exc}")

scan_roots = [ROOT / "skills", ROOT / "playbooks", ROOT / "config", ROOT / "agents"]
scan_files = [ROOT / "README.md", ROOT / "FULL_EXECUTION_PROMPT.md", ROOT / "aeos.pack.yaml"]
paths = list(scan_files)
for scan_root in scan_roots:
    if scan_root.exists():
        paths.extend(p for p in scan_root.rglob("*") if p.is_file())
for path in paths:
    if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
        continue
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_ACTIVE:
        if pattern.search(text):
            error("FORBIDDEN_PATTERN", f"{path.relative_to(ROOT)}: {pattern.pattern}")

skills_reg = (ROOT / "registries/skills.registry.overlay.yaml").read_text(encoding="utf-8")
agents_reg = (ROOT / "registries/agents.registry.overlay.yaml").read_text(encoding="utf-8")
for slug in slugs:
    if f"id: {slug}\n" not in skills_reg:
        error("SKILL_NOT_REGISTERED", slug)
    if f"id: {slug}-agent\n" not in agents_reg:
        error("AGENT_NOT_REGISTERED", slug)

manifest_path = ROOT / "MANIFEST.json"
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest.get("files", []):
        p = ROOT / item["path"]
        if not p.exists():
            error("MANIFEST_MISSING", item["path"])
        elif hashlib.sha256(p.read_bytes()).hexdigest() != item["sha256"]:
            error("MANIFEST_HASH_MISMATCH", item["path"])

result = {
    "package": ROOT.name,
    "valid": not findings,
    "error_count": len(findings),
    "findings": findings,
}
(ROOT / "VALIDATION_REPORT.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(ROOT / "VALIDATION_REPORT.txt").write_text(
    ("PASS\n" if not findings else "FAIL\n") +
    "\n".join(f"{x['code']}: {x['detail']}" for x in findings) + "\n",
    encoding="utf-8",
)
print(json.dumps(result, indent=2))
raise SystemExit(0 if not findings else 1)
