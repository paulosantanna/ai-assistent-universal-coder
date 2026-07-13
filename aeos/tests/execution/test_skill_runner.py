from __future__ import annotations

from pathlib import Path

from aeos.core.execution import ExecutionRequest, SkillResolver, SkillRunner


def test_execution_request_generates_execution_id():
    request = ExecutionRequest(run_type="skill", entity_id="repo-scanner", execution_id="")
    assert request.execution_id.startswith("exec-")


def test_skill_resolver_resolves_registered_skill():
    resolver = SkillResolver(".")
    resolved = resolver.resolve("repo-scanner")
    assert resolved is not None
    assert resolved.skill_id == "repo-scanner"
    assert resolved.contract.is_valid()
    assert resolved.validation["valid"] is True


def test_skill_runner_dry_run_writes_evidence(tmp_path: Path):
    runner = SkillRunner(aeos_root=".", workspace_root=str(tmp_path))
    request = ExecutionRequest(
        run_type="skill",
        entity_id="repo-scanner",
        input={"repository_path": str(tmp_path), "scan_depth": "standard"},
        target_path=str(tmp_path),
        dry_run=True,
    )

    result = runner.run(request)

    assert result.status == "PASS"
    assert result.mode == "dry-run"
    assert result.evidence_refs

    evidence_dir = tmp_path / ".aeos" / "evidence" / result.execution_id
    assert (evidence_dir / "runtime-request.jsonl").exists()
    assert (evidence_dir / "skill-contract-validation.jsonl").exists()
    assert (evidence_dir / "skill-result.jsonl").exists()
    assert (evidence_dir / "runtime-result.jsonl").exists()
    assert (evidence_dir / "runtime-evidence-manifest.json").exists()


def test_skill_runner_blocks_missing_required_input(tmp_path: Path):
    runner = SkillRunner(aeos_root=".", workspace_root=str(tmp_path))
    request = ExecutionRequest(
        run_type="skill",
        entity_id="repo-scanner",
        input={"repository_path": str(tmp_path)},
        target_path=str(tmp_path),
        dry_run=True,
    )

    result = runner.run(request)

    assert result.status == "BLOCKED"
    assert "scan_depth" in " ".join(result.blocking_conditions)


def test_skill_runner_blocks_unknown_skill(tmp_path: Path):
    runner = SkillRunner(aeos_root=".", workspace_root=str(tmp_path))
    request = ExecutionRequest(
        run_type="skill",
        entity_id="missing-skill",
        input={},
        target_path=str(tmp_path),
        dry_run=True,
    )

    result = runner.run(request)

    assert result.status == "BLOCKED"
    assert "not found" in " ".join(result.blocking_conditions).lower()
