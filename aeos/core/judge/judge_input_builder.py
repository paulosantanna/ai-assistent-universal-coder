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
        data["permission_decisions"] = self._load_first_jsonl(
            evidence_dir,
            "permission_decisions.jsonl",
            "permission-decisions.jsonl",
            "permission_decisions.jsonl",
        )
        data["policy_decisions"] = self._load_first_jsonl(evidence_dir, "policy_decisions.jsonl")
        data["governance_decisions"] = self._load_first_jsonl(evidence_dir, "governance_decisions.jsonl")
        data["tool_results"] = self._load_first_jsonl(evidence_dir, "tool_result.jsonl", "tool_results.jsonl")
        data["skill_results"] = self._load_first_jsonl(evidence_dir, "skill-result.jsonl", "skill_results.jsonl")
        data["playbook_results"] = self._load_first_jsonl(evidence_dir, "playbook-result.jsonl", "playbook_results.jsonl")
        data["agent_results"] = self._load_first_jsonl(evidence_dir, "agent-result.jsonl", "agent_results.jsonl")
        data["runtime_results"] = self._load_first_jsonl(
            evidence_dir,
            "runtime-result.jsonl",
            "runtime_results.jsonl",
            "runtime_result.jsonl",
        )
        data["claims"] = self._load_jsonl(evidence_dir / "claims.jsonl")
        data["approval_refs"] = self._load_jsonl(evidence_dir / "approvals.jsonl")
        data["package_refs"] = self._load_jsonl(evidence_dir / "packages.jsonl")

        return JudgeInput(**data)

    def build_from_dict(self, data: dict[str, Any]) -> JudgeInput:
        return JudgeInput(**data)

    def _load_first_jsonl(self, directory: Path, *filenames: str) -> list[dict[str, Any]]:
        for filename in filenames:
            records = self._load_jsonl(directory / filename)
            if records:
                return records
        return []

    def _load_jsonl(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(self._normalize_jsonl_record(json.loads(line)))
        except (json.JSONDecodeError, IOError):
            pass
        return records

    def _normalize_jsonl_record(self, record: dict[str, Any]) -> dict[str, Any]:
        content = record.get("content")
        if not isinstance(content, dict):
            return record
        normalized = dict(content)
        for key in ("record_id", "record_type", "timestamp", "sha256"):
            if key in record and key not in normalized:
                normalized[key] = record[key]
        return normalized

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
