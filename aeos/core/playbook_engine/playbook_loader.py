from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional

from aeos.core.playbook_engine.playbook_models import PlaybookContract, PlaybookStep
from aeos.core.playbook_engine.playbook_registry_resolver import PlaybookRegistryResolver


class PlaybookLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.resolver = PlaybookRegistryResolver(workspace_root)

    def _parse_playbook_markdown(self, path: Path) -> dict[str, Any]:
        if not path or not path.exists():
            return {}

        content = path.read_text(encoding="utf-8")
        sections = re.split(r"\n## ", content)
        result: dict[str, Any] = {}

        for section in sections:
            header_line = section.split("\n", 1)[0].strip()
            body = section.split("\n", 1)[1] if "\n" in section else ""

            if header_line == "Objective":
                text = body.strip().strip("'\"")
                if text:
                    result["objective"] = text

            elif header_line == "Steps":
                steps = []
                for line in body.split("\n"):
                    line = line.strip()
                    m = re.match(r"\d+\.\s+(.+)", line)
                    if m:
                        desc = m.group(1).strip()
                        sid = re.sub(r"[^a-z0-9_]", "_", desc.lower().strip())
                        sid = re.sub(r"_+", "_", sid).strip("_")
                        steps.append({
                            "id": sid or f"step_{len(steps) + 1}",
                            "description": desc,
                        })
                if steps:
                    result["steps"] = steps

            elif header_line == "Blocking Conditions":
                conditions = []
                for line in body.split("\n"):
                    line = line.strip()
                    m = re.match(r"[-*]\s+(.+)", line)
                    if m:
                        conditions.append(m.group(1).strip().rstrip("."))
                if conditions:
                    result["blocking_conditions"] = conditions

            elif header_line == "Outputs":
                outputs = []
                in_code_block = False
                for line in body.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        outputs.append(stripped)
                        continue
                    m = re.match(r"[-*]\s+(.+)", stripped)
                    if m:
                        outputs.append(m.group(1).strip())
                if outputs:
                    result["outputs"] = outputs

            elif header_line == "Final Report Required Sections":
                sections_list = []
                for line in body.split("\n"):
                    line = line.strip()
                    m = re.match(r"[-*]\s+(.+)", line)
                    if m:
                        sections_list.append(m.group(1).strip().rstrip("."))
                if sections_list:
                    result["final_report_sections"] = sections_list

        return result

    def load_playbook_contract(self, playbook_id: str) -> Optional[PlaybookContract]:
        registry = self.resolver.load()
        entry = registry.get(playbook_id)
        if not entry:
            return None

        playbook_path = entry.get("path", "")
        full_path = self.workspace_root / playbook_path if playbook_path else None

        md_fallback = self._parse_playbook_markdown(full_path) if full_path else {}

        steps_data = entry.get("steps", []) or md_fallback.get("steps", [])
        steps = []
        for s in steps_data:
            steps.append(PlaybookStep(
                id=s.get("id", ""),
                skill=s.get("skill"),
                description=s.get("description", ""),
                depends_on=s.get("depends_on", []),
            ))

        return PlaybookContract(
            id=playbook_id,
            objective=entry.get("objective") or md_fallback.get("objective", ""),
            required_agents=entry.get("required_agents", []),
            required_skills=entry.get("required_skills", []),
            required_lcps=entry.get("required_lcps", []),
            allowed_mcps=entry.get("allowed_mcps", []),
            steps=steps,
            blocking_conditions=entry.get("blocking_conditions") or md_fallback.get("blocking_conditions", []),
            outputs=entry.get("outputs") or md_fallback.get("outputs", []),
            final_report_sections=entry.get("final_report_sections") or md_fallback.get("final_report_sections", []),
            risk_level=entry.get("risk_level", "low"),
            required_capabilities=entry.get("required_capabilities", []),
            path=str(full_path) if full_path else "",
        )

    def playbook_file_exists(self, playbook_id: str) -> bool:
        path = self.resolver.get_playbook_path(playbook_id)
        if not path:
            return False
        full_path = self.workspace_root / path
        return full_path.exists()

    def list_available_playbooks(self) -> list[str]:
        self.resolver.load()
        return self.resolver.list_playbooks()
