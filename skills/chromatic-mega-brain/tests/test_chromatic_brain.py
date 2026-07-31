from pathlib import Path
import importlib.util
import json
import sys

module_path = Path(__file__).resolve().parents[1] / "scripts" / "chromatic_brain.py"
spec = importlib.util.spec_from_file_location("chromatic_brain", module_path)
module = importlib.util.module_from_spec(spec)
sys.modules["chromatic_brain"] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_architecture_selection():
    colors = module.select_colors("Analyze architecture, security risks and implementation plan")
    assert "WHITE" in colors
    assert "BLUE" in colors
    assert "RED" in colors
    assert "GREEN" in colors


def test_minimum_two_colors():
    colors = module.select_colors("A complex decision")
    assert len(colors) >= 2


def test_maximum_colors():
    colors = module.select_colors("architecture security performance knowledge user constraints implementation evidence", 3)
    assert len(colors) <= 3


def test_inventory_discovers_skills_and_playbooks_with_learning_contract(tmp_path):
    skill = tmp_path / "skills" / "sample-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: Sample Skill\n---\n"
        "# Skill\n\n"
        "## Allowed Actions\n\n- inspect evidence\n\n"
        "## Forbidden Actions\n\n- fabricate outputs\n",
        encoding="utf-8",
    )
    (skill / "knowledge").mkdir()
    (skill / "knowledge" / "POSITIVE_KNOWLEDGE.md").write_text(
        "# POSITIVE_KNOWLEDGE.md\n\nPreferred patterns:\n\n- reuse local contracts\n",
        encoding="utf-8",
    )
    (skill / "knowledge" / "NEGATIVE_KNOWLEDGE.md").write_text(
        "# NEGATIVE_KNOWLEDGE.md\n\nKnown failure patterns:\n\n- bypass judge review\n",
        encoding="utf-8",
    )
    playbook = tmp_path / "playbooks" / "sample"
    playbook.mkdir(parents=True)
    (playbook / "playbook.yaml").write_text(
        "playbook:\n"
        "  id: sample-playbook\n"
        "  policies:\n"
        "    - evidence-before-claims\n"
        "    - no-auto-deploy\n",
        encoding="utf-8",
    )

    payload = module.integration_payload(tmp_path)
    assert payload["summary"] == {"skills": 1, "playbooks": 1, "total": 2}
    entities = {item["id"]: item for item in payload["entities"]}
    assert entities["sample-skill"]["do"]
    assert entities["sample-skill"]["do_not"]
    assert "reuse local contracts" in entities["sample-skill"]["do"]
    assert "bypass judge review" in entities["sample-skill"]["do_not"]
    assert any("evidence-before-claims" in item for item in entities["sample-playbook"]["do"])
    assert any("no-auto-deploy" in item for item in entities["sample-playbook"]["do_not"])


def test_sync_integration_writes_memory_index(tmp_path):
    skill = tmp_path / "skills" / "sample-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: Sample Skill\n---\n# Skill\n", encoding="utf-8")
    output = tmp_path / "skills" / "chromatic-mega-brain" / "memory"

    json_path, md_path = module.write_integration_memory(tmp_path, output)

    assert json_path.exists()
    assert md_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["learning_contract"]["do"]
    assert payload["learning_contract"]["do_not"]
    assert payload["summary"]["skills"] == 1
    assert "Status: CANDIDATE_LEARNING" in md_path.read_text(encoding="utf-8")


def test_repository_inventory_covers_all_repository_skills_and_playbooks():
    repo_root = Path(__file__).resolve().parents[3]
    payload = module.integration_payload(repo_root)
    indexed_paths = {item["path"] for item in payload["entities"]}
    expected_skills = {
        path.relative_to(repo_root).as_posix()
        for path in repo_root.rglob("SKILL.md")
        if not any(part in module.EXCLUDED_DIRS for part in path.relative_to(repo_root).parts)
    }
    expected_playbooks = {
        path.relative_to(repo_root).as_posix()
        for path in repo_root.rglob("*.yaml")
        if not any(part in module.EXCLUDED_DIRS for part in path.relative_to(repo_root).parts)
        and (path.name == "playbook.yaml" or path.name.endswith(".playbook.yaml"))
    }
    assert expected_skills <= indexed_paths
    assert expected_playbooks <= indexed_paths


