"""Report Generator — execution-summary, judge-report, artifacts-index."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ReportGenerator:
    def __init__(self, reports_dir: Path, execution_id: str):
        self.reports_dir = reports_dir / execution_id
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_execution_summary(self, context: dict) -> Path:
        content = f"""# Execution Summary

**Execution ID:** {context.get('execution_id', 'unknown')}
**Playbook:** {context.get('playbook_id', 'unknown')}
**Target:** {context.get('target_path', 'unknown')}
**Mode:** {context.get('mode', 'sandbox')}
**Timestamp:** {datetime.now(timezone.utc).isoformat()}
**Status:** {context.get('final_state', 'unknown')}

## State Machine History

| Step | State | Detail |
|------|-------|--------|
"""
        history = context.get("state_history", [])
        for entry in history:
            content += f"| {entry.get('timestamp', '?')} | {entry.get('state', '?')} | {entry.get('detail', '')} |\n"

        content += f"""
## Steps Executed

{context.get('step_summary', 'No steps executed')}

## Approved Permissions

| Action | Actor | Decision |
|--------|-------|----------|
"""
        perm_log = context.get("permission_log", [])
        for entry in perm_log:
            content += f"| {entry.get('action', '?')} | {entry.get('actor', '?')} | {entry.get('decision', '?')} |\n"

        content += f"""
## Generated Artifacts

{chr(10).join(f'- {a}' for a in context.get('generated_artifacts', []))}

## Risks Identified

{chr(10).join(f'- {r}' for r in context.get('risks', []))}
"""
        path = self.reports_dir / "execution-summary.md"
        path.write_text(content, encoding="utf-8")
        return path

    def generate_judge_report(self, judge_result: dict) -> Path:
        checks = judge_result.get("checks", {})
        content = f"""# Judge Report v2

**Judge ID:** {judge_result.get('judge_id', 'judge-v2-aeos-001')}
**Execution ID:** {judge_result.get('execution_id', 'unknown')}
**Timestamp:** {judge_result.get('timestamp', datetime.now(timezone.utc).isoformat())}
**Decision:** **{judge_result.get('decision', 'UNKNOWN')}**
**Final Score:** {judge_result.get('final_score', 0.0)}/10

## Blocking Reasons

{chr(10).join(f'- {r}' for r in judge_result.get('blocking_reasons', ['None'])) or 'None'}

## Warnings

{chr(10).join(f'- {w}' for w in judge_result.get('warnings', ['None'])) or 'None'}

## Validation Checks

| Check | Passed | Detail |
|-------|--------|--------|
"""
        for check_name, check_data in checks.items():
            content += f"| {check_name} | {'PASS' if check_data.get('passed') else 'FAIL'} | {check_data.get('detail', '')} |\n"

        content += f"""
## Deductions

- Blocking deductions: {judge_result.get('deductions', {}).get('blocking_deductions', 0)}
- Warning deductions: {judge_result.get('deductions', {}).get('warning_deductions', 0)}
- Total deductions: {judge_result.get('deductions', {}).get('total_deductions', 0)}

## Verdict

**{judge_result.get('decision', 'UNKNOWN')}** — {'Execution passed all checks.' if judge_result.get('decision') == 'PASS' else 'Execution blocked. Review blocking reasons above.'}
"""
        path = self.reports_dir / "judge-report.md"
        path.write_text(content, encoding="utf-8")
        return path

    def generate_artifacts_index(self, artifacts: list[dict]) -> Path:
        content = f"""# Generated Artifacts Index

**Generated At:** {datetime.now(timezone.utc).isoformat()}
**Total Artifacts:** {len(artifacts)}

| # | Artifact | Path | Type | Size (bytes) |
|---|----------|------|------|-------------|
"""
        for i, art in enumerate(artifacts, 1):
            content += f"| {i} | {art.get('name', '?')} | {art.get('path', '?')} | {art.get('type', '?')} | {art.get('size', 0)} |\n"

        content += """
## Evidence Index

"""
        evidence_list = [a for a in artifacts if a.get("type") == "evidence"]
        for ev in evidence_list:
            content += f"- {ev.get('name', '?')}: {ev.get('path', '?')}\n"
        path = self.reports_dir / "generated-artifacts-index.md"
        path.write_text(content, encoding="utf-8")
        return path