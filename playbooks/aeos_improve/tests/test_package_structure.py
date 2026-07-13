from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_top_level_contracts():
    for rel in [
        "README.md", "aeos.pack.yaml", "FULL_EXECUTION_PROMPT.md",
        "playbooks/aidiabetic-urgent-improvement.playbook.yaml",
        "config/execution-policy.yaml", "config/quality-gates.yaml",
        "schemas/evidence.schema.json", "scripts/validate_package.py"
    ]:
        assert (ROOT / rel).exists(), rel

def test_exact_skill_count():
    assert len([p for p in (ROOT / "skills").iterdir() if p.is_dir()]) == 19
