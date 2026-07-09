from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

from aeos.core.judge.judge_models import JudgeResult, JudgeScorecard


class JudgeReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, result: JudgeResult, scorecard: JudgeScorecard) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / result.execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "judge-report.md"

        lines = [
            f"# AEOS Judge Report",
            f"",
            f"- **Execution ID:** {result.execution_id}",
            f"- **Status:** {result.status}",
            f"- **Score:** {result.score:.4f}",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Blocking Rules ({len(result.blocking_rules)})",
            f"",
        ]
        if result.blocking_rules:
            for rule in result.blocking_rules:
                lines.append(f"- :no_entry: `{rule}`")
        else:
            lines.append(f"- None")
        lines.append("")

        lines.extend([
            f"## Scorecard Categories",
            f"",
        ])
        for cat, score in sorted(scorecard.categories.items()):
            icon = ":green_circle:" if score >= 0.95 else ":yellow_circle:" if score >= 0.80 else ":red_circle:"
            lines.append(f"- {icon} **{cat}**: {score:.4f}")
        lines.append(f"")
        lines.append(f"## Findings ({len(result.facts_validated)} validated, {len(result.claims_rejected)} rejected)")
        lines.append(f"")
        lines.append(f"- Facts validated: {len(result.facts_validated)}")
        lines.append(f"- Claims rejected: {len(result.claims_rejected)}")
        lines.append(f"- Missing evidence: {len(result.missing_evidence)}")
        lines.append(f"")
        lines.append(f"## Security Findings ({len(result.security_findings)})")
        lines.append(f"")
        if result.security_findings:
            for sf in result.security_findings:
                lines.append(f"- :warning: {sf}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Policy Findings ({len(result.policy_findings)})",
            f"",
        ])
        if result.policy_findings:
            for pf in result.policy_findings:
                lines.append(f"- {pf}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Permission Findings ({len(result.permission_findings)})",
            f"",
        ])
        if result.permission_findings:
            for pf in result.permission_findings:
                lines.append(f"- {pf}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Warnings ({len(result.warnings)})",
            f"",
        ])
        if result.warnings:
            for w in result.warnings:
                lines.append(f"- {w}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Recommendations",
            f"",
        ])
        if result.recommendations:
            for r in result.recommendations:
                lines.append(f"- {r}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Evidence References ({len(result.evidence_refs)})",
            f"",
        ])
        for ref in result.evidence_refs:
            lines.append(f"- `{ref}`")
        lines.append("")
        lines.append(f"---")
        lines.append(f"## Final Verdict: **{result.status}**")

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)

    def generate_summary(self, result: JudgeResult) -> dict:
        return {
            "execution_id": result.execution_id,
            "status": result.status,
            "score": result.score,
            "blocking_rules_count": len(result.blocking_rules),
            "critical_blockers": [r for r in result.blocking_rules if r in (
                "missing_evidence_manifest", "manifest_hash_mismatch",
                "permission_denied", "policy_denied", "governance_blocked",
                "tool_router_bypass", "secret_exposed",
            )],
            "findings_summary": {
                "facts_validated": len(result.facts_validated),
                "claims_rejected": len(result.claims_rejected),
                "missing_evidence": len(result.missing_evidence),
                "security_findings": len(result.security_findings),
                "policy_findings": len(result.policy_findings),
                "permission_findings": len(result.permission_findings),
            },
        }
