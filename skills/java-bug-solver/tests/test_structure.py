import json
from pathlib import Path

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


def test_required_files():
    root = Path(__file__).resolve().parents[1]
    for rel in ["SKILL.md", "README.md", "schemas/output.schema.json", "templates/OUTPUT.template.md"]:
        assert (root / rel).exists()


def test_deep_bug_analysis_contract_terms():
    root = Path(__file__).resolve().parents[1]
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    for term in REQUIRED_TERMS:
        assert term in text


def test_output_schema_requires_deep_analysis_bundle():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "schemas/output.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    for field in REQUIRED_SCHEMA_FIELDS:
        assert field in required