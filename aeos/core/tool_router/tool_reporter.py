from __future__ import annotations

from pathlib import Path
from typing import Any

from aeos.core.tool_router.tool_models import ToolDecision, ToolResult


class ToolRouterReporter:
    def __init__(self, output_dir: str = ".aeos/reports"):
        self.output_dir = Path(output_dir)

    def generate_report(
        self,
        execution_id: str,
        decisions: list[ToolDecision],
        results: list[ToolResult],
        config_info: dict[str, Any] | None = None,
    ) -> str:
        out_dir = self.output_dir / execution_id
        out_dir.mkdir(parents=True, exist_ok=True)

        total = len(decisions)
        passed = sum(1 for d in decisions if d.status == "PASS")
        blocked = sum(1 for d in decisions if d.status == "BLOCKED")
        errors = sum(1 for d in decisions if d.status == "ERROR")
        waiting = sum(1 for d in decisions if d.status == "WAITING_APPROVAL")

        lines = [
            "# Tool Router Report",
            f"",
            f"- **Execution ID**: {execution_id}",
            f"- **Total Requests**: {total}",
            f"- **PASS**: {passed}",
            f"- **BLOCKED**: {blocked}",
            f"- **ERROR**: {errors}",
            f"- **WAITING_APPROVAL**: {waiting}",
            f"",
        ]

        if config_info:
            lines.extend([
                "## Configuration",
                f"",
                f"- **Tool Router**: {'enabled' if config_info.get('tool_router_enabled', False) else 'disabled'}",
                f"- **MCP Runtime**: {'enabled' if config_info.get('mcp_runtime_enabled', False) else 'disabled'}",
                f"- **Fail Closed**: {config_info.get('fail_closed', True)}",
                f"- **MCPs Registered**: {config_info.get('mcps_count', 0)}",
                f"- **Config Files Loaded**: {config_info.get('loaded_files', [])}",
                f"- **Findings**: {config_info.get('findings_count', 0)}",
                f"",
            ])

        lines.extend([
            "## Decisions",
            f"",
            "| tool_id | action | status | reason |",
            "|---------|--------|--------|--------|",
        ])
        for d in decisions:
            lines.append(f"| {d.tool_id} | {d.action} | {d.status} | {d.reason} |")

        lines.extend([
            f"",
            "## Results",
            f"",
            "| tool_id | action | status | duration_ms | error |",
            "|---------|--------|--------|-------------|-------|",
        ])
        for r in results:
            lines.append(f"| {r.tool_id} | {r.action} | {r.status} | {r.duration_ms} | {r.error or ''} |")

        report = "\n".join(lines)
        fp = out_dir / "tool-router-report.md"
        with open(fp, "w", encoding="utf-8") as f:
            f.write(report)

        return str(fp)
