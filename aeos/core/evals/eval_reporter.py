from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from aeos.core.evals.eval_models import EvalResult, EvalScorecard


class EvalReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, results: list[EvalResult], scorecard: EvalScorecard) -> str:
        execution_id = scorecard.execution_id
        report_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "evaluation-harness-report.md"

        lines = [
            f"# AEOS Evaluation Harness Report",
            f"",
            f"- **Execution ID:** {execution_id}",
            f"- **Status:** {scorecard.status}",
            f"- **Overall Score:** {scorecard.overall_score:.4f}",
            f"- **Total Cases:** {scorecard.total_cases}",
            f"- **Passed:** {scorecard.passed}",
            f"- **Failed:** {scorecard.failed}",
            f"- **Errors:** {scorecard.errors}",
            f"- **Skipped:** {scorecard.skipped}",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Suite Summary",
            f"",
        ]

        for suite_id, sdata in sorted(scorecard.suites.items()):
            icon = ":green_circle:" if sdata["score"] >= 1.0 else ":yellow_circle:" if sdata["score"] >= 0.8 else ":red_circle:"
            lines.append(f"- {icon} **{suite_id}**: {sdata['passed']}/{sdata['total']} passed (score: {sdata['score']:.4f})")

        lines.extend([
            f"",
            f"## Blocking Failures",
            f"",
        ])
        if scorecard.blocking_failures:
            for bf in scorecard.blocking_failures:
                lines.append(f"- :no_entry: {bf}")
        else:
            lines.append("- None")
        lines.append("")

        lines.extend([
            f"## Detailed Results",
            f"",
        ])
        for r in results:
            icon = ":white_check_mark:" if r.status == "PASS" else ":x:" if r.status == "FAIL" else ":warning:"
            lines.append(f"- {icon} **{r.suite_id}/{r.case_id}**: {r.status} - {r.actual[:100]}")
        lines.append("")

        lines.append(f"## Final Status: **{scorecard.status}**")

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)
