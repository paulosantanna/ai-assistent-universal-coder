#!/usr/bin/env python3
"""AEOS Skill Factory generator and validator."""

from __future__ import annotations

import argparse
import hashlib
import json
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import yaml

REQUIRED_SKILL_SECTIONS = [
    "Identity",
    "Mission",
    "Activation",
    "Non-activation",
    "Scope",
    "Inputs",
    "Outputs",
    "Workflow",
    "Evidence",
    "Stop conditions",
    "Completion",
]

FORBIDDEN_PATTERNS = {
    "unfinished placeholder": re.compile(r"\b(TODO|TBD|FIXME|XXX)\b", re.I),
    "fictional certainty": re.compile(r"\b(zero hallucination|never fail|100% perfect|god mode)\b", re.I),
    "unbounded loop": re.compile(r"\b(until 10/10|retry forever|never terminate)\b", re.I),
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
MIN_GENERATED_ARCHITECTURE_LEVEL = 3
MANIFEST_EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
MANIFEST_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

OWNER_AGENT_BY_CATEGORY = {
    "ANALYSIS": "architect",
    "AUDIT": "security",
    "CLINICAL": "security",
    "DATA": "coder",
    "DOCUMENTATION": "documenter",
    "EXECUTION": "coder",
    "GENERATION": "coder",
    "GOVERNANCE": "judge",
    "HYBRID": "coder",
    "MIGRATION": "coder",
    "ORCHESTRATION": "planner",
    "REPAIR": "coder",
    "RESEARCH": "architect",
    "SECURITY": "security",
    "TESTING": "tester",
    "VALIDATION": "judge",
    "AI_ML": "coder",
}

CAPABILITIES_BY_CATEGORY = {
    "AUDIT": ["READ_REPOSITORY", "READ_FILES", "GENERATE_REPORT"],
    "DOCUMENTATION": ["READ_REPOSITORY", "READ_FILES", "WRITE_SANDBOX_FILES", "GENERATE_REPORT"],
    "REPAIR": ["READ_REPOSITORY", "READ_FILES", "PROPOSE_PATCH", "GENERATE_DIFF"],
    "SECURITY": ["READ_REPOSITORY", "READ_FILES", "SCAN_SECRETS", "GENERATE_REPORT"],
    "TESTING": ["READ_REPOSITORY", "READ_FILES", "WRITE_SANDBOX_FILES", "GENERATE_REPORT"],
}
DEFAULT_CAPABILITIES = ["READ_REPOSITORY", "READ_FILES", "GENERATE_REPORT"]


class Finding:
    def __init__(self, severity: str, code: str, message: str, path: str | None = None):
        self.severity = severity
        self.code = code
        self.message = message
        self.path = path

    def render(self) -> str:
        location = f" [{self.path}]" if self.path else ""
        return f"{self.severity:<8} {self.code}: {self.message}{location}"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_manifest_file(path: Path) -> bool:
    if path.name == "MANIFEST.json":
        return False
    if any(part in MANIFEST_EXCLUDED_PARTS for part in path.parts):
        return False
    return path.suffix not in MANIFEST_EXCLUDED_SUFFIXES


def resolve_template(factory_root: Path, filename: str) -> Path:
    candidates = [
        factory_root / "templates" / filename,
        factory_root.parent / "Templates" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Template not found: {filename}. Searched: {searched}")


def extract_metadata(text: str) -> dict[str, str]:
    match = re.search(r"```yaml\s+skill:\s*(.*?)```", text, re.S | re.I)
    if not match:
        return {}
    data: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("-") or ":" not in raw:
            continue
        # Only parse direct scalar children of "skill:" (two-space indentation).
        if len(raw) - len(raw.lstrip(" ")) != 2:
            continue
        line = raw.strip()
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        if value:
            data[key.strip()] = value
    return data


def architecture_files(level: int) -> list[str]:
    required = ["SKILL.md", "README.md"]
    if level >= 2:
        required += ["scripts", "schemas", "templates", "tests"]
    if level >= 3:
        required += ["AGENT.md", "knowledge", "memory", "evaluation"]
    return required


def validate_package(package: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not package.exists() or not package.is_dir():
        return [Finding("ERROR", "PACKAGE_NOT_FOUND", "Package directory does not exist", str(package))]

    skill_md = package / "SKILL.md"
    if not skill_md.exists():
        return [Finding("ERROR", "MISSING_SKILL_MD", "SKILL.md is required", str(skill_md))]

    text = read_text(skill_md)
    metadata = extract_metadata(text)

    for section in REQUIRED_SKILL_SECTIONS:
        if not re.search(rf"^##+\s+\d*\.?\s*{re.escape(section)}\b", text, re.M | re.I):
            findings.append(Finding("ERROR", "MISSING_SECTION", f"Missing section: {section}", "SKILL.md"))

    # Exclude explicitly educational anti-pattern sections and fenced examples.
    active_text = re.sub(
        r"^##+\s+(?:\d+\.\s*)?(?:What not to do|Structure that must not be followed).*?(?=^##+\s|\Z)",
        "",
        text,
        flags=re.M | re.S | re.I,
    )
    active_text = re.sub(r"```.*?```", "", active_text, flags=re.S)
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(active_text):
            findings.append(Finding("ERROR", "FORBIDDEN_PATTERN", f"Contains active {label}", "SKILL.md"))

    slug = metadata.get("slug", package.name)
    if not SLUG_RE.fullmatch(slug):
        findings.append(Finding("ERROR", "INVALID_SLUG", f"Invalid slug: {slug}", "SKILL.md"))

    version = metadata.get("version")
    if not version or not SEMVER_RE.fullmatch(version):
        findings.append(Finding("ERROR", "INVALID_VERSION", "Version must use semantic versioning", "SKILL.md"))

    try:
        level = int(metadata.get("architecture_level", "1"))
    except ValueError:
        level = 0
        findings.append(Finding("ERROR", "INVALID_ARCHITECTURE_LEVEL", "Architecture level must be 1, 2 or 3", "SKILL.md"))

    if level not in {1, 2, 3}:
        findings.append(Finding("ERROR", "INVALID_ARCHITECTURE_LEVEL", f"Unsupported level: {level}", "SKILL.md"))
    else:
        for required in architecture_files(level):
            path = package / required
            if not path.exists():
                findings.append(Finding("ERROR", "MISSING_ARCHITECTURE_ITEM", f"Level {level} requires {required}", required))

    if "Activate" not in text and "activate" not in text:
        findings.append(Finding("ERROR", "MISSING_ACTIVATION", "Activation behavior is not defined", "SKILL.md"))

    if "Do not activate" not in text and "Non-activation" not in text:
        findings.append(Finding("ERROR", "MISSING_EXCLUSIONS", "Non-activation behavior is not defined", "SKILL.md"))

    for md in package.rglob("*.md"):
        content = read_text(md)
        for match in re.finditer(r"`([^`\n]+\.(?:md|py|json|yaml|yml))`", content):
            ref = match.group(1)
            if "<" in ref or "{{" in ref or ref.startswith("http"):
                continue
            candidate = package / ref
            if "/" in ref and not candidate.exists():
                findings.append(Finding("WARN", "UNRESOLVED_REFERENCE", f"Reference may not resolve: {ref}", str(md.relative_to(package))))

    for py in package.rglob("*.py"):
        try:
            py_compile.compile(str(py), doraise=True)
        except py_compile.PyCompileError as exc:
            findings.append(Finding("ERROR", "PYTHON_SYNTAX", str(exc), str(py.relative_to(package))))

    manifest = package / "MANIFEST.json"
    if manifest.exists():
        try:
            manifest_data = json.loads(read_text(manifest))
            for item in manifest_data.get("files", []):
                p = package / item["path"]
                if not is_manifest_file(p):
                    continue
                if not p.exists():
                    findings.append(Finding("ERROR", "MANIFEST_MISSING_FILE", item["path"], "MANIFEST.json"))
                    continue
                actual = hashlib.sha256(p.read_bytes()).hexdigest()
                if actual != item["sha256"]:
                    findings.append(Finding("ERROR", "MANIFEST_HASH_MISMATCH", item["path"], "MANIFEST.json"))
        except (json.JSONDecodeError, KeyError) as exc:
            findings.append(Finding("ERROR", "INVALID_MANIFEST", str(exc), "MANIFEST.json"))

    return findings


def render_template(path: Path, values: dict[str, str]) -> str:
    text = read_text(path)
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def create_learning_modules(target: Path) -> None:
    (target / "knowledge").mkdir(exist_ok=True)
    (target / "memory").mkdir(exist_ok=True)
    modules = {
        "knowledge/KNOWLEDGE.md": (
            "# KNOWLEDGE.md\n\n"
            "Validated domain knowledge for this skill. Promote only facts backed by evidence, tests or repeated successful execution.\n"
        ),
        "knowledge/NEGATIVE_KNOWLEDGE.md": (
            "# NEGATIVE_KNOWLEDGE.md\n\n"
            "Known failures, unsafe shortcuts, false assumptions and prohibited patterns. Check this before choosing an approach.\n"
        ),
        "knowledge/POSITIVE_KNOWLEDGE.md": (
            "# POSITIVE_KNOWLEDGE.md\n\n"
            "Validated successful patterns, reusable heuristics and examples that survived honest evaluation.\n"
        ),
        "knowledge/KNOWLEDGE_PROMOTION.md": (
            "# KNOWLEDGE_PROMOTION.md\n\n"
            "Observation -> Evidence -> Candidate lesson -> Independent validation -> Promotion -> Scheduled revalidation.\n\n"
            "Do not promote a lesson from a single lucky run, unsupported opinion or hidden assumption.\n"
        ),
        "knowledge/CONTINUOUS_LEARNING.md": (
            "# CONTINUOUS_LEARNING.md\n\n"
            "Capture observations, compare against failures, validate with tests or evidence, then promote only reusable lessons.\n"
        ),
        "knowledge/ANTI_FORGETTING.md": (
            "# ANTI_FORGETTING.md\n\n"
            "Before execution, review mission, negative knowledge, positive knowledge, open risks and the honest evaluator checklist.\n"
        ),
        "knowledge/TOKEN_EFFICIENCY.md": (
            "# TOKEN_EFFICIENCY.md\n\n"
            "Load only the knowledge layer required by the current task. Prefer file refs and summaries over copying large context.\n"
        ),
        "memory/EXECUTIONS.md": "# EXECUTIONS.md\n\nRecord notable executions with objective, evidence refs, result and follow-up.\n",
        "memory/LESSONS.md": "# LESSONS.md\n\nReusable lessons awaiting or passing promotion.\n",
        "memory/FAILURES.md": "# FAILURES.md\n\nFailure modes, root causes and prevention rules.\n",
        "memory/PATTERNS.md": "# PATTERNS.md\n\nRecurring patterns and decision heuristics.\n",
        "memory/DECISIONS.md": "# DECISIONS.md\n\nImportant design or operating decisions with rationale and evidence.\n",
        "memory/OPEN_RISKS.md": "# OPEN_RISKS.md\n\nKnown risks, uncertainty and unresolved blockers.\n",
    }
    for rel, content in modules.items():
        (target / rel).write_text(content, encoding="utf-8")


def create_agent_contract(target: Path, name: str, slug: str) -> None:
    (target / "AGENT.md").write_text(
        f"# {name} Agent\n\n"
        "## Operating Role\n\n"
        f"Act as the execution agent for `{slug}`. Keep the skill bounded, evidence-backed and reversible when mutation is involved.\n\n"
        "## Knowledge Layer Order\n\n"
        "1. Read `SKILL.md` for mission, scope and stop conditions.\n"
        "2. Read `knowledge/NEGATIVE_KNOWLEDGE.md` to avoid known failures.\n"
        "3. Read `knowledge/POSITIVE_KNOWLEDGE.md` and `knowledge/KNOWLEDGE.md` only when relevant.\n"
        "4. Read `memory/OPEN_RISKS.md` and `memory/DECISIONS.md` before risky or ambiguous work.\n"
        "5. Apply `evaluation/HONEST_EVALUATOR.md` before reporting completion.\n\n"
        "## Execution Rules\n\n"
        "- Prefer evidence over confidence.\n"
        "- State assumptions and uncertainty explicitly.\n"
        "- Do not hide blockers to make the result look complete.\n"
        "- Record reusable lessons only after validation.\n",
        encoding="utf-8",
    )


def create_honest_evaluator(target: Path) -> None:
    (target / "evaluation").mkdir(exist_ok=True)
    (target / "evaluation" / "HONEST_EVALUATOR.md").write_text(
        "# HONEST_EVALUATOR.md\n\n"
        "Use this checklist before marking work complete.\n\n"
        "## Extremely Honest Review\n\n"
        "- What evidence directly supports each material claim?\n"
        "- What is assumed, guessed or still unverified?\n"
        "- What would fail in production, CI or a fresh workspace?\n"
        "- What user-visible risk remains after the proposed result?\n"
        "- Did any tool, permission, policy or registry boundary get bypassed?\n"
        "- Are secrets, tokens, credentials and sensitive values redacted?\n\n"
        "## Verdict Rules\n\n"
        "- Return `PASS` only when evidence and validation support completion.\n"
        "- Return `REVIEW` when the result is useful but needs human judgment.\n"
        "- Return `BLOCKED` when required input, evidence, permission, tool access or validation is missing.\n",
        encoding="utf-8",
    )


def write_manifest(target: Path) -> None:
    entries = []
    for p in sorted(target.rglob("*")):
        if p.is_file() and is_manifest_file(p.relative_to(target)):
            entries.append({
                "path": str(p.relative_to(target)).replace("\\", "/"),
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "bytes": p.stat().st_size,
            })
    payload = {"skill": target.name, "files": entries}
    (target / "MANIFEST.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def find_aeos_root(start: Path) -> Path | None:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "aeos" / "registries" / "skills.registry.yaml").exists():
            return candidate
    return None


def owner_agent_for(category: str) -> str:
    return OWNER_AGENT_BY_CATEGORY.get(category.upper(), "coder")


def capabilities_for(category: str) -> list[str]:
    return CAPABILITIES_BY_CATEGORY.get(category.upper(), DEFAULT_CAPABILITIES)


def relative_to_workspace(path: Path, workspace: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def registry_contains_skill(registry_path: Path, slug: str) -> bool:
    if not registry_path.exists():
        return False
    try:
        data = yaml.safe_load(read_text(registry_path)) or {}
    except yaml.YAMLError:
        return False
    for entry in data.get("skills") or []:
        if isinstance(entry, dict) and entry.get("id") == slug:
            return True
    return False


def append_skill_registry_entry(registry_path: Path, entry: dict[str, object]) -> None:
    text = read_text(registry_path) if registry_path.exists() else ""
    rendered_entry = yaml.safe_dump({"skills": [entry]}, sort_keys=False, allow_unicode=False)
    lines = rendered_entry.splitlines()
    entry_lines = lines[1:] if lines and lines[0] == "skills:" else lines

    if not text.strip():
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text("skills:\n" + "\n".join(entry_lines) + "\n", encoding="utf-8")
        return

    if not re.search(r"^skills:\s*$", text, re.M):
        raise ValueError(f"Registry does not contain a root 'skills:' key: {registry_path}")

    separator = "" if text.endswith("\n") else "\n"
    registry_path.write_text(text + separator + "\n".join(entry_lines) + "\n", encoding="utf-8")


def register_generated_skill(target: Path, values: dict[str, str], args: argparse.Namespace) -> str:
    if not getattr(args, "register", True):
        return "SKIPPED (--no-register)"

    explicit_registry = getattr(args, "registry", None)
    if explicit_registry:
        registry_path = Path(explicit_registry).resolve()
        workspace = registry_path.parents[2] if len(registry_path.parents) >= 3 else target.resolve().parent
    else:
        workspace = find_aeos_root(target) or find_aeos_root(Path.cwd())
        if workspace is None:
            return "SKIPPED (AEOS registry not found)"
        registry_path = workspace / "aeos" / "registries" / "skills.registry.yaml"

    slug = values["slug"]
    if registry_contains_skill(registry_path, slug):
        return f"SKIPPED (already registered: {slug})"

    category = values["category"]
    entry = {
        "id": slug,
        "path": relative_to_workspace(target / "SKILL.md", workspace),
        "version": "1.0.0",
        "owner_agent": owner_agent_for(category),
        "risk_level": values["risk_level"].lower(),
        "capabilities": capabilities_for(category),
        "production_ready": False,
        "mission": values["description"],
        "required_inputs": ["user_objective", "target_scope", "evidence_refs"],
        "quality_gates": [
            "Facts cite evidence",
            "Assumptions are explicitly marked",
            "Honest evaluator verdict is PASS or REVIEW",
            "No secrets are exposed",
        ],
        "stop_conditions": [
            "Required input missing",
            "Evidence cannot be produced",
            "Permission or policy denied",
            "Honest evaluator returns BLOCKED",
        ],
    }
    append_skill_registry_entry(registry_path, entry)
    return f"REGISTERED: {registry_path}"


def generate(args: argparse.Namespace) -> int:
    factory_root = Path(__file__).resolve().parents[1]
    slug = slugify(args.name)
    target = Path(args.output).resolve() / slug
    effective_level = max(int(args.level), MIN_GENERATED_ARCHITECTURE_LEVEL)

    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"ERROR: target already exists and is not empty: {target}", file=sys.stderr)
        return 2

    target.mkdir(parents=True, exist_ok=True)
    values = {
        "title": args.name,
        "slug": slug,
        "description": args.description,
        "category": args.category,
        "architecture_level": str(effective_level),
        "risk_level": args.risk,
        "activation": args.activation,
        "memory_enabled": "true",
        "human_approval": "true" if args.risk in {"HIGH", "CRITICAL"} else "false",
    }

    (target / "SKILL.md").write_text(
        render_template(resolve_template(factory_root, "SKILL.template.md"), values),
        encoding="utf-8",
    )
    (target / "README.md").write_text(
        render_template(resolve_template(factory_root, "README.template.md"), values),
        encoding="utf-8",
    )

    if effective_level >= 2:
        for folder in ["scripts", "schemas", "templates", "tests"]:
            (target / folder).mkdir(exist_ok=True)
        (target / "scripts" / "validate.py").write_text(
            "#!/usr/bin/env python3\nfrom pathlib import Path\nimport sys\n"
            "required=['SKILL.md','README.md','AGENT.md','knowledge','memory','evaluation/HONEST_EVALUATOR.md']\n"
            "missing=[x for x in required if not (Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()/x).exists()]\n"
            "print('PASS' if not missing else 'FAIL: '+', '.join(missing))\n"
            "raise SystemExit(0 if not missing else 1)\n",
            encoding="utf-8",
        )
        (target / "schemas" / "output.schema.json").write_text(
            json.dumps({
                "type": "object",
                "required": ["status", "facts", "assumptions", "risks", "recommendations", "evidence_refs", "blocking_conditions"],
                "properties": {
                    "status": {"enum": ["PASS", "BLOCKED", "REVIEW"]},
                    "facts": {"type": "array"},
                    "assumptions": {"type": "array"},
                    "risks": {"type": "array"},
                    "recommendations": {"type": "array"},
                    "evidence_refs": {"type": "array"},
                    "blocking_conditions": {"type": "array"},
                },
                "additionalProperties": True,
            }, indent=2),
            encoding="utf-8",
        )
        (target / "templates" / "OUTPUT.template.md").write_text(
            "# Output\n\n"
            "## Status\n\nPASS|BLOCKED|REVIEW\n\n"
            "## Facts\n\n- \n\n"
            "## Assumptions\n\n- \n\n"
            "## Risks\n\n- \n\n"
            "## Recommendations\n\n- \n\n"
            "## Evidence Refs\n\n- \n\n"
            "## Blocking Conditions\n\n- \n",
            encoding="utf-8",
        )
        (target / "tests" / "test_structure.py").write_text(
            "from pathlib import Path\n\n"
            "def test_required_files():\n"
            "    root=Path(__file__).resolve().parents[1]\n"
            "    assert (root/'SKILL.md').exists()\n"
            "    assert (root/'README.md').exists()\n"
            "    assert (root/'AGENT.md').exists()\n"
            "    assert (root/'knowledge'/'NEGATIVE_KNOWLEDGE.md').exists()\n"
            "    assert (root/'evaluation'/'HONEST_EVALUATOR.md').exists()\n",
            encoding="utf-8",
        )

    create_agent_contract(target, args.name, slug)
    create_learning_modules(target)
    create_honest_evaluator(target)

    write_manifest(target)
    findings = validate_package(target)
    for finding in findings:
        print(finding.render())
    errors = [f for f in findings if f.severity == "ERROR"]
    if errors:
        print(f"FAILED_VALIDATION: {len(errors)} error(s)")
        return 1

    try:
        registry_status = register_generated_skill(target, values, args)
    except Exception as exc:
        print(f"FAILED_REGISTRY_UPDATE: {exc}", file=sys.stderr)
        return 1

    print(f"GENERATED_AND_VALIDATED: {target}")
    print(f"REGISTRY_STATUS: {registry_status}")
    return 0


def validate(args: argparse.Namespace) -> int:
    package = Path(args.package).resolve()
    findings = validate_package(package)
    for finding in findings:
        print(finding.render())
    errors = [f for f in findings if f.severity == "ERROR"]
    print(f"Summary: {len(errors)} error(s), {len(findings)-len(errors)} warning(s)")
    return 1 if errors else 0



def infer_from_prompt(prompt: str) -> dict[str, object]:
    """Infer skill metadata from a natural-language prompt using deterministic heuristics."""
    normalized = prompt.strip()
    lower = normalized.lower()

    # Name inference
    name_match = re.search(r"(?:create|generate|build|make)\s+(?:an?\s+)?(.+?)\s+skill\b", normalized, re.I)
    if name_match:
        name = name_match.group(1).strip(" .,:;-")
    else:
        words = re.findall(r"[A-Za-z0-9]+", normalized)
        name = " ".join(words[:5]) or "Generated Skill"

    # Keep names concise
    name = re.sub(r"\bthat\b.*$", "", name, flags=re.I).strip()
    if not name.lower().endswith("skill"):
        name = f"{name} Skill"

    # Category inference
    category = "HYBRID"
    category_map = [
        ("SECURITY", ["security", "vulnerability", "cve", "secret", "owasp"]),
        ("REPAIR", ["bug", "stack trace", "exception", "fix", "repair", "root cause", "regression"]),
        ("TESTING", ["test", "coverage", "qa", "quality assurance"]),
        ("AUDIT", ["audit", "review", "assessment", "compliance"]),
        ("DOCUMENTATION", ["documentation", "docs", "readme"]),
        ("RESEARCH", ["research", "search", "paper", "internet"]),
        ("AI_ML", ["ai", "machine learning", "rag", "llm", "model"]),
        ("DATA", ["data", "database", "etl", "pipeline"]),
        ("ORCHESTRATION", ["orchestrate", "agent", "subagent", "workflow"]),
    ]
    for candidate, keywords in category_map:
        if any(k in lower for k in keywords):
            category = candidate
            break

    # Risk inference
    risk = "MEDIUM"
    if any(k in lower for k in ["production", "clinical", "medical", "security", "credential", "secret", "delete", "migration"]):
        risk = "HIGH"
    if any(k in lower for k in ["irreversible", "patient safety", "critical infrastructure"]):
        risk = "CRITICAL"

    # Architecture level inference
    level = 2
    if any(k in lower for k in ["lesson", "memory", "learn", "knowledge", "continuous learning", "subagent", "agent"]):
        level = 3
    elif any(k in lower for k in ["simple", "minimal", "one file"]):
        level = 1

    description = normalized.rstrip(".")
    activation = f"the user requests {description[0].lower() + description[1:] if description else 'this reusable capability'}"

    return {
        "name": name,
        "description": description,
        "activation": activation,
        "category": category,
        "level": level,
        "risk": risk,
    }


def create_from_prompt(args: argparse.Namespace) -> int:
    inferred = infer_from_prompt(args.prompt)
    generated_args = argparse.Namespace(
        name=args.name or inferred["name"],
        description=args.description or inferred["description"],
        activation=args.activation or inferred["activation"],
        category=args.category or inferred["category"],
        level=args.level or inferred["level"],
        risk=args.risk or inferred["risk"],
        output=args.output,
        force=args.force,
        registry=args.registry,
        register=args.register,
    )

    print("Inferred skill configuration:")
    print(json.dumps({
        "name": generated_args.name,
        "description": generated_args.description,
        "activation": generated_args.activation,
        "category": generated_args.category,
        "level": generated_args.level,
        "risk": generated_args.risk,
        "output": str(Path(generated_args.output).resolve()),
    }, indent=2))

    return generate(generated_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AEOS Skill Factory")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate a new AEOS skill")
    p_gen.add_argument("--name", required=True)
    p_gen.add_argument("--description", required=True)
    p_gen.add_argument("--activation", required=True)
    p_gen.add_argument("--category", default="HYBRID")
    p_gen.add_argument("--level", type=int, choices=[1, 2, 3], default=2)
    p_gen.add_argument("--risk", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="MEDIUM")
    p_gen.add_argument("--output", default=".")
    p_gen.add_argument("--force", action="store_true")
    p_gen.add_argument("--registry", help="Optional skills.registry.yaml path for immediate registration")
    p_gen.add_argument("--no-register", dest="register", action="store_false", help="Generate without updating AEOS registry")
    p_gen.set_defaults(register=True)
    p_gen.set_defaults(func=generate)

    p_create = sub.add_parser("create", help="Create a new AEOS skill from a natural-language prompt")
    p_create.add_argument("--prompt", required=True, help="Natural-language description of the desired skill")
    p_create.add_argument("--name", help="Optional explicit skill name")
    p_create.add_argument("--description", help="Optional explicit description")
    p_create.add_argument("--activation", help="Optional explicit activation rule")
    p_create.add_argument("--category", choices=[
        "EXECUTION", "ANALYSIS", "RESEARCH", "GENERATION", "VALIDATION",
        "AUDIT", "ORCHESTRATION", "REPAIR", "MIGRATION", "DOCUMENTATION",
        "SECURITY", "TESTING", "DATA", "AI_ML", "CLINICAL", "GOVERNANCE", "HYBRID"
    ])
    p_create.add_argument("--level", type=int, choices=[1, 2, 3])
    p_create.add_argument("--risk", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    p_create.add_argument("--output", default=".")
    p_create.add_argument("--force", action="store_true")
    p_create.add_argument("--registry", help="Optional skills.registry.yaml path for immediate registration")
    p_create.add_argument("--no-register", dest="register", action="store_false", help="Create without updating AEOS registry")
    p_create.set_defaults(register=True)
    p_create.set_defaults(func=create_from_prompt)

    p_val = sub.add_parser("validate", help="Validate an AEOS skill package")
    p_val.add_argument("package")
    p_val.set_defaults(func=validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
