#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import py_compile
import re
import subprocess
import sys
from typing import Callable

import yaml


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "src/medical_research_mcp/server.py",
    "src/medical_research_mcp/AI_architecture.py",
    "src/medical_research_mcp/AI_architecture_best_practices.py",
    "src/medical_research_mcp/AI_trainning_pipeline.py",
    "src/medical_research_mcp/AI_OWASP.py",
    "src/medical_research_mcp/AI_best_practises.py",
    "src/medical_research_mcp/python_best_practises.py",
    "src/medical_research_mcp/repository.py",
    "src/medical_research_mcp/research.py",
    "src/medical_research_mcp/continuos_learning.py",
    "src/medical_research_mcp/continuos_learning_architecture.py",
    "src/medical_research_mcp/RAG.py",
    "src/medical_research_mcp/lora_qora_dora_doubleLora.py",
    "src/medical_research_mcp/bm25.py",
    "src/medical_research_mcp/expert_validator(accepts only with 10.0).py",
    "src/medical_research_mcp/expert_validator.py",
    "src/medical_research_mcp/subagents.py",
    "src/medical_research_mcp/qulified_sites_for_medical_researchs_around_world.py",
    "src/medical_research_mcp/audit.py",
    "src/medical_research_mcp/planning.py",
    "src/medical_research_mcp/models.py",
    "playbooks/MEDICAL_AI_COMPLETE_PLAYBOOK.md",
    "skills/medical-ai-engineering/SKILL.md",
    "skills/medical-ai-engineering/handover",
    "skills/medical-ai-engineering/knowledge",
    "skills/medical-ai-engineering/learning",
    "skills/medical-ai-engineering/subagents",
    "skills/medical-ai-engineering/memory",
    "config/disease-profile.yaml",
    "config/mcp-server.json",
    "schemas/evidence.schema.json",
    "docs/ARCHITECTURE.md",
    "docs/REGULATORY_AND_SCIENTIFIC_BOUNDARIES.md",
    "tests",
    "pyproject.toml",
    "SOURCES.md",
    "README.md",
]

EXPECTED_TOOLS = {
    "repository_scan",
    "repository_architecture_inventory",
    "medical_ai_audit",
    "architecture_recommendation",
    "architecture_best_practices_gate",
    "training_pipeline_design",
    "training_pipeline_audit",
    "owasp_ai_gate",
    "rag_quality_gate",
    "continuous_learning_quality_gate",
    "adapter_recommendation",
    "bm25_search",
    "qualified_medical_sources",
    "build_disease_research_query",
    "build_research_method_queries",
    "pubmed_research",
    "pubmed_summaries",
    "europe_pmc_research",
    "clinical_trials_research",
    "medical_evidence_screening_policy",
    "dependency_inventory",
    "osv_vulnerability_query",
    "cisa_known_exploited_vulnerabilities",
    "epss_scores",
    "vulnerability_intelligence_policy",
    "specialized_subagents",
    "token_budget_plan",
    "context_hash",
    "complete_beta_plan",
    "expert_validation_10_0",
    "ai_engineering_practices",
}

FORBIDDEN_PLACEHOLDERS = re.compile(r"\b(TODO|TBD|FIXME|PLACEHOLDER_IMPLEMENTATION)\b", re.I)


def check_structure() -> tuple[bool, list[str]]:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    return not missing, [f"missing: {path}" for path in missing]


def check_python_syntax() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return not errors, errors


def check_json_yaml() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    for path in ROOT.rglob("*.yaml"):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return not errors, errors


def check_server_tools() -> tuple[bool, list[str]]:
    server = ROOT / "src/medical_research_mcp/server.py"
    tree = ast.parse(server.read_text(encoding="utf-8"))
    tools: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr == "tool":
                        tools.add(node.name)
    missing = sorted(EXPECTED_TOOLS - tools)
    return not missing, [f"missing MCP tool: {name}" for name in missing]


def check_subagents() -> tuple[bool, list[str]]:
    files = list((ROOT / "skills/medical-ai-engineering/subagents").glob("*.md"))
    text = (ROOT / "src/medical_research_mcp/subagents.py").read_text(encoding="utf-8")
    errors = []
    if len(files) < 19:
        errors.append(f"only {len(files)} subagent contracts found; expected at least 19")
    for required in [
        "repository-cartographer",
        "architecture-governor",
        "medical-evidence-researcher",
        "data-governance-specialist",
        "rag-specialist",
        "bm25-specialist",
        "adapter-specialist",
        "continuous-learning-specialist",
        "owasp-ai-security-specialist",
        "vulnerability-intelligence-specialist",
        "expert-judge",
    ]:
        if required not in text:
            errors.append(f"runtime subagent missing: {required}")
    return not errors, errors


