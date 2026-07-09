import pytest
import json
from pathlib import Path
from aeos.core.release.release_candidate_builder import ReleaseCandidateBuilder
from aeos.core.release.release_models import ReleaseStatus, ReleaseBlockerCategory


class TestReleaseCandidateBuilder:
    def test_build_with_no_evidence(self, tmp_path: Path):
        builder = ReleaseCandidateBuilder(workspace_root=str(tmp_path))
        candidate = builder.build("exec-001")
        assert candidate.candidate_id.startswith("rc-")
        assert candidate.status == ReleaseStatus.PASS

    def test_build_with_judge_blocked(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "judge-result.json").write_text(json.dumps({
            "status": "BLOCKED", "score": 0.6,
        }))

        builder = ReleaseCandidateBuilder(workspace_root=str(tmp_path))
        candidate = builder.build("exec-001")
        assert candidate.judge_status == "BLOCKED"
        assert any(b.category == ReleaseBlockerCategory.JUDGE_BLOCKED for b in candidate.blockers)

    def test_build_with_evals_below_threshold(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "eval-scorecard.json").write_text(json.dumps({
            "passed": 20, "total_cases": 25, "overall_score": 0.80,
        }))

        builder = ReleaseCandidateBuilder(workspace_root=str(tmp_path))
        candidate = builder.build("exec-001")
        assert any(b.category == ReleaseBlockerCategory.EVALS_BELOW_THRESHOLD for b in candidate.blockers)

    def test_build_with_readiness_blocked(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "production-readiness-scorecard.json").write_text(json.dumps({
            "status": "BLOCKED", "overall_score": 0.80,
        }))

        builder = ReleaseCandidateBuilder(workspace_root=str(tmp_path))
        candidate = builder.build("exec-001")
        assert any(b.category == ReleaseBlockerCategory.READINESS_BLOCKED for b in candidate.blockers)

    def test_build_with_all_gates_pass(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "judge-result.json").write_text(json.dumps({
            "status": "PASS", "score": 0.98,
        }))
        (exec_dir / "eval-scorecard.json").write_text(json.dumps({
            "passed": 47, "total_cases": 47, "overall_score": 1.0,
        }))
        (exec_dir / "production-readiness-scorecard.json").write_text(json.dumps({
            "status": "PASS", "overall_score": 0.99,
        }))

        builder = ReleaseCandidateBuilder(workspace_root=str(tmp_path))
        candidate = builder.build("exec-001")
        assert candidate.status == ReleaseStatus.PASS
        assert len(candidate.blockers) == 0
