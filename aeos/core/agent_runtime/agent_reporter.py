from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from aeos.core.agent_runtime.agent_models import AgentTask, AgentResult


class AgentReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, execution_id: str, task: AgentTask, result: AgentResult) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "agent-runtime-report.md"

        lines = [
            f"# Agent Runtime Report — {task.agent_id}",
            f"",
            f"- **Execution ID:** {execution_id}",
            f"- **Task ID:** {task.task_id}",
            f"- **Agent ID:** {task.agent_id}",
            f"- **Actor:** {task.actor}",
            f"- **Role:** {task.role}",
            f"- **Objective:** {task.objective}",
            f"- **Status:** {result.status}",
            f"- **Duration:** {result.duration_ms}ms",
            f"- **Generated at:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Execution Summary",
            f"",
            f"- Messages sent: {len(result.messages)}",
            f"- Delegations: {len(result.delegations)}",
            f"- Skills executed: {len(result.skill_results)}",
            f"- Playbooks executed: {len(result.playbook_results)}",
            f"- Tool calls: {len(result.tool_results)}",
            f"- Evidence refs: {len(result.evidence_refs)}",
            f"",
            f"## Messages",
            f"",
        ]

        for msg in result.messages:
            lines.append(f"- [{msg.get('message_type', '?')}] {msg.get('from_agent', '?')} → {msg.get('to_agent', '?')}")

        lines.extend([
            f"",
            f"## Delegations",
            f"",
        ])
        for d in result.delegations:
            lines.append(f"- {d.get('parent_agent', '?')} → {d.get('child_agent', '?')} ({d.get('objective', '')})")

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
            f"## Blocking Conditions",
            f"",
        ])
        for bc in result.blocking_conditions:
            lines.append(f"- {bc}")

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)