def check_playbook() -> tuple[bool, list[str]]:
    text = (ROOT / "playbooks/MEDICAL_AI_COMPLETE_PLAYBOOK.md").read_text(encoding="utf-8")
    errors = []
    for phase in range(19):
        if f"Phase {phase}" not in text:
            errors.append(f"playbook phase missing: {phase}")
    for term in [
        "BM25", "RAG", "QLoRA", "DoRA", "continuous learning",
        "CISA KEV", "FIRST EPSS", "BETA_READY_RESEARCH_ONLY",
        "human-research boundary", "10.0",
    ]:
        if term.lower() not in text.lower():
            errors.append(f"playbook concern missing: {term}")
    return not errors, errors


def check_skill_contracts() -> tuple[bool, list[str]]:
    text = (ROOT / "skills/medical-ai-engineering/SKILL.md").read_text(encoding="utf-8")
    errors = []
    for term in [
        "microservices", "modular monolith", "OWASP", "SBOM", "OSV",
        "continuous learning", "simulation", "documentation", "10.0",
        "Token and context policy", "human experimentation",
    ]:
        if term.lower() not in text.lower():
            errors.append(f"skill concern missing: {term}")
    for directory in ["handover", "knowledge", "learning", "subagents", "memory"]:
        if not any((ROOT / f"skills/medical-ai-engineering/{directory}").iterdir()):
            errors.append(f"empty skill directory: {directory}")
    return not errors, errors


def check_scientific_boundaries() -> tuple[bool, list[str]]:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "README.md",
            "docs/REGULATORY_AND_SCIENTIFIC_BOUNDARIES.md",
            "playbooks/MEDICAL_AI_COMPLETE_PLAYBOOK.md",
            "skills/medical-ai-engineering/SKILL.md",
        ]
    ).lower()
    requirements = [
        "research-only",
        "not biological proof",
        "human experimentation",
        "cannot establish a cure",
        "approval",
        "rollback",
    ]
    missing = [term for term in requirements if term not in combined]
    return not missing, [f"boundary statement missing: {term}" for term in missing]


def check_no_placeholders() -> tuple[bool, list[str]]:
    errors = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".md", ".json", ".yaml", ".toml"}:
            continue
        if path.resolve() == Path(__file__).resolve() or path.name.startswith("VALIDATION_REPORT"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = FORBIDDEN_PLACEHOLDERS.search(text)
        if match:
            errors.append(f"{path.relative_to(ROOT)} contains {match.group(0)}")
    return not errors, errors


def run_tests() -> tuple[bool, list[str]]:
    env = os.environ.copy()
    src = str(ROOT / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(ROOT / "tests")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, [output] if output else []


def check_strict_validator_contract() -> tuple[bool, list[str]]:
    text = (ROOT / "src/medical_research_mcp/expert_validator.py").read_text(encoding="utf-8")
    errors = []
    for term in ["score==10", "not failures", "c.passed and c.evidence"]:
        if term not in text:
            errors.append(f"strict validator expression missing: {term}")
    return not errors, errors


CHECKS: list[tuple[str, Callable[[], tuple[bool, list[str]]]]] = [
    ("structure", check_structure),
    ("python_syntax", check_python_syntax),
    ("json_yaml", check_json_yaml),
    ("mcp_tools", check_server_tools),
    ("subagents", check_subagents),
    ("playbook", check_playbook),
    ("skill_contracts", check_skill_contracts),
    ("scientific_boundaries", check_scientific_boundaries),
    ("no_placeholders", check_no_placeholders),
    ("tests", run_tests),
    ("strict_validator", check_strict_validator_contract),
]


def main() -> int:
    results = []
    for name, function in CHECKS:
        passed, details = function()
        results.append({"name": name, "passed": passed, "details": details})
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        if details and (not passed or name == "tests"):
            for detail in details:
                print(detail)

    passed_count = sum(1 for item in results if item["passed"])
    score = round(10.0 * passed_count / len(results), 2)
    accepted = passed_count == len(results) and score == 10.0

    report = {
        "score": score,
        "accepted": accepted,
        "passed": passed_count,
        "total": len(results),
        "results": results,
        "scope": "package structure and executable contract validation; not clinical validation",
    }
    (ROOT / "VALIDATION_REPORT.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps({
        "score": score,
        "accepted": accepted,
        "passed": passed_count,
        "total": len(results),
    }, indent=2))

    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
