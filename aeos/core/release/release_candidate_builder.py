import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from aeos.core.release.release_models import (
    ReleaseCandidate, ReleaseStatus, ReleaseBlocker, ReleaseBlockerCategory,
)
from aeos.core.packaging.package_verifier import PackageVerifier


class ReleaseCandidateBuilder:

    EVIDENCE_DIR = ".aeos/evidence"

    def __init__(self, workspace_root: str | Path):
        self.workspace_root = Path(workspace_root).resolve()

    def build(self, execution_id: str, version: str = "1.0.0") -> ReleaseCandidate:
        execution_dir = self.workspace_root / self.EVIDENCE_DIR / execution_id
        candidate_id = f"rc-{execution_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        candidate = ReleaseCandidate(
            candidate_id=candidate_id,
            version=version,
            created_at=datetime.now(timezone.utc).isoformat(),
            status=ReleaseStatus.PENDING,
        )

        judge_result_path = execution_dir / "judge-result.json"
        if judge_result_path.exists():
            with open(judge_result_path) as f:
                jr = json.load(f)
            candidate.judge_status = jr.get("status")
            candidate.judge_score = jr.get("score")
            if jr.get("status") == "BLOCKED":
                candidate.blockers.append(ReleaseBlocker(
                    category=ReleaseBlockerCategory.JUDGE_BLOCKED,
                    description=f"Judge BLOCKED with score {jr.get('score', 0)}",
                ))

        eval_scorecard_path = execution_dir / "eval-scorecard.json"
        if eval_scorecard_path.exists():
            with open(eval_scorecard_path) as f:
                es = json.load(f)
            candidate.evals_passed = es.get("passed", 0)
            candidate.evals_total = es.get("total_cases", 0)
            candidate.evals_score = es.get("overall_score", 0)
            if es.get("overall_score", 0) < 0.95:
                candidate.blockers.append(ReleaseBlocker(
                    category=ReleaseBlockerCategory.EVALS_BELOW_THRESHOLD,
                    description=f"Evals score {es.get('overall_score', 0):.4f} < 0.95",
                ))

        readiness_path = execution_dir / "production-readiness-scorecard.json"
        if readiness_path.exists():
            with open(readiness_path) as f:
                rs = json.load(f)
            candidate.readiness_status = rs.get("status")
            candidate.readiness_score = rs.get("overall_score", 0)
            if rs.get("status") == "BLOCKED":
                candidate.blockers.append(ReleaseBlocker(
                    category=ReleaseBlockerCategory.READINESS_BLOCKED,
                    description=f"Readiness BLOCKED with score {rs.get('overall_score', 0):.4f}",
                ))

        package_dir = self.workspace_root / ".aeos" / "packages"
        if package_dir.exists():
            for pkg_file in sorted(package_dir.iterdir()):
                if pkg_file.suffix == ".zip" and execution_id in pkg_file.name:
                    verify_result = PackageVerifier.verify(pkg_file)
                    candidate.package_verified = verify_result.verified
                    candidate.package_path = str(pkg_file)
                    if not verify_result.verified:
                        candidate.blockers.append(ReleaseBlocker(
                            category=ReleaseBlockerCategory.PACKAGE_VERIFY_FAILED,
                            description=f"Package verification failed: {'; '.join(verify_result.errors[:3])}",
                        ))
                    break

        if not candidate.blockers:
            candidate.status = ReleaseStatus.PASS
            candidate.summary = "All release gates passed"
        else:
            has_critical = any(b.severity == "critical" for b in candidate.blockers)
            candidate.status = ReleaseStatus.BLOCKED if has_critical else ReleaseStatus.REVIEW
            candidate.summary = f"Release blocked by {len(candidate.blockers)} blocker(s)"

        return candidate
