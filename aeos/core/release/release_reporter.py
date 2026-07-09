from datetime import datetime, timezone
from pathlib import Path
from aeos.core.release.release_models import ReleaseCandidate, ReleaseGateResult


class ReleaseReporter:

    @staticmethod
    def generate_report(candidate: ReleaseCandidate) -> str:
        lines = [
            "# AEOS Release Candidate Report",
            "",
            f"- **Candidate ID**: {candidate.candidate_id}",
            f"- **Version**: {candidate.version}",
            f"- **Status**: {candidate.status.value}",
            f"- **Created**: {candidate.created_at}",
            "",
            "## Gates",
            "",
            f"- **Judge**: {candidate.judge_status or 'N/A'} (score: {candidate.judge_score or 'N/A'})",
            f"- **Evals**: {candidate.evals_passed}/{candidate.evals_total} ({candidate.evals_score or 'N/A'})",
            f"- **Readiness**: {candidate.readiness_status or 'N/A'} (score: {candidate.readiness_score or 'N/A'})",
            f"- **Package Verified**: {candidate.package_verified}",
            "",
        ]
        if candidate.blockers:
            lines.extend(["## Blockers", ""])
            for b in candidate.blockers:
                lines.append(f"- [{b.severity}] {b.category.value}: {b.description}")
            lines.append("")
        lines.extend([
            "## Summary",
            "",
            candidate.summary or "No summary available",
            "",
            f"*Report generated at {datetime.now(timezone.utc).isoformat()}*",
        ])
        return "\n".join(lines)

    @staticmethod
    def generate_gate_result_report(result: ReleaseGateResult) -> str:
        status = "PASS" if result.passed else "BLOCKED"
        lines = [
            "# AEOS Release Gate Result",
            "",
            f"- **Status**: {status}",
            f"- **Candidate**: {result.candidate.candidate_id}",
            f"- **Version**: {result.candidate.version}",
            "",
        ]
        if result.errors:
            lines.extend(["## Errors", ""])
            for e in result.errors:
                lines.append(f"- {e}")
        return "\n".join(lines)
