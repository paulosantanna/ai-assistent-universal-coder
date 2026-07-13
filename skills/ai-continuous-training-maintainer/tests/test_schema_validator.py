"""Validate schemas, finding examples, and recursion rubric."""
import json
from pathlib import Path

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def test_finding_schema_is_valid_json():
    schema_file = SCHEMAS_DIR / "finding.schema.json"
    assert schema_file.is_file()
    data = json.loads(schema_file.read_text(encoding="utf-8"))
    assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "required" in data


def test_execution_schema_is_valid_json():
    schema_file = SCHEMAS_DIR / "execution.schema.json"
    assert schema_file.is_file()
    data = json.loads(schema_file.read_text(encoding="utf-8"))
    assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "required" in data


def test_score_schema_is_valid_json():
    schema_file = SCHEMAS_DIR / "score.schema.json"
    assert schema_file.is_file()
    data = json.loads(schema_file.read_text(encoding="utf-8"))
    assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "required" in data
    assert data["properties"]["score"]["maximum"] == 10.0
    assert data["properties"]["score"]["minimum"] == 0.0


def test_required_files_exist():
    skill_dir = Path(__file__).resolve().parent.parent
    required = [
        "SKILL.md", "README.md", "AGENT.md",
        "ROOT_AGENT.md", "PARENT_AGENT.md", "CHILD_AGENT.md",
        "HANDOFF.md", "MEMORY_SCHEMA.md",
        "KNOWLEDGE_PROMOTION.md", "CONTINUOUS_LEARNING.md",
        "schemas/finding.schema.json",
        "schemas/execution.schema.json",
        "schemas/score.schema.json",
        "templates/report.md",
        "templates/cve_report.md",
        "tests/test_schema_validator.py",
        "tests/POSITIVE_KNOWLEDGE.md",
        "tests/KNOWLEDGE_PROMOTION.md",
        "tests/CONTINUOUS_LEARNING.md",
        "knowledge/KNOWLEDGE.md",
        "knowledge/NEGATIVE_KNOWLEDGE.md",
        "knowledge/POSITIVE_KNOWLEDGE.md",
        "knowledge/KNOWLEDGE_PROMOTION.md",
        "knowledge/CONTINUOUS_LEARNING.md",
        "memory/EXECUTIONS.md",
        "memory/LESSONS.md",
        "memory/FAILURES.md",
        "memory/PATTERNS.md",
    ]
    for path in required:
        assert (skill_dir / path).is_file(), f"Missing required file: {path}"


def test_memory_directories_exist():
    skill_dir = Path(__file__).resolve().parent.parent
    dirs = [
        "memory/root",
        "memory/parents",
        "memory/children/executions",
        "memory/shared",
    ]
    for d in dirs:
        assert (skill_dir / d).is_dir(), f"Missing directory: {d}"


def test_constitutional_files_have_required_sections():
    skill_dir = Path(__file__).resolve().parent.parent
    files_sections = {
        "ROOT_AGENT.md": ["Identity", "authority", "prohibition"],
        "PARENT_AGENT.md": ["Identity", "authority", "prohibition"],
        "CHILD_AGENT.md": ["Identity", "authority"],
        "HANDOFF.md": ["Purpose", "principles", "handoff"],
        "MEMORY_SCHEMA.md": ["Purpose", "Memory classes", "integrity"],
    }
    for fname, sections in files_sections.items():
        content = (skill_dir / fname).read_text(encoding="utf-8")
        for section in sections:
            assert section.lower() in content.lower(), f"{fname} missing section: {section}"


def test_skill_md_contains_recursive_evaluator():
    skill_md = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    assert "Recursive Evaluation Gate" in content
    assert "Quality-Judge" in content
    assert "Deterministic Gates" in content
    assert "Score Rubric" in content
    assert "MAX_RECURSION" in content or "max_recursion" in content
    assert "10.0" in content


def test_agreement_has_judge_rules():
    agent_md = Path(__file__).resolve().parent.parent / "AGENT.md"
    content = agent_md.read_text(encoding="utf-8")
    assert "Quality-Judge" in content
    assert "NUNCA" in content or "nunca" in content
    assert "recursion" in content.lower()
    assert "MAX_RECURSION" in content
