from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from aeos.core.skill_engine.skill_models import SkillRequest, SkillResult


class SkillReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, execution_id: str, request: SkillRequest, result: SkillResult) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "skill-engine-report.md"

        lines = [
            f"# Skill Engine Report — {request.skill_id}",
            f"",
            f"- **Execution ID:** {execution_id}",
            f"- **Skill ID:** {request.skill_id}",
            f"- **Actor:** {request.actor}",
            f"- **Role:** {request.role}",
            f"- **Status:** {result.status}",
            f"- **Duration:** {result.duration_ms}ms",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Input",
            f"",
            f"```json",
            f"{request.input}",
            f"```",
            f"",
            f"## Facts",
            f"",
        ]

        for f in result.facts:
            lines.append(f"- {f.get('claim', '')} (evidence: {f.get('evidence', '')})")

        lines.extend([
            f"",
            f"## Assumptions",
            f"",
        ])
        for a in result.assumptions:
            lines.append(f"- {a.get('assumption', '')} (evidence: {a.get('evidence_ref', '')})")

        lines.extend([
            f"",
            f"## Risks",
            f"",
        ])
        for r in result.risks:
            lines.append(f"- {r.get('risk', '')} (evidence: {r.get('evidence_ref', '')})")

        lines.extend([
            f"",
            f"## Recommendations",
            f"",
        ])
        for r in result.recommendations:
            lines.append(f"- {r.get('recommendation', '')}")

        lines.extend([
            f"",
            f"## Tool Results",
            f"",
        ])
        for tr in result.tool_results:
            lines.append(f"- `{tr.get('tool_id', '?')}` → {tr.get('status', '?')} | {tr.get('error', 'ok')}")

        lines.extend([
            f"",
            f"## Blocking Conditions",
            f"",
        ])
        for bc in result.blocking_conditions:
            lines.append(f"- {bc}")

        lines.extend([
            f"",
            f"## Evidence References",
            f"",
        ])
        for ref in result.evidence_refs:
            lines.append(f"- `{ref}`")

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)
