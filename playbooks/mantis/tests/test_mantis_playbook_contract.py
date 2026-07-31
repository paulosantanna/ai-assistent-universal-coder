from pathlib import Path

import yaml


def test_mantis_playbook_contract():
    root = Path(__file__).resolve().parents[1]
    data = yaml.safe_load((root / "playbook.yaml").read_text(encoding="utf-8"))
    playbook = data["playbook"]
    assert playbook["id"] == "mantis"
    assert playbook["entry"]["skill"] == "mantis-meta-agent"
    assert "defensive-security-only" in playbook["policies"]
    skills = {step["skill"] for wave in playbook["waves"] for step in wave.get("steps", []) if "skill" in step}
    expected = {"mantis-architecture", "mantis-calibrate", "mantis-chain", "mantis-critic", "mantis-dedupe", "mantis-history", "mantis-meta-agent", "mantis-patch", "mantis-pipeline-adapter", "mantis-plan", "mantis-reflect", "mantis-report", "mantis-reproduce", "mantis-researcher", "mantis-review", "mantis-structural-index", "mantis-summarize", "mantis-threat-model"}
    assert expected <= skills
    assert any("VERIFIED_SECURE" in item for item in playbook["completion"]["requires"])
