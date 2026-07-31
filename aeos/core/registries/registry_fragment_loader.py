from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import yaml

from aeos.core.registries.registry_models import (
    AgentEntry,
    BlueprintEntry,
    FragmentCategory,
    FragmentMetadata,
    LCPEntry,
    LoadedFragment,
    MCPEntry,
    PlaybookEntry,
    ProfileEntry,
    RegistryType,
    SkillEntry,
    SubAgentEntry,
)


def _classify_fragment(filepath: str) -> tuple[FragmentCategory, Optional[str]]:
    name = Path(filepath).stem
    full = Path(filepath).name

    if full.startswith("enterprise-"):
        return FragmentCategory.ENTERPRISE, None

    if ".additions." in full:
        m = re.search(r"v?(\d+[_\d]*(?:to)?v?\d*)", name)
        version = m.group(1) if m else None
        return FragmentCategory.ADDITIONS, version

    return FragmentCategory.BASE, None


def _infer_registry_type(filepath: str) -> Optional[RegistryType]:
    name = Path(filepath).stem.lower()
    full = Path(filepath).name.lower()

    for rt in RegistryType:
        if rt.value in name or rt.value in full:
            return rt

    if "agent" in name or "agent" in full:
        return RegistryType.AGENTS
    if "skill" in name or "skill" in full:
        return RegistryType.SKILLS
    if "playbook" in name or "playbook" in full:
        return RegistryType.PLAYBOOKS
    if "mcp" in name or "mcp" in full:
        return RegistryType.MCPS
    if "lcp" in name or "lcp" in full:
        return RegistryType.LCPS
    if "blueprint" in name or "blueprint" in full:
        return RegistryType.BLUEPRINTS
    if "profile" in name or "workbench" in name:
        return RegistryType.PROFILES

    return None


def _registry_entries(data: dict, key: str) -> list[dict]:
    raw = data.get(key, [])
    if isinstance(raw, dict):
        raw = raw.get("entries", [])
    return [entry for entry in raw if isinstance(entry, dict) and "id" in entry]


def _normalize_entry_path(path_value: Optional[str], fragment_path: Path, workspace_root: Path) -> Optional[str]:
    if not path_value:
        return path_value

    raw = Path(path_value)
    if raw.is_absolute() or (workspace_root / raw).exists():
        return path_value.replace("\\", "/")

    if fragment_path.parent.name == "registries":
        package_candidate = fragment_path.parent.parent / raw
        if package_candidate.exists():
            try:
                return str(package_candidate.resolve().relative_to(workspace_root)).replace("\\", "/")
            except ValueError:
                return str(package_candidate.resolve())

    return path_value.replace("\\", "/")


def _parse_agents(data: dict, fragment_path: Path, workspace_root: Path) -> tuple[list[AgentEntry], list[SubAgentEntry]]:
    agents = []
    subagents = []
    for entry in _registry_entries(data, "agents"):
        agents.append(AgentEntry(
            id=entry["id"],
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
            role=entry.get("role"),
            can_delegate=entry.get("can_delegate"),
            can_block=entry.get("can_block"),
            independent=entry.get("independent"),
        ))
    for entry in _registry_entries(data, "subagents"):
        subagents.append(SubAgentEntry(
            id=entry["id"],
            parent_roles=entry.get("parent_roles", []),
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
        ))
    return agents, subagents


def _parse_skills(data: dict, fragment_path: Path, workspace_root: Path) -> list[SkillEntry]:
    skills = []
    for entry in _registry_entries(data, "skills"):
        caps = entry.get("capabilities", [])
        if isinstance(caps, list):
            caps_list = caps
        elif isinstance(caps, str):
            caps_list = [c.strip() for c in caps.split(",")]
        else:
            caps_list = []
        skills.append(SkillEntry(
            id=entry["id"],
            owner_agent=entry.get("owner_agent") or entry.get("agent"),
            risk_level=entry.get("risk_level") or entry.get("risk"),
            capabilities=caps_list,
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
            version=entry.get("version"),
            production_ready=entry.get("production_ready", entry.get("enabled")),
        ))
    return skills


def _parse_playbooks(data: dict, fragment_path: Path, workspace_root: Path) -> list[PlaybookEntry]:
    playbooks = []
    for entry in _registry_entries(data, "playbooks"):
        playbooks.append(PlaybookEntry(
            id=entry["id"],
            risk_level=entry.get("risk_level") or entry.get("risk"),
            required_agents=entry.get("required_agents", []),
            required_skills=entry.get("required_skills", []),
            required_lcps=entry.get("required_lcps", []),
            allowed_mcps=entry.get("allowed_mcps", []),
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
            version=entry.get("version"),
            production_ready=entry.get("production_ready", entry.get("enabled")),
        ))
    return playbooks


