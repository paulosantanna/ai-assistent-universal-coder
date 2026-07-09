#!/usr/bin/env python3
"""
AEOS Release Candidate Smoke Test
Tests release candidate building, gate evaluation, and blocking logic.
"""
import sys
import json
from pathlib import Path
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def test_build_candidate_pass():
    tmp = Path(tempfile.mkdtemp())
    ev_dir = tmp / ".aeos" / "evidence" / "exec-rel-pass"
    ev_dir.mkdir(parents=True, exist_ok=True)

    (ev_dir / "judge-result.json").write_text(json.dumps({"status": "PASS", "score": 0.98}))
    (ev_dir / "eval-scorecard.json").write_text(json.dumps({"passed": 47, "total_cases": 47, "overall_score": 1.0}))
    (ev_dir / "production-readiness-scorecard.json").write_text(json.dumps({"status": "PASS", "overall_score": 0.99}))

    from aeos.core.release.release_candidate_builder import ReleaseCandidateBuilder
    from aeos.core.release.release_models import ReleaseStatus

    builder = ReleaseCandidateBuilder(workspace_root=str(tmp))
    candidate = builder.build("exec-rel-pass")

    assert candidate.status == ReleaseStatus.PASS
    assert len(candidate.blockers) == 0
    assert candidate.judge_status == "PASS"
    assert candidate.evals_score == 1.0
    assert candidate.readiness_status == "PASS"
    print("  [PASS] Build release candidate with all gates passing")


def test_build_candidate_judge_blocked():
    tmp = Path(tempfile.mkdtemp())
    ev_dir = tmp / ".aeos" / "evidence" / "exec-judge-blocked"
    ev_dir.mkdir(parents=True, exist_ok=True)

    (ev_dir / "judge-result.json").write_text(json.dumps({"status": "BLOCKED", "score": 0.6}))

    from aeos.core.release.release_candidate_builder import ReleaseCandidateBuilder
    from aeos.core.release.release_models import ReleaseStatus, ReleaseBlockerCategory

    builder = ReleaseCandidateBuilder(workspace_root=str(tmp))
    candidate = builder.build("exec-judge-blocked")

    assert candidate.status == ReleaseStatus.BLOCKED
    assert any(b.category == ReleaseBlockerCategory.JUDGE_BLOCKED for b in candidate.blockers)
    print("  [PASS] Judge BLOCKED correctly blocks release")


def test_build_candidate_evals_below_threshold():
    tmp = Path(tempfile.mkdtemp())
    ev_dir = tmp / ".aeos" / "evidence" / "exec-evals-low"
    ev_dir.mkdir(parents=True, exist_ok=True)

    (ev_dir / "eval-scorecard.json").write_text(json.dumps({"passed": 40, "total_cases": 47, "overall_score": 0.85}))

    from aeos.core.release.release_candidate_builder import ReleaseCandidateBuilder
    from aeos.core.release.release_models import ReleaseStatus, ReleaseBlockerCategory

    builder = ReleaseCandidateBuilder(workspace_root=str(tmp))
    candidate = builder.build("exec-evals-low")

    assert any(b.category == ReleaseBlockerCategory.EVALS_BELOW_THRESHOLD for b in candidate.blockers)
    print("  [PASS] Evals below threshold correctly blocks release")


def test_build_candidate_readiness_blocked():
    tmp = Path(tempfile.mkdtemp())
    ev_dir = tmp / ".aeos" / "evidence" / "exec-readiness-blocked"
    ev_dir.mkdir(parents=True, exist_ok=True)

    (ev_dir / "production-readiness-scorecard.json").write_text(json.dumps({"status": "BLOCKED", "overall_score": 0.80}))

    from aeos.core.release.release_candidate_builder import ReleaseCandidateBuilder
    from aeos.core.release.release_models import ReleaseStatus, ReleaseBlockerCategory

    builder = ReleaseCandidateBuilder(workspace_root=str(tmp))
    candidate = builder.build("exec-readiness-blocked")

    assert any(b.category == ReleaseBlockerCategory.READINESS_BLOCKED for b in candidate.blockers)
    print("  [PASS] Readiness BLOCKED correctly blocks release")


def test_gate_evaluation():
    from aeos.core.release.release_gate import ReleaseGate
    from aeos.core.release.release_models import ReleaseCandidate, ReleaseStatus

    candidate = ReleaseCandidate(
        candidate_id="rc-gate",
        version="1.0.0",
        created_at="2025-01-01T00:00:00",
        status=ReleaseStatus.PASS,
        judge_status="PASS",
        judge_score=0.98,
        evals_passed=47,
        evals_total=47,
        evals_score=1.0,
        readiness_status="PASS",
        readiness_score=0.99,
        package_verified=True,
    )
    result = ReleaseGate.evaluate(candidate)
    assert result.passed
    assert ReleaseGate.can_release(result)
    print("  [PASS] Release gate passes clean candidate")

    blocked_candidate = ReleaseCandidate(
        candidate_id="rc-blocked",
        version="1.0.0",
        created_at="2025-01-01T00:00:00",
        status=ReleaseStatus.PENDING,
        judge_status="BLOCKED",
        judge_score=0.6,
    )
    result = ReleaseGate.evaluate(blocked_candidate)
    assert not result.passed
    assert ReleaseGate.is_blocked(result)
    print("  [PASS] Release gate blocks BLOCKED candidate")


def test_release_reporter():
    from aeos.core.release.release_reporter import ReleaseReporter
    from aeos.core.release.release_models import ReleaseCandidate, ReleaseStatus

    candidate = ReleaseCandidate(
        candidate_id="rc-report",
        version="1.0.0",
        created_at="2025-01-01T00:00:00",
        status=ReleaseStatus.PASS,
        judge_status="PASS",
        judge_score=0.98,
        evals_passed=47,
        evals_total=47,
        evals_score=1.0,
        readiness_status="PASS",
        readiness_score=0.99,
        package_verified=True,
        summary="All gates passed",
    )
    report = ReleaseReporter.generate_report(candidate)
    assert "Release Candidate Report" in report
    assert "PASS" in report

    from aeos.core.release.release_gate import ReleaseGate
    result = ReleaseGate.evaluate(candidate)
    gate_report = ReleaseReporter.generate_gate_result_report(result)
    assert "Release Gate Result" in gate_report
    print("  [PASS] Release reports generated")


def main():
    print("=" * 60)
    print("AEOS Release Candidate Smoke Test")
    print("=" * 60)
    failures = 0
    tests = [
        ("build_candidate_pass", test_build_candidate_pass),
        ("build_candidate_judge_blocked", test_build_candidate_judge_blocked),
        ("build_candidate_evals_below_threshold", test_build_candidate_evals_below_threshold),
        ("build_candidate_readiness_blocked", test_build_candidate_readiness_blocked),
        ("gate_evaluation", test_gate_evaluation),
        ("release_reporter", test_release_reporter),
    ]
    for name, fn in tests:
        try:
            fn()
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            import traceback
            traceback.print_exc()
            failures += 1
    print()
    if failures == 0:
        print(f"RELEASE CANDIDATE SMOKE TEST PASSED ({len(tests)}/{len(tests)})")
        return 0
    else:
        print(f"RELEASE CANDIDATE SMOKE TEST FAILED ({len(tests)-failures}/{len(tests)} failures={failures})")
        return 1


if __name__ == "__main__":
    sys.exit(main())