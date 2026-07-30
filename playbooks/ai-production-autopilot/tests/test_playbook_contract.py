from pathlib import Path

import yaml


def test_playbook_contract():
    root = Path(__file__).resolve().parents[1]
    data = yaml.safe_load((root / "playbook.yaml").read_text(encoding="utf-8"))
    playbook = data["playbook"]

    assert playbook["id"] == "ai-production-autopilot"
    assert playbook["entry"]["skill"] == "staff-iii-architecture-governor"
    assert playbook["risk"] == "CRITICAL"

    skills = {
        step["skill"]
        for wave in playbook["waves"]
        for step in wave.get("steps", [])
        if "skill" in step
    }

    assert "staff-iii-architecture-governor" in skills
    assert "staff-tdd-code-builder" in skills
    assert "documentation-11-layer-mapper" in skills
    assert "security-audit" in skills
    assert "test-generation" in skills
    assert "diff-reviewer" in skills
    assert "aeos-autonomous-learning-governor" in skills

    policies = set(playbook["policies"])
    assert "tdd-before-code-by-default" in policies
    assert "multi-source-cve-screening" in policies
    assert "honest-10-of-10-gates" in policies
    assert "documentation-11-layers-before-release" in policies
    assert "n8n-through-approved-automation-boundary" in policies

    gates = [
        step
        for wave in playbook["waves"]
        for step in wave.get("steps", [])
        if step.get("requires_score") == 10
    ]
    assert len(gates) >= 4

    completion = "\n".join(playbook["completion"]["requires"])
    assert "PASS_10_10" in completion
    assert "no blocker" in completion
    assert "Mermaid" in completion
    assert "Memory, Handoff, progress, Learning, evidencias and analise" in completion
