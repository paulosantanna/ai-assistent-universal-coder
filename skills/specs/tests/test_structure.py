from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist():
    for rel in [
        "SKILL.md",
        "README.md",
        "AGENT.md",
        "schemas/output.schema.json",
        "scripts/validate.py",
        "templates/OUTPUT.template.md",
        "templates/SPEC.template.md",
        "references/SPEC_DRIVEN_SOURCES.md",
    ]:
        assert (ROOT / rel).exists(), rel


def test_skill_contract_defines_spec_preflight_gate():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for term in [
        "before any AEOS skill",
        "requirements",
        "acceptance criteria",
        "design",
        "tasks",
        "test applicability matrix",
        "approval gates",
        "evidence gates",
    ]:
        assert term in text


def test_output_schema_requires_traceable_spec_artifacts():
    schema = json.loads((ROOT / "schemas" / "output.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    for field in [
        "spec_id",
        "requirements",
        "acceptance_criteria",
        "design",
        "tasks",
        "test_matrix",
        "approval_gates",
        "evidence_gates",
        "blocking_conditions",
    ]:
        assert field in required


def test_schema_statuses_are_governed():
    schema = json.loads((ROOT / "schemas" / "output.schema.json").read_text(encoding="utf-8"))
    assert set(schema["properties"]["status"]["enum"]) == {"PASS", "REVIEW", "BLOCKED"}
