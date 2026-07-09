"""Patch Proposal Engine — generates patch proposals without applying changes."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class PatchProposalEngine:
    def __init__(self, workspace_root: Path, execution_id: Optional[str] = None):
        self.workspace_root = workspace_root.resolve()
        self.execution_id = execution_id or f"pt-{uuid.uuid4().hex[:12]}"
        self.patches_dir = self.workspace_root / ".aeos" / "patches" / self.execution_id
        self.fact_count = 0
        self.assumption_count = 0
        self.risk_count = 0
        self.recommendation_count = 0

    def generate_patch(self, target_path: Path, issue: str, file_changes: list[dict], rollback_chain: dict, risk_analysis: dict) -> dict:
        self.patches_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()
        affected_files = [f.get("file", "") for f in file_changes]
        diff_lines = self._generate_diff(file_changes)
        summary = self._build_summary(target_path, issue, file_changes)
        rollback_content = self._build_rollback(rollback_chain, target_path, file_changes)
        risk_content = self._build_risk(risk_analysis, target_path)

        self._write_text("proposed.patch", diff_lines)
        self._write_json("affected-files.json", {
            "execution_id": self.execution_id, "timestamp": timestamp,
            "target": str(target_path), "affected_files": affected_files,
            "total_files": len(affected_files)
        })
        self._write_md("patch-summary.md", summary)
        self._write_md("rollback-plan.md", risk_content + "\n\n" + rollback_content)
        self._write_md("risk-analysis.md", risk_content)

        return {
            "execution_id": self.execution_id,
            "patches_dir": str(self.patches_dir),
            "affected_files": affected_files,
            "patch_path": str(self.patches_dir / "proposed.patch"),
            "rollback_path": str(self.patches_dir / "rollback-plan.md"),
            "summary_path": str(self.patches_dir / "patch-summary.md"),
            "risk_path": str(self.patches_dir / "risk-analysis.md"),
            "status": "patch_proposed",
            "artifacts_generated": [
                str(self.patches_dir / "proposed.patch"),
                str(self.patches_dir / "affected-files.json"),
                str(self.patches_dir / "patch-summary.md"),
                str(self.patches_dir / "rollback-plan.md"),
                str(self.patches_dir / "risk-analysis.md"),
            ],
        }

    def _generate_diff(self, file_changes: list[dict]) -> str:
        lines = []
        for fc in file_changes:
            f = fc.get("file", "unknown")
            lines.append(f"--- a/{f}")
            lines.append(f"+++ b/{f}")
            for change in fc.get("changes", []):
                ctype = change.get("type", "modify")
                if ctype == "hunk":
                    lines.append(f"@@ -{change.get('start_old', 0)},{change.get('count_old', 0)} +{change.get('start_new', 0)},{change.get('count_new', 0)} @@")
                    for line in change.get("lines", []):
                        lines.append(line)
                elif ctype == "add":
                    content = change.get("content", "")
                    for line in content.split("\n"):
                        lines.append(f"+{line}")
                elif ctype == "delete":
                    content = change.get("content", "")
                    for line in content.split("\n"):
                        lines.append(f"-{line}")
                else:
                    content = change.get("content", "")
                    for line in content.split("\n"):
                        lines.append(f" {line}")
            lines.append("")
        return "\n".join(lines)

    def _build_summary(self, target_path: Path, issue: str, file_changes: list[dict]) -> str:
        sections = [
            f"# Patch Summary — {self.execution_id}",
            f"",
            f"**Target:** {target_path}",
            f"**Issue:** {issue}",
            f"**Generated At:** {datetime.now(timezone.utc).isoformat()}",
            f"**Status: PROPOSAL ONLY — NOT APPLIED**",
            f"",
            f"## Affected Files",
            f"",
            f"| # | File | Changes | Type |",
            f"|---|------|---------|------|",
        ]
        fact_count = 0
        for i, fc in enumerate(file_changes, 1):
            f = fc.get("file", "unknown")
            changes = fc.get("changes", [])
            sections.append(f"| {i} | `{f}` | {len(changes)} change(s) | {fc.get('type', 'modify')} |")
            fact_count += 1

        sections += ["", "## Facts", ""]
        for fc in file_changes:
            f = fc.get("file", "unknown")
            sections.append(f"- `{f}` will be read as source evidence")
            fact_count += 1

        sections += ["", "## Assumptions", "",
            f"- Issue description accurately reflects the desired change",
            f"- All relevant files were identified by the analysis",
            f"- No conflicting changes exist in other parts of the codebase",
        ]

        sections += ["", "## Risks", ""]
        risk_count = 0
        for fc in file_changes:
            for c in fc.get("changes", []):
                if c.get("type") == "delete":
                    sections.append(f"- Deleting code in `{fc.get('file', '?')}` may remove functionality")
                    risk_count += 1
        sections.append(f"- Patch has NOT been applied — requires explicit approval")
        risk_count += 1

        sections += ["", "## Recommendations", "",
            f"- Review proposed.patch before approving",
            f"- Run suggested tests in sandbox before applying",
            f"- Verify rollback plan covers all edge cases",
        ]

        sections += ["", "## Evidence Manifest", "",
            f"- `proposed.patch` — SHA-256 will be computed on generation",
            f"- `affected-files.json` — lists all files involved",
            f"- `patch-summary.md` — this file",
            f"- `rollback-plan.md` — undo strategy",
            f"- `risk-analysis.md` — risk assessment",
            "",
            f"---",
            f"*This is a PROPOSAL. No files outside .aeos/patches/ were modified.*",
        ]

    def _build_rollback(self, rollback_chain: dict, target_path: Path, file_changes: list[dict]) -> str:
        sections = [
            f"# Rollback Plan — {self.execution_id}",
            f"",
            f"**Strategy:** restore_originals + delete_generated_artifacts",
            f"**Scope:** This plan covers undoing ALL proposed changes in this execution.",
            f"",
            f"## Rollback Operations",
            f"",
            f"| # | Operation | Target | Action |",
            f"|---|-----------|--------|--------|",
        ]
        for i, fc in enumerate(file_changes, 1):
            f = fc.get("file", "unknown")
            sections.append(f"| {i} | Restore original | `{f}` | `git checkout -- {f}` |")
        sections += [
            f"| {len(file_changes) + 1} | Delete patch artifacts | `.aeos/patches/{self.execution_id}` | `rm -rf .aeos/patches/{self.execution_id}` |",
            f"| {len(file_changes) + 2} | Delete sandbox tests | `.aeos/sandbox/{self.execution_id}` | `rm -rf .aeos/sandbox/{self.execution_id}` |",
            "",
            f"## Rollback Verification",
            f"",
            f"- Verify `git diff --stat` shows zero changes after rollback",
            f"- Verify all tests pass after rollback",
            f"- Verify no artifacts remain in `.aeos/patches/{self.execution_id}/`",
            "",
            f"## Rollback Conditions",
            f"",
            f"- Apply if: patch introduces regression",
            f"- Apply if: tests fail after patch application",
            f"- Apply if: approval is revoked",
            f"- Apply if: manual review identifies issues",
        ]

        sections = ["# Rollback Plan — " + self.execution_id, ""]
        sections.append("**Strategy:** restore_originals + delete_generated_artifacts")
        sections.append(f"**Scope:** Rollback for execution {self.execution_id}")
        sections.append("")
        sections.append("## Rollback Operations")
        sections.append("")
        sections.append("| # | Operation | Target | Action |")
        sections.append("|---|-----------|--------|--------|")
        for i, fc in enumerate(file_changes, 1):
            f = fc.get("file", "unknown")
            sections.append(f"| {i} | Restore original | `{f}` | `git checkout -- {f}` |")
        sections.append(f"| {len(file_changes) + 1} | Delete patch artifacts | `.aeos/patches/{self.execution_id}` | `rm -rf .aeos/patches/{self.execution_id}` |")
        if file_changes:
            sections.append(f"| {len(file_changes) + 2} | Delete sandbox tests | `.aeos/sandbox/{self.execution_id}` | `rm -rf .aeos/sandbox/{self.execution_id}` |")
        sections += ["", "## Rollback Verification", "",
            "- Verify `git diff --stat` shows zero changes after rollback",
            "- Verify all tests pass after rollback",
            "- Verify no artifacts remain in `.aeos/patches/` or `.aeos/sandbox/` directories",
        ]
        return "\n".join(sections)

    def _build_risk(self, risk_analysis: dict, target_path: Path) -> str:
        sections = [
            f"# Risk Analysis — {self.execution_id}",
            f"",
            f"**Target:** {target_path}",
            f"**Generated At:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Risk Classification",
            f"",
            f"| Risk | Level | Mitigation |",
            f"|------|-------|------------|",
        ]
        for r in risk_analysis.get("risks", []):
            sections.append(f"| {r.get('risk', 'unknown')} | {r.get('level', 'low')} | {r.get('mitigation', 'none')} |")
        sections += [
            "", "## Blocking Conditions", "",
            "- [ ] Patch has rollback plan",
            "- [ ] Patch was NOT applied automatically",
            "- [ ] Proposal has dry-run artifacts",
            "- [ ] Required approvals are present",
            "- [ ] Approvals are within scope",
            "- [ ] All artifacts have SHA-256",
            "- [ ] Evidence manifest is valid",
            "- [ ] Hash chain is valid",
            "- [ ] No secrets appear in outputs",
            "- [ ] No files outside .aeos were modified",
        ]
        return "\n".join(sections)

    def _write_text(self, name: str, content: str) -> Path:
        path = self.patches_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _write_json(self, name: str, data: dict) -> Path:
        return self._write_text(name, json.dumps(data, indent=2, ensure_ascii=False))

    def _write_md(self, name: str, content: str) -> Path:
        return self._write_text(name, content)