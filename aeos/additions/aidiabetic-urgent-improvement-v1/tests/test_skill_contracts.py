from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ["Identity", "Mission", "Activation", "Non-activation", "Scope",
            "Inputs", "Outputs", "Workflow", "Evidence", "Stop conditions",
            "Completion"]

def test_every_skill_level_3_and_complete():
    for skill in (ROOT / "skills").iterdir():
        if not skill.is_dir():
            continue
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        assert "architecture_level: 3" in text
        assert "version: 1.0.0" in text
        for section in SECTIONS:
            assert re.search(rf"^##+\s+\d*\.?\s*{section}\b", text, re.M | re.I), (skill.name, section)
        for rel in ["AGENT.md", "scripts", "schemas", "templates", "tests", "knowledge", "memory"]:
            assert (skill / rel).exists(), (skill.name, rel)
