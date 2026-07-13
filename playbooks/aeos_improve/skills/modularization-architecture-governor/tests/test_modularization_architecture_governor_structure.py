from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def test_required_structure():
    for rel in [
        "SKILL.md", "README.md", "AGENT.md", "scripts", "schemas",
        "templates", "tests", "knowledge", "memory"
    ]:
        assert (ROOT / rel).exists(), rel

def test_skill_metadata_and_sections():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert re.search(r"slug:\s+[a-z0-9-]+", text)
    assert re.search(r"version:\s+\d+\.\d+\.\d+", text)
    for section in ["Identity", "Mission", "Activation", "Non-activation",
                    "Scope", "Inputs", "Outputs", "Workflow", "Evidence",
                    "Stop conditions", "Completion"]:
        assert re.search(rf"^##+\s+\d*\.?\s*{section}\b", text, re.M | re.I), section

def test_schema_is_json():
    json.loads((ROOT / "schemas/output.schema.json").read_text(encoding="utf-8"))
