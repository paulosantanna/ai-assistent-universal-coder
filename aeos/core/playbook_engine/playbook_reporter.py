from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from aeos.core.playbook_engine.playbook_models import PlaybookRequest, PlaybookResult


class PlaybookReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, execution_id: str, request: PlaybookRequest, result: PlaybookResult) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "playbook-engine-report.md"

        lines = [
            f"# Playbook Engine Report — {request.playbook_id}",
            f"",
            f"- **Execution ID:** {execution_id}",
            f"- **Playbook ID:** {request.playbook_id}",
            f"- **Actor:** {request.actor}",
            f"- **Role:** {request.role}",
            f"- **Status:** {result.status}",
            f"- **Duration:** {result.duration_ms}ms",
            f"- **Dry Run:** {request.dry_run}",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Execution Summary",
            f"",
            f"- Steps completed: {len(result.steps)}",
            f"- Skills executed: {len(result.skill_results)}",
            f"- Tool calls: {len(result.tool_results)}",
            f"- Evidence refs: {len(result.evidence_refs)}",
            f"",
            f"## Steps",
            f"",
        ]

        for step in result.steps:
            status_icon = "PASS" if step.get("status") == "PASS" else "FAIL"
            lines.append(f"- `{step.get('step_id', '?')}` [{status_icon}] {step.get('description', '')} ({step.get('duration_ms', 0)}ms)")
            if step.get("error"):
                lines.append(f"  - Error: {step['error']}")

        lines.extend([
            f"",
            f"## Facts",
            f"",
        ])
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
            f"## Skill Results",
            f"",
        ])
        for sr in result.skill_results:
            lines.append(f"- `{sr.get('skill_id', '?')}` → {sr.get('status', '?')} | {sr.get('error', 'ok')}")

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