def _parse_mcps(data: dict, fragment_path: Path, workspace_root: Path) -> list[MCPEntry]:
    mcps = []
    for entry in _registry_entries(data, "mcps"):
        caps = entry.get("capabilities", [])
        mcps.append(MCPEntry(
            id=entry["id"],
            type=entry.get("type"),
            transport=entry.get("transport"),
            config=_normalize_entry_path(entry.get("config"), fragment_path, workspace_root),
            risk_level=entry.get("risk_level") or entry.get("risk"),
            capabilities=caps if isinstance(caps, list) else [],
            tools=entry.get("tools", []),
            write_allowed=entry.get("write_allowed"),
            sandbox_required=entry.get("sandbox_required"),
            approval_required=entry.get("approval_required"),
            allowlist_required=entry.get("allowlist_required"),
            enabled=entry.get("enabled", True),
            reason=entry.get("reason"),
        ))
    return mcps


def _parse_lcps(data: dict, fragment_path: Path, workspace_root: Path) -> list[LCPEntry]:
    lcps = []
    for entry in _registry_entries(data, "lcps"):
        lcps.append(LCPEntry(
            id=entry["id"],
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
            priority=entry.get("priority", 50),
            scope=entry.get("scope", "global"),
            applies_to=entry.get("applies_to", []),
        ))
    return lcps


def _parse_blueprints(data: dict, fragment_path: Path, workspace_root: Path) -> list[BlueprintEntry]:
    blueprints = []
    for entry in _registry_entries(data, "blueprints"):
        blueprints.append(BlueprintEntry(
            id=entry["id"],
            type=entry.get("type"),
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
        ))
    return blueprints


def _parse_profiles(data: dict, fragment_path: Path, workspace_root: Path) -> list[ProfileEntry]:
    profiles = []
    for entry in _registry_entries(data, "profiles"):
        profiles.append(ProfileEntry(
            id=entry["id"],
            path=_normalize_entry_path(entry.get("path"), fragment_path, workspace_root),
        ))
    return profiles


class RegistryFragmentLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.fragments: list[LoadedFragment] = []

    def load_fragment(self, filepath: str) -> LoadedFragment:
        full_path = Path(filepath)
        if not full_path.exists():
            raise FileNotFoundError(f"Fragment not found: {full_path}")

        category, version = _classify_fragment(filepath)
        reg_type = _infer_registry_type(filepath)

        metadata = FragmentMetadata(
            path=str(full_path.resolve()),
            registry_type=reg_type or RegistryType.AGENTS,
            category=category,
            version_label=version,
        )

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data:
                metadata.loaded = False
                metadata.parse_error = "Empty YAML file"
                return LoadedFragment(metadata=metadata)

            agents, subagents = _parse_agents(data, full_path, self.workspace_root)
            skills = _parse_skills(data, full_path, self.workspace_root)
            playbooks = _parse_playbooks(data, full_path, self.workspace_root)
            mcps = _parse_mcps(data, full_path, self.workspace_root)
            lcps = _parse_lcps(data, full_path, self.workspace_root)
            blueprints = _parse_blueprints(data, full_path, self.workspace_root)
            profiles = _parse_profiles(data, full_path, self.workspace_root)

            entry_count = (
                len(agents) + len(subagents) + len(skills) + len(playbooks)
                + len(mcps) + len(lcps) + len(blueprints) + len(profiles)
            )

            metadata.loaded = True
            metadata.entry_count = entry_count

            return LoadedFragment(
                metadata=metadata,
                agents=agents,
                subagents=subagents,
                skills=skills,
                playbooks=playbooks,
                mcps=mcps,
                lcps=lcps,
                blueprints=blueprints,
                profiles=profiles,
            )

        except Exception as e:
            metadata.loaded = False
            metadata.parse_error = str(e)
            return LoadedFragment(metadata=metadata)

    def load_fragments(self, filepaths: list[str]) -> list[LoadedFragment]:
        self.fragments = []
        for fp in filepaths:
            try:
                frag = self.load_fragment(fp)
            except FileNotFoundError as e:
                frag = LoadedFragment(
                    metadata=FragmentMetadata(
                        path=fp,
                        registry_type=RegistryType.AGENTS,
                        category=FragmentCategory.BASE,
                        loaded=False,
                        parse_error=str(e),
                    )
                )
            self.fragments.append(frag)
        return self.fragments

