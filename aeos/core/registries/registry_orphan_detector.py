from __future__ import annotations

from aeos.core.registries.registry_models import (
    ConsolidatedRegistry,
    OrphanRecord,
    OrphanSeverity,
    RegistryType,
)


class RegistryOrphanDetector:
    def __init__(self):
        self.orphans: list[OrphanRecord] = []

    def detect(self, registry: ConsolidatedRegistry) -> list[OrphanRecord]:
        self.orphans = []

        agent_ids = set(registry.agents.keys())
        skill_ids = set(registry.skills.keys())
        mcp_ids = set(registry.mcps.keys())
        lcp_ids = set(registry.lcps.keys())

        for playbook_id, playbook in registry.playbooks.items():
            for agent_ref in playbook.required_agents:
                if agent_ref not in agent_ids:
                    self.orphans.append(
                        OrphanRecord(
                            orphan_id=agent_ref,
                            orphan_type="agent",
                            referenced_by=f"playbook:{playbook_id}",
                            reference_field="required_agents",
                            severity=OrphanSeverity.CRITICAL,
                            description=f"Playbook '{playbook_id}' requires agent '{agent_ref}' which is not registered",
                        )
                    )

            for skill_ref in playbook.required_skills:
                if skill_ref not in skill_ids:
                    self.orphans.append(
                        OrphanRecord(
                            orphan_id=skill_ref,
                            orphan_type="skill",
                            referenced_by=f"playbook:{playbook_id}",
                            reference_field="required_skills",
                            severity=OrphanSeverity.HIGH,
                            description=f"Playbook '{playbook_id}' requires skill '{skill_ref}' which is not registered",
                        )
                    )

            for lcp_ref in playbook.required_lcps:
                if lcp_ref not in lcp_ids:
                    self.orphans.append(
                        OrphanRecord(
                            orphan_id=lcp_ref,
                            orphan_type="lcp",
                            referenced_by=f"playbook:{playbook_id}",
                            reference_field="required_lcps",
                            severity=OrphanSeverity.HIGH,
                            description=f"Playbook '{playbook_id}' requires LCP '{lcp_ref}' which is not registered",
                        )
                    )

            for mcp_ref in playbook.allowed_mcps:
                if mcp_ref not in mcp_ids:
                    self.orphans.append(
                        OrphanRecord(
                            orphan_id=mcp_ref,
                            orphan_type="mcp",
                            referenced_by=f"playbook:{playbook_id}",
                            reference_field="allowed_mcps",
                            severity=OrphanSeverity.HIGH,
                            description=f"Playbook '{playbook_id}' allows MCP '{mcp_ref}' which is not registered",
                        )
                    )

        for skill_id, skill in registry.skills.items():
            if skill.owner_agent and skill.owner_agent not in agent_ids:
                if skill.owner_agent == "enterprise":
                    severity = OrphanSeverity.MEDIUM
                else:
                    severity = OrphanSeverity.CRITICAL
                self.orphans.append(
                    OrphanRecord(
                        orphan_id=skill.owner_agent,
                        orphan_type="agent",
                        referenced_by=f"skill:{skill_id}",
                        reference_field="owner_agent",
                        severity=severity,
                        description=f"Skill '{skill_id}' references owner_agent '{skill.owner_agent}' which is not registered",
                    )
                )

        return self.orphans

    def count_by_severity(self) -> dict[str, int]:
        counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for o in self.orphans:
            counts[o.severity.value] += 1
        return counts

    def has_critical_orphans(self) -> bool:
        return any(o.severity == OrphanSeverity.CRITICAL for o in self.orphans)

    def has_high_orphans(self) -> bool:
        return any(o.severity == OrphanSeverity.HIGH for o in self.orphans)
