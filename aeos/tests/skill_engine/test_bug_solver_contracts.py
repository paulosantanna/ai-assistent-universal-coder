from pathlib import Path

import yaml


BUG_SOLVER_IDS = {
    "java-docs-bug-solver",
    "python-docs-bug-solver",
    "node-bug-solver",
    "typescript-bug-solver",
    "angular-bug-solver",
    "javascript-bug-solver",
    "python-bug-solver-skill",
}
REQUIRED_INPUTS = {
    "target_identifier",
    "branch_commit_worktree_scope",
    "github_actions_evidence_or_access",
    "subagent_handoff_refs",
    "specs_preflight_ref",
}
REQUIRED_TERMS = [
    "Mandatory Deep Bug Analysis Before Planning",
    "HANDOFF.md",
    "LEARNING.md",
    "MEMORY.md",
    "PROGRESS.md",
    "README.md",
    "linha-do-tempo-runs.md",
    "Diagnostico.md",
    "PROPOSTA_CORRECAO.md",
    "worktree",
    "GitHub Actions",
    "subagents",
    "top-down exception-chain",
    "root cause",
]


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_registry() -> list[dict]:
    registry_path = _workspace_root() / "aeos" / "registries" / "skills.registry.yaml"
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    skills = data.get("skills", [])
    assert isinstance(skills, list)
    return skills


def test_active_bug_solver_registry_entries_require_deep_analysis_inputs_and_gates():
    entries = {entry["id"]: entry for entry in _load_registry() if entry.get("id") in BUG_SOLVER_IDS}
    assert set(entries) == BUG_SOLVER_IDS

    for skill_id, entry in entries.items():
        required_inputs = set(entry.get("required_inputs", []))
        assert REQUIRED_INPUTS <= required_inputs, skill_id

        searchable = "\n".join(
            str(item)
            for key in ("quality_gates", "stop_conditions")
            for item in entry.get(key, [])
        )
        for term in [
            "linha-do-tempo-runs.md",
            "worktree",
            "GitHub Actions",
            "subagents",
            "top-down exception chain",
            "root cause",
            "PROPOSTA_CORRECAO.md",
        ]:
            assert term in searchable, skill_id


def test_active_bug_solver_skill_files_contain_deep_analysis_contract():
    root = _workspace_root()
    entries = [entry for entry in _load_registry() if entry.get("id") in BUG_SOLVER_IDS]

    for entry in entries:
        skill_path = root / entry["path"]
        text = skill_path.read_text(encoding="utf-8")
        for term in REQUIRED_TERMS:
            assert term in text, entry["id"]