from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.judge.judge_models import JudgeInput


class JudgeInputBuilder:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def build(self, execution_id: str, target_path: str = ".") -> JudgeInput:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / execution_id
        reports_dir = self.workspace_root / ".aeos" / "reports" / execution_id

        manifest_path = evidence_dir / "runtime-evidence-manifest.json"
        if not manifest_path.exists():
            manifest_path = evidence_dir / "evidence-manifest.json"

        data: dict[str, Any] = {
            "execution_id": execution_id,
            "target_path": target_path,
        }

        if manifest_path.exists():
            data["evidence_manifest_path"] = str(manifest_path)

        data["reports"] = self._load_reports(reports_dir)
        data["permission_decisions"] = self._load_jsonl(evidence_dir / "permission_decisions.jsonl")
        data["policy_decisions"] = self._load_jsonl(evidence_dir / "policy_decisions.jsonl")
        data["governance_decisions"] = self._load_jsonl(evidence_dir / "governance_decisions.jsonl")
        data["tool_results"] = self._load_jsonl(evidence_dir / "tool_results.jsonl")
        data["skill_results"] = self._load_jsonl(evidence_dir / "skill_results.jsonl")
        data["playbook_results"] = self._load_jsonl(evidence_dir / "playbook_results.jsonl")
        data["agent_results"] = self._load_jsonl(evidence_dir / "agent_results.jsonl")
        data["runtime_results"] = self._load_jsonl(evidence_dir / "runtime_results.jsonl")
        data["claims"] = self._load_jsonl(evidence_dir / "claims.jsonl")
        data["approval_refs"] = self._load_jsonl(evidence_dir / "approvals.jsonl")
        data["package_refs"] = self._load_jsonl(evidence_dir / "packages.jsonl")

        return JudgeInput(**data)

    def build_from_dict(self, data: dict[str, Any]) -> JudgeInput:
        return JudgeInput(**data)

    def _load_jsonl(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        except (json.JSONDecodeError, IOError):
            pass
        return records

    def _load_reports(self, reports_dir: Path) -> list[dict[str, Any]]:
        if not reports_dir.exists():
            return []
        reports: list[dict[str, Any]] = []
        try:
            for fp in sorted(reports_dir.glob("*.md")):
                with open(fp, "r", encoding="utf-8") as f:
                    reports.append({
                        "path": str(fp),
                        "content": f.read(),
                        "size": fp.stat().st_size,
                    })
        except IOError:
            pass
        return reports
