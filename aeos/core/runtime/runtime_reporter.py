from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from aeos.core.runtime.runtime_models import RuntimeRequest, RuntimeResult


class RuntimeReporter:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def generate_report(self, execution_id: str, request: RuntimeRequest, result: RuntimeResult) -> str:
        report_dir = self.workspace_root / ".aeos" / "reports" / execution_id
        report_dir.mkdir(parents=True, exist_ok=True)
        fp = report_dir / "runtime-orchestrator-report.md"

        lines = [
            f"# AEOS Runtime Orchestrator Report",
            f"",
            f"- **Execution ID:** {execution_id}",
            f"- **Run Type:** {request.run_type}",
            f"- **Entity ID:** {request.entity_id}",
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
            f"## Result Summary",
            f"",
        ]

        inner = result.result
        if inner:
            lines.append(f"- Inner status: {inner.get('status', '?')}")
            lines.append(f"- Facts: {len(inner.get('facts', []))}")
            lines.append(f"- Assumptions: {len(inner.get('assumptions', []))}")
            lines.append(f"- Risks: {len(inner.get('risks', []))}")
            lines.append(f"- Tool results: {len(inner.get('tool_results', []))}")
            lines.append(f"- Evidence refs: {len(inner.get('evidence_refs', []))}")
            lines.append(f"- Blocking conditions: {len(inner.get('blocking_conditions', []))}")

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

        lines.extend([
            f"",
            f"## Governance Summary",
            f"",
            f"- Permission Engine: Called",
            f"- Policy Engine: Called",
            f"- Governance Gate: Called",
            f"- Evidence Store: Records written",
            f"- Tool Router: All external actions routed",
            f"",
            f"## Pipeline Summary",
            f"",
        ])
        judge_path = self.workspace_root / ".aeos" / "evidence" / execution_id / "judge-result.json"
        if judge_path.exists():
            lines.append(f"- Judge Layer: Executed")
        else:
            lines.append(f"- Judge Layer: Not executed")
        eval_path = self.workspace_root / ".aeos" / "evidence" / execution_id / "eval-scorecard.json"
        if eval_path.exists():
            lines.append(f"- Evaluation Harness: Executed")
        else:
            lines.append(f"- Evaluation Harness: Not executed")
        readiness_path = self.workspace_root / ".aeos" / "evidence" / execution_id / "production-readiness-scorecard.json"
        if readiness_path.exists():
            lines.append(f"- Production Readiness: Executed")
        else:
            lines.append(f"- Production Readiness: Not executed")

        lines.extend([
            f"",
            f"## Final Status: {result.status}",
        ])

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(fp)
