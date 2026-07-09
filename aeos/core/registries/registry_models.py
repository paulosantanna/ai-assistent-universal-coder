from __future__ import annotations

import enum
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


class RegistryType(str, enum.Enum):
    AGENTS = "agents"
    SKILLS = "skills"
    PLAYBOOKS = "playbooks"
    MCPS = "mcps"
    LCPS = "lcps"
    BLUEPRINTS = "blueprints"
    PROFILES = "profiles"


class FragmentCategory(str, enum.Enum):
    BASE = "base"
    ADDITIONS = "additions"
    ENTERPRISE = "enterprise"


class OrphanSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationSeverity(str, enum.Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AgentEntry:
    id: str
    path: Optional[str] = None
    role: Optional[str] = None
    can_delegate: Optional[bool] = None
    can_block: Optional[bool] = None
    independent: Optional[bool] = None

    def key(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class SubAgentEntry:
    id: str
    parent_roles: list[str] = field(default_factory=list)
    path: Optional[str] = None

    def key(self) -> str:
        return self.id


@dataclass
class SkillEntry:
    id: str
    owner_agent: Optional[str] = None
    risk_level: Optional[str] = None
    capabilities: list[str] = field(default_factory=list)
    path: Optional[str] = None
    version: Optional[str] = None
    production_ready: Optional[bool] = None

    def key(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class PlaybookEntry:
    id: str
    risk_level: Optional[str] = None
    required_agents: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)
    required_lcps: list[str] = field(default_factory=list)
    allowed_mcps: list[str] = field(default_factory=list)
    path: Optional[str] = None
    version: Optional[str] = None
    production_ready: Optional[bool] = None

    def key(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class MCPEntry:
    id: str
    type: Optional[str] = None
    transport: Optional[str] = None
    config: Optional[str] = None
    risk_level: Optional[str] = None
    capabilities: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    write_allowed: Optional[bool] = None
    sandbox_required: Optional[bool] = None
    approval_required: Optional[bool] = None
    allowlist_required: Optional[bool] = None
    enabled: bool = True
    reason: Optional[str] = None

    def key(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class LCPEntry:
    id: str
    path: Optional[str] = None
    priority: int = 50
    scope: str = "global"
    applies_to: list[str] = field(default_factory=list)

    def key(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BlueprintEntry:
    id: str
    type: Optional[str] = None
    path: Optional[str] = None

    def key(self) -> str:
        return self.id


@dataclass
class ProfileEntry:
    id: str
    path: Optional[str] = None

    def key(self) -> str:
        return self.id


@dataclass
class FragmentMetadata:
    path: str
    registry_type: RegistryType
    category: FragmentCategory
    version_label: Optional[str] = None
    loaded: bool = False
    parse_error: Optional[str] = None
    entry_count: int = 0


@dataclass
class LoadedFragment:
    metadata: FragmentMetadata
    agents: list[AgentEntry] = field(default_factory=list)
    subagents: list[SubAgentEntry] = field(default_factory=list)
    skills: list[SkillEntry] = field(default_factory=list)
    playbooks: list[PlaybookEntry] = field(default_factory=list)
    mcps: list[MCPEntry] = field(default_factory=list)
    lcps: list[LCPEntry] = field(default_factory=list)
    blueprints: list[BlueprintEntry] = field(default_factory=list)
    profiles: list[ProfileEntry] = field(default_factory=list)


@dataclass
class ConsolidatedRegistry:
    agents: dict[str, AgentEntry] = field(default_factory=dict)
    subagents: dict[str, SubAgentEntry] = field(default_factory=dict)
    skills: dict[str, SkillEntry] = field(default_factory=dict)
    playbooks: dict[str, PlaybookEntry] = field(default_factory=dict)
    mcps: dict[str, MCPEntry] = field(default_factory=dict)
    lcps: dict[str, LCPEntry] = field(default_factory=dict)
    blueprints: dict[str, BlueprintEntry] = field(default_factory=dict)
    profiles: dict[str, ProfileEntry] = field(default_factory=dict)


@dataclass
class ConfigRegistryPaths:
    agents: str = ""
    skills: str = ""
    playbooks: str = ""
    mcps: str = ""
    lcps: str = ""
    blueprints: str = ""
    enterprise_skills: str = ""
    enterprise_playbooks: str = ""
    workbench_profiles: str = ""
    overlay_index: str = ""


@dataclass
class AEOSConfig:
    name: str = ""
    version: str = ""
    mode: str = ""
    registries: ConfigRegistryPaths = field(default_factory=ConfigRegistryPaths)


@dataclass
class ConflictRecord:
    entry_id: str
    registry_type: RegistryType
    source_a_path: str
    source_b_path: str
    existing_path: Optional[str] = None
    conflicting_path: Optional[str] = None
    description: str = ""


@dataclass
class OrphanRecord:
    orphan_id: str
    orphan_type: str
    referenced_by: str
    reference_field: str
    severity: OrphanSeverity
    description: str = ""


@dataclass
class ValidationFinding:
    check: str
    status: str
    severity: ValidationSeverity
    detail: str = ""


@dataclass
class CrossDependencyResult:
    agent_skills: list[ValidationFinding] = field(default_factory=list)
    playbook_agents: list[ValidationFinding] = field(default_factory=list)
    playbook_skills: list[ValidationFinding] = field(default_factory=list)
    playbook_lcps: list[ValidationFinding] = field(default_factory=list)
    playbook_mcps: list[ValidationFinding] = field(default_factory=list)
    skill_capabilities: list[ValidationFinding] = field(default_factory=list)
    mcp_capabilities: list[ValidationFinding] = field(default_factory=list)
    file_paths: list[ValidationFinding] = field(default_factory=list)
    config_paths: list[ValidationFinding] = field(default_factory=list)

    def all_findings(self) -> list[ValidationFinding]:
        result = []
        for attr in vars(self):
            result.extend(getattr(self, attr))
        return result

    def errors(self) -> list[ValidationFinding]:
        return [f for f in self.all_findings() if f.severity == ValidationSeverity.ERROR]

    def has_errors(self) -> bool:
        return len(self.errors()) > 0


@dataclass
class SchemaValidationResult:
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    unknown_capabilities: set[str] = field(default_factory=set)


@dataclass
class MergeManifest:
    generated_at: str = ""
    fragments_loaded: int = 0
    fragments_failed: int = 0
    total_entries_by_type: dict[str, int] = field(default_factory=dict)
    deduplications: list[dict[str, Any]] = field(default_factory=list)
    conflicts_resolved: int = 0
    source_fragments: list[str] = field(default_factory=list)
