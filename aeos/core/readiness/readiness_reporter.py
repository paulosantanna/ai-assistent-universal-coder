from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from aeos.core.readiness.readiness_models import ReadinessResult, ReadinessScorecard


class ReadinessReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, result: ReadinessResult, scorecard: ReadinessScorecard) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / result.execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "production-readiness-report.md"

        lines = [
            f"# AEOS Production Readiness Report",
            f"",
            f"- **Execution ID:** {result.execution_id}",
            f"- **Status:** {result.status}",
            f"- **Overall Score:** {result.overall_score:.4f}",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Category Scores",
            f"",
        ]

        for cat, score in sorted(result.categories.items()):
            icon = ":green_circle:" if score >= 0.95 else ":yellow_circle:" if score >= 0.80 else ":red_circle:"
            lines.append(f"- {icon} **{cat}**: {score:.4f}")

        lines.extend([
            f"",
            f"## Critical Blockers ({len(result.critical_blockers)})",
            f"",
        ])
        if result.critical_blockers:
            for cb in result.critical_blockers:
                lines.append(f"- :no_entry: {cb}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## High Risks ({len(result.high_risks)})",
            f"",
        ])
        if result.high_risks:
            for hr in result.high_risks:
                lines.append(f"- :warning: {hr}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Medium Risks ({len(result.medium_risks)})",
            f"",
        ])
        if result.medium_risks:
            for mr in result.medium_risks:
                lines.append(f"- {mr}")
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

        lines.append(f"## Final Verdict: **{result.status}**")
        lines.append(f"")
        lines.append(f"> **Note:** A READINESS_PASS requires all of the following:")
        lines.append(f"> - Judge PASS (no BLOCKED status)")
        lines.append(f"> - Runtime PASS (no BLOCKED status)")
        lines.append(f"> - Eval overall_score >= 0.95")
        lines.append(f"> - Zero critical blockers")
        lines.append(f"> - Evidence manifest present")
        lines.append(f"> - All three required reports exist (judge, eval, readiness)")

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)
