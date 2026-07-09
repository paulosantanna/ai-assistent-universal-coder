from __future__ import annotations

import json
from pathlib import Path

from aeos.core.governance.governance_models import GovernanceResult


class GovernanceReporter:
    def __init__(self, reports_dir: str = ".aeos/reports"):
        self.reports_dir = Path(reports_dir)

    def write_governance_report(self, execution_id: str, results: list[GovernanceResult]) -> str:
        base = self.reports_dir / execution_id
        base.mkdir(parents=True, exist_ok=True)
        fp = base / "governance-report.md"

        lines = []
        lines.append(f"# Governance Report — {execution_id}")
        lines.append("")
        lines.append(f"**Generated at:** {results[0].timestamp if results else 'N/A'}")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        passed = sum(1 for r in results if r.status == "PASS")
        blocked = sum(1 for r in results if r.status == "BLOCKED")
        waiting = sum(1 for r in results if r.status == "WAITING_APPROVAL")
        lines.append(f"- **PASS:** {passed}")
        lines.append(f"- **BLOCKED:** {blocked}")
        lines.append(f"- **WAITING_APPROVAL:** {waiting}")
        lines.append(f"- **Total decisions:** {len(results)}")
        lines.append("")

        for r in results:
            icon = {"PASS": "✓", "BLOCKED": "✗", "WAITING_APPROVAL": "⏳"}
            lines.append(f"### {icon.get(r.status, '?')} {r.action}")
            lines.append(f"- **Status:** {r.status}")
            lines.append(f"- **Permission:** {'✓' if r.permission_allowed else '✗'}")
            lines.append(f"- **Policy:** {'✓' if r.policy_allowed else '✗'}")
            lines.append(f"- **Requires Approval:** {r.requires_approval}")
            lines.append(f"- **Approval Present:** {r.approval_present}")
            if r.blocking_reasons:
                for br in r.blocking_reasons:
                    lines.append(f"- **Blocked:** {br}")
            lines.append("")

        content = "\n".join(lines)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return str(fp)
