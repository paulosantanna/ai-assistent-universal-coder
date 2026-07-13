"""DryRunPlanner — generates full dry-run artifacts without side effects."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


ACTIONS = ["read", "analyze", "generate_report", "propose_patch", "generate_test", "analyze_dependency", "propose_refactor"]
PERMISSION_TYPES = ["filesystem.read", "filesystem.write_sandbox", "filesystem.write_aeos", "git.read", "shell.readonly"]
RISK_LEVELS = ["low", "medium", "high", "critical"]


class DryRunPlanner:
    def __init__(self, workspace_root: Path, execution_id: Optional[str] = None):
        self.workspace_root = workspace_root.resolve()
        self.execution_id = execution_id or f"dr-{uuid.uuid4().hex[:12]}"
        self.dry_run_dir = self.workspace_root / ".aeos" / "dry-runs" / self.execution_id

    def plan_dry_run(self, target_path: Path, issue: Optional[str] = None, scope: Optional[str] = None) -> dict:
        self.dry_run_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()

        file_candidates = self._map_target_files(target_path)
        actions = self._determine_actions(target_path, issue, scope)
        required_approvals = self._determine_approvals(actions)
        risks = self._assess_risks(actions, file_candidates, scope)
        expected_outputs = self._determine_expected_outputs(actions)

        planned_actions = {
            "execution_id": self.execution_id,
            "timestamp": timestamp,
            "target": str(target_path),
            "issue": issue,
            "scope": scope,
            "actions": [
                {
                    "action_id": f"act-{i}",
                    "action": a,
                    "description": self._action_description(a, target_path, scope),
                    "evidence_produced": self._action_evidence(a),
                }
                for i, a in enumerate(actions)
            ],
            "summary": {
                "total_actions": len(actions),
                "read_actions": sum(1 for a in actions if a.startswith("read")),
                "generate_actions": sum(1 for a in actions if a.startswith("generate") or a.startswith("propose")),
            },
        }

        planned_file_changes = {
            "execution_id": self.execution_id,
            "timestamp": timestamp,
            "files_to_read": [str(f) for f in file_candidates if f.is_file()],
            "files_to_analyze": [str(f) for f in file_candidates if f.suffix in (".py", ".ts", ".js", ".java", ".yaml", ".json", ".md")],
            "files_to_generate": self._generate_paths(actions),
            "files_to_propose_change": self._propose_paths(actions, target_path),
            "summary": {
                "total_files_to_read": len(file_candidates),
                "total_files_to_analyze": len([f for f in file_candidates if f.suffix in (".py", ".ts", ".js", ".java", ".yaml", ".json", ".md")]),
                "total_files_to_generate": 0,
                "total_proposed_changes": 0,
            },
        }

        required_approvals_doc = {
            "execution_id": self.execution_id,
            "timestamp": timestamp,
            "required_approvals": required_approvals,
            "summary": {
                "total_required": len(required_approvals),
                "approval_types": list(set(a["action"] for a in required_approvals)),
            },
        }

        risk_preview = self._generate_risk_preview(actions, risks, scope)
        expected_outputs_doc = self._generate_expected_outputs(expected_outputs)

        self._write_json("planned-actions.json", planned_actions)
        self._write_json("planned-file-changes.json", planned_file_changes)
        self._write_json("required-approvals.json", required_approvals_doc)
        self._write_md("risk-preview.md", risk_preview)
        self._write_md("expected-outputs.md", expected_outputs_doc)

        return {
            "execution_id": self.execution_id,
            "dry_run_dir": str(self.dry_run_dir),
            "planned_actions": planned_actions,
            "planned_file_changes": planned_file_changes,
            "required_approvals": required_approvals_doc,
            "risks": risks,
            "status": "dry_run_complete",
            "artifacts_generated": [
                str(self.dry_run_dir / "planned-actions.json"),
                str(self.dry_run_dir / "planned-file-changes.json"),
                str(self.dry_run_dir / "required-approvals.json"),
                str(self.dry_run_dir / "risk-preview.md"),
                str(self.dry_run_dir / "expected-outputs.md"),
            ],
        }

    def _map_target_files(self, target_path: Path) -> list[Path]:
        files = []
        target = target_path.resolve()
        if target.is_file():
            return [target]
        if target.is_dir():
            for ext in ["*.py", "*.ts", "*.js", "*.java", "*.yaml", "*.json", "*.md", "*.toml", "*.xml"]:
                files.extend(target.rglob(ext))
            files = [f for f in files if ".aeos" not in str(f) and "node_modules" not in str(f)]
        return sorted(set(files))

    def _determine_actions(self, target_path: Path, issue: Optional[str], scope: Optional[str]) -> list[str]:
        actions = ["read_target_files"]
        if issue:
            actions += ["analyze_issue", "map_relevant_files", "classify_risk", "propose_strategy", "propose_patch", "generate_suggested_tests", "generate_rollback_plan"]
        if scope:
            actions += ["analyze_scope", "map_affected_files", "assess_architectural_impact", "propose_refactoring"]
        actions += ["run_judge", "block_if_missing_evidence"]
        return actions

    def _determine_approvals(self, actions: list[str]) -> list[dict]:
        approvals = []
        for a in actions:
            if a == "propose_patch":
                approvals.append({"action": "patch.propose", "scope": ".aeos/patches/**", "reason": "Patch proposal generation requires scope approval", "risk_level": "medium"})
            if "propose_refactoring" in a:
                approvals.append({"action": "refactoring.propose", "scope": ".aeos/patches/**", "reason": "Refactoring proposal requires architectural scope approval", "risk_level": "high"})
            if "generate_test" in a or "generate_suggested_tests" in a:
                approvals.append({"action": "sandbox.generate_test", "scope": ".aeos/sandbox/**", "reason": "Test generation in sandbox requires approval", "risk_level": "low"})
        approvals.append({"action": "read.files", "scope": "**/*.py,.ts,.js,.java", "reason": "Read-only access to source files", "risk_level": "low"})
        return approvals

    def _assess_risks(self, actions: list[str], files: list[Path], scope: Optional[str]) -> list[dict]:
        risks = []
        if any("propose_patch" in a for a in actions):
            risks.append({"risk": "unintended_code_change", "level": "medium", "mitigation": "Patch is proposal-only; requires approval before apply"})
        if scope and "refactor" in scope.lower():
            risks.append({"risk": "architectural_regression", "level": "high", "mitigation": "Refactoring must include rollback plan and evidence of current behavior"})
        if any(f.name == "package.json" or f.name == "pyproject.toml" or f.name == "requirements.txt" for f in files):
            risks.append({"risk": "dependency_change_implicit", "level": "medium", "mitigation": "Dependency analysis is read-only; no changes applied"})
        risks.append({"risk": "false_positive_analysis", "level": "low", "mitigation": "All outputs are proposals only; manual review required"})
        return risks

    def _determine_expected_outputs(self, actions: list[str]) -> list[dict]:
        outputs = []
        for a in actions:
            if a == "propose_patch":
                outputs.append({"type": "patch", "path": ".aeos/patches/{execution_id}/proposed.patch"})
                outputs.append({"type": "summary", "path": ".aeos/patches/{execution_id}/patch-summary.md"})
                outputs.append({"type": "rollback_plan", "path": ".aeos/patches/{execution_id}/rollback-plan.md"})
            if "generate_test" in a or "generate_suggested_tests" in a:
                outputs.append({"type": "generated_test", "path": ".aeos/sandbox/{execution_id}/generated-tests/"})
            if "generate_rollback_plan" in a:
                outputs.append({"type": "rollback_plan", "path": ".aeos/patches/{execution_id}/rollback-plan.md"})
            if "propose_refactoring" in a:
                outputs.append({"type": "refactoring_proposal", "path": ".aeos/patches/{execution_id}/refactoring-proposal.md"})
            if a == "generate_report" or a == "analyze_dependency":
                outputs.append({"type": "report", "path": ".aeos/reports/{execution_id}/"})
            outputs.append({"type": "judge_report", "path": ".aeos/reports/{execution_id}/judge-report.md"})
        return outputs

    def _action_description(self, action: str, target: Path, scope: Optional[str]) -> str:
        descs = {
            "read_file_files": f"Read source files from {target}",
            "analyze_issue": "Analyze the issue description and map to affected code areas",
            "map_relevant_files": "Identify relevant source files based on issue analysis",
            "classify_risk": "Classify the risk level of the proposed change",
            "propose_strategy": "Propose a change strategy with evidence",
            "propose_patch": "Generate a proposed patch without applying it",
            "generate_suggested_tests": "Generate suggested tests in sandbox directory",
            "generate_rollback_plan": "Generate a rollback plan for the proposed change",
            "analyze_scope": f"Analyze refactoring scope: {scope}",
            "map_affected_files": "Map all files affected by the refactoring",
            "assess_architectural_impact": "Assess architectural impact of the refactoring",
            "propose_refactoring": "Propose refactoring changes as patch only",
            "generate_judge": "Run Judge evaluation on all proposals and artifacts",
            "block_if_no_evidence": "Block if required evidence is missing or invalid",
        }
        return descs.get(action, f"Execute action: {action}")

    def _evidence_required(self, action: str) -> list[str]:
        evidence = {
            "propose_patch": ["SHA-256 of proposed.patch", "patch-summary.md", "rollback-plan.md", "risk-analysis.md"],
            "generate_suggested_tests": ["source files used as evidence", "test framework detected", "generated test files"],
            "propose_refactoring": ["motivation statement", "architecture evidence", "affected files list", "rollback plan"],
            "analyze_dependency": ["direct dependencies list", "transitive dependencies", "compatibility matrix"],
        }
        return evidence.get(action, ["action evidence"])

    def _generate_paths(self, actions: list[str]) -> list[str]:
        paths = []
        if "propose_patch" in actions:
            paths += [
                f".aeos/patches/{self.execution_id}/proposed.patch",
                f".aeos/patches/{self.execution_id}/affected-files.json",
                f".aeos/patches/{self.execution_id}/patch-summary.md",
                f".aeos/patches/{self.execution_id}/rollback-plan.md",
                f".aeos/patches/{self.execution_id}/risk-analysis.md",
            ]
        if "generate_suggested_tests" in actions:
            paths.append(f".aeos/sandbox/{self.execution_id}/generated-tests/")
        if "analyze_dependency" in actions:
            paths += [
                f".aeos/reports/{self.execution_id}/dependency-risk-report.md",
                f".aeos/reports/{self.execution_id}/upgrade-candidates.md",
                f".aeos/reports/{self.execution_id}/compatibility-matrix.md",
            ]
        return paths

    def _propose_paths(self, actions: list[str], target: Path) -> list[str]:
        return [str(target / "..")]

    def _generate_risk_preview(self, actions: list[str], risks: list[dict], scope: Optional[str]) -> str:
        lines = [
            f"# Risk Preview — {self.execution_id}",
            f"",
            f"**Generated At:** {datetime.now(timezone.utc).isoformat()}",
            f"**Scope:** {scope or 'not specified'}",
            f"",
            f"## Actions Planned",
            f"",
        ]
        for a in actions:
            lines.append(f"- {a}")
        lines += ["", "## Identified Risks", ""]
        for r in risks:
            lines.append(f"- **{r['risk']}** (level: {r['level']})")
            lines.append(f"  - Mitigation: {r['mitigation']}")
        lines += ["", "## Evidence to be Produced", ""]
        for a in actions:
            for ev in self._evidence_required(a):
                lines.append(f"- {ev}")
        lines += ["", "## Dry Run Status: NO CHANGES APPLIED", "This is a preview only. No files were read, written, or modified."]
        return "\n".join(lines)

    def _generate_expected_outputs(self, outputs: list[dict]) -> str:
        lines = [
            f"# Expected Outputs — {self.execution_id}",
            f"",
            f"**Generated At:** {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Output Artifacts",
            f"",
            f"| # | Type | Path |",
            f"|---|------|------|",
        ]
        for i, o in enumerate(outputs, 1):
            lines.append(f"| {i} | {o['type']} | `{o['path'].format(execution_id=self.execution_id)}` |")
        lines += [
            f"",
            f"## Integrity Requirements",
            f"",
            f"- All artifacts must have SHA-256 hashes",
            f"- All artifacts must be registered in evidence-manifest.json",
            f"- All artifacts must appear in hash-chain.jsonl",
            f"- Artifacts outside .aeos/ are prohibited",
            f"",
            f"## Non-Goals (not implemented in v0.3)",
            f"",
            f"- Real patch application",
            f"- Git commit, push, or merge",
            f"- Dependency updates",
            f"- Destructive shell commands",
            f"- Real secret access",
        ]
        return "\n".join(lines)

    def _write_json(self, name: str, data: dict) -> Path:
        path = self.dry_run_dir / name
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def _write_md(self, name: str, content: str) -> Path:
        path = self.dry_run_dir / name
        path.write_text(content, encoding="utf-8")
        return path