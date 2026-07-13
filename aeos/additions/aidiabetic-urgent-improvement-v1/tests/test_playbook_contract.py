from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def test_playbook_has_all_waves_and_final_judge():
    text = (ROOT / "playbooks/aidiabetic-urgent-improvement.playbook.yaml").read_text(encoding="utf-8")
    for wave in ["W0", "W1", "W2", "W3", "W4", "W5"]:
        assert re.search(rf"\bid:\s+{wave}\b", text)
    assert "W5-FINAL" in text
    assert "evidence-readiness-judge" in text

def test_no_auto_merge_or_deploy():
    text = (ROOT / "config/execution-policy.yaml").read_text(encoding="utf-8")
    assert "auto_merge" in text and "auto_deploy" in text
    assert "auto_merge: true" not in text
    assert "auto_deploy: true" not in text
