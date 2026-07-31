from pathlib import Path

import yaml


def test_playbook_contract():
    root = Path(__file__).resolve().parents[1]
    data = yaml.safe_load((root / "playbook.yaml").read_text(encoding="utf-8"))
    playbook = data["playbook"]
    assert playbook["id"] == "analayze-metricas"
    skills = {
        step["skill"]
        for wave in playbook["waves"]
        for step in wave.get("steps", [])
        if "skill" in step
    }
    assert "dynatrace-observability-staff" in skills
    assert "grafana-observability-staff" in skills
    assert "kubernetes-observability-staff" in skills
    assert "openshift-observability-staff" in skills
    assert "splunk-observability-staff" in skills
    assert "observability-root-cause-integrator" in skills
    isolated_steps = [
        step for wave in playbook["waves"] for step in wave.get("steps", []) if step["id"].startswith("W1-")
    ]
    assert all(step.get("isolation") == "no_peer_agent_communication" for step in isolated_steps)
