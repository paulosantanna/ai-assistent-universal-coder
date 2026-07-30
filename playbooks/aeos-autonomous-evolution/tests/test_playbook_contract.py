from pathlib import Path

import yaml


def test_playbook_contract():
    root = Path(__file__).resolve().parents[1]
    data = yaml.safe_load((root / "playbook.yaml").read_text(encoding="utf-8"))
    playbook = data["playbook"]

    assert playbook["id"] == "aeos-autonomous-evolution"
    assert playbook["entry"]["skill"] == "aeos-autonomous-learning-governor"

    skills = {
        step["skill"]
        for wave in playbook["waves"]
        for step in wave.get("steps", [])
        if "skill" in step
    }

    assert "aeos-autonomous-learning-governor" in skills
    assert "telemetry-bug-root-cause-solver" in skills
    assert "kubernetes-code-context-mapper" in skills
    assert "test-generation" in skills
    assert "diff-reviewer" in skills

    assert "api-memory-by-org-project-acronym" in playbook["policies"]
    assert any("memory target" in item for item in playbook["completion"]["requires"])
