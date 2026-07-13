from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def test_all_skills_and_agents_registered():
    skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    sreg = (ROOT / "registries/skills.registry.overlay.yaml").read_text(encoding="utf-8")
    areg = (ROOT / "registries/agents.registry.overlay.yaml").read_text(encoding="utf-8")
    for slug in skills:
        assert re.search(rf"^\s*-\s+id:\s+{re.escape(slug)}\s*$", sreg, re.M), slug
        assert re.search(rf"^\s*-\s+id:\s+{re.escape(slug)}-agent\s*$", areg, re.M), slug
