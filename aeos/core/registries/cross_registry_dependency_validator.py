from __future__ import annotations

from pathlib import Path

from aeos.core.registries.registry_models import (
    ConsolidatedRegistry,
    CrossDependencyResult,
    ValidationFinding,
    ValidationSeverity,
)


class CrossRegistryDependencyValidator:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()

    def validate(self, registry: ConsolidatedRegistry) -> CrossDependencyResult:
        result = CrossDependencyResult()

        agent_ids = set(registry.agents.keys())
        skill_ids = set(registry.skills.keys())
        playbook_ids = set(registry.playbooks.keys())
        mcp_ids = set(registry.mcps.keys())
        lcp_ids = set(registry.lcps.keys())

        for skill_id, skill in registry.skills.items():
            if skill.owner_agent and skill.owner_agent not in agent_ids:
                result.agent_skills.append(
                    ValidationFinding(
                        check=f"skill.{skill_id}.owner_agent",
                        status="ORPHAN_AGENT",
                        severity=ValidationSeverity.ERROR,
                        detail=f"Skill '{skill_id}' references owner_agent '{skill.owner_agent}' which does not exist in agents registry",
                    )
                )

        for playbook_id, playbook in registry.playbooks.items():
            for agent_ref in playbook.required_agents:
                if agent_ref not in agent_ids:
                    result.playbook_agents.append(
                        ValidationFinding(
                            check=f"playbook.{playbook_id}.required_agents",
                            status="MISSING_AGENT",
                            severity=ValidationSeverity.ERROR,
                            detail=f"Playbook '{playbook_id}' requires agent '{agent_ref}' which does not exist",
                        )
                    )

            for skill_ref in playbook.required_skills:
                if skill_ref not in skill_ids:
                    result.playbook_skills.append(
                        ValidationFinding(
                            check=f"playbook.{playbook_id}.required_skills",
                            status="MISSING_SKILL",
                            severity=ValidationSeverity.ERROR,
                            detail=f"Playbook '{playbook_id}' requires skill '{skill_ref}' which does not exist",
                        )
                    )

            for lcp_ref in playbook.required_lcps:
                if lcp_ref not in lcp_ids:
                    result.playbook_lcps.append(
                        ValidationFinding(
                            check=f"playbook.{playbook_id}.required_lcps",
                            status="MISSING_LCP",
                            severity=ValidationSeverity.ERROR,
                            detail=f"Playbook '{playbook_id}' requires LCP '{lcp_ref}' which does not exist",
                        )
                    )

            for mcp_ref in playbook.allowed_mcps:
                if mcp_ref not in mcp_ids:
                    result.playbook_mcps.append(
                        ValidationFinding(
                            check=f"playbook.{playbook_id}.allowed_mcps",
                            status="MISSING_MCP",
                            severity=ValidationSeverity.ERROR,
                            detail=f"Playbook '{playbook_id}' allows MCP '{mcp_ref}' which does not exist",
                        )
                    )

        for skill_id, skill in registry.skills.items():
            self._validate_path(
                result.file_paths,
                f"skill.{skill_id}.path",
                skill.path,
                f"Skill '{skill_id}'",
            )

        for agent_id, agent in registry.agents.items():
            self._validate_path(
                result.file_paths,
                f"agent.{agent_id}.path",
                agent.path,
                f"Agent '{agent_id}'",
            )

        for playbook_id, playbook in registry.playbooks.items():
            self._validate_path(
                result.file_paths,
                f"playbook.{playbook_id}.path",
                playbook.path,
                f"Playbook '{playbook_id}'",
            )

        for lcp_id, lcp in registry.lcps.items():
            self._validate_path(
                result.file_paths,
                f"lcp.{lcp_id}.path",
                lcp.path,
                f"LCP '{lcp_id}'",
            )

        return result

    def _validate_path(
        self,
        findings: list,
        check: str,
        path: Optional[str],
        label: str,
    ) -> None:
        if not path:
            findings.append(
                ValidationFinding(
                    check=check,
                    status="MISSING_PATH",
                    severity=ValidationSeverity.WARNING,
                    detail=f"{label} has no path defined",
                )
            )
            return
        full = self.workspace_root / path
        if not full.exists():
            findings.append(
                ValidationFinding(
                    check=check,
                    status="PATH_NOT_FOUND",
                    severity=ValidationSeverity.ERROR,
                    detail=f"{label} path '{path}' does not exist on disk",
                )
            )
