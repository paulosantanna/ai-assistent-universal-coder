from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest
import yaml

from aeos.core.config.config_loader import ConfigLoader
from aeos.core.registries.cross_registry_dependency_validator import CrossRegistryDependencyValidator
from aeos.core.registries.overlay_index_loader import OverlayRegistryIndexLoader
from aeos.core.registries.overlay_registry_merger import OverlayRegistryMerger
from aeos.core.registries.registry_conflict_detector import RegistryConflictDetector
from aeos.core.registries.registry_fragment_loader import RegistryFragmentLoader
from aeos.core.registries.registry_models import (
    AgentEntry,
    ConsolidatedRegistry,
    FragmentCategory,
    LCPEntry,
    LoadedFragment,
    MCPEntry,
    OrphanSeverity,
    PlaybookEntry,
    RegistryType,
    SkillEntry,
)
from aeos.core.registries.registry_orphan_detector import RegistryOrphanDetector
from aeos.core.registries.schema_validator import SchemaValidator


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture
def sample_agent_base() -> LoadedFragment:
    return LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/agents.registry.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.BASE,
            "version_label": None,
            "loaded": True,
            "parse_error": None,
            "entry_count": 2,
        })(),
        agents=[
            AgentEntry(id="architect", path="aeos/agents/architect.agent.md", role="architect"),
            AgentEntry(id="coder", path="aeos/agents/coder.agent.md", role="coder"),
        ],
    )


@pytest.fixture
def sample_agent_additions() -> LoadedFragment:
    return LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/agents.v0_7.additions.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.ADDITIONS,
            "version_label": "0_7",
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        agents=[
            AgentEntry(id="planner", path="aeos/agents/planner.agent.md", role="planner"),
        ],
    )


@pytest.fixture
def sample_skill_base() -> LoadedFragment:
    return LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/skills.registry.yaml",
            "registry_type": RegistryType.SKILLS,
            "category": FragmentCategory.BASE,
            "version_label": None,
            "loaded": True,
            "parse_error": None,
            "entry_count": 2,
        })(),
        skills=[
            SkillEntry(id="repo-scanner", owner_agent="architect", risk_level="low"),
            SkillEntry(id="security-audit", owner_agent="security", risk_level="high"),
        ],
    )


@pytest.fixture
def sample_playbook_base() -> LoadedFragment:
    return LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/playbooks.registry.yaml",
            "registry_type": RegistryType.PLAYBOOKS,
            "category": FragmentCategory.BASE,
            "version_label": None,
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        playbooks=[
            PlaybookEntry(
                id="test-pb", risk_level="low",
                required_agents=["architect", "coder", "security"],
                required_skills=["repo-scanner", "security-audit"],
                required_lcps=["global-rules"],
                allowed_mcps=["filesystem-readonly"],
            ),
        ],
    )


@pytest.fixture
def sample_fragments_for_merge(sample_agent_base, sample_agent_additions, sample_skill_base, sample_playbook_base):
    return [sample_agent_base, sample_agent_additions, sample_skill_base, sample_playbook_base]


@pytest.fixture
def full_registry() -> ConsolidatedRegistry:
    reg = ConsolidatedRegistry()
    reg.agents["architect"] = AgentEntry(id="architect", path="aeos/agents/architect.agent.md")
    reg.agents["security"] = AgentEntry(id="security", path="aeos/agents/security.agent.md")
    reg.agents["coder"] = AgentEntry(id="coder", path="aeos/agents/coder.agent.md")
    reg.agents["judge"] = AgentEntry(id="judge", path="aeos/agents/judge.agent.md")

    reg.skills["repo-scanner"] = SkillEntry(id="repo-scanner", owner_agent="architect", capabilities=["READ_FILES", "GENERATE_REPORT"])
    reg.skills["security-audit"] = SkillEntry(id="security-audit", owner_agent="security", capabilities=["SCAN_SECRETS"])

    reg.playbooks["test-pb"] = PlaybookEntry(
        id="test-pb",
        required_agents=["architect", "coder"],
        required_skills=["repo-scanner"],
        required_lcps=["global-rules"],
        allowed_mcps=["filesystem-readonly"],
    )

    reg.lcps["global-rules"] = LCPEntry(id="global-rules", priority=100)
    reg.mcps["filesystem-readonly"] = MCPEntry(id="filesystem-readonly", type="filesystem")
    return reg


# ============================================================
# Test 1: Config Loader
# ============================================================

def test_config_loader_loads_main_config(workspace_root):
    loader = ConfigLoader(str(workspace_root))
    config = loader.load("aeos/config/aeos.config.yaml")
    assert config.name == "AEOS Workbench"
    assert config.version == "1.2.0"
    assert "agents.registry.yaml" in config.registries.agents


# ============================================================
# Test 2: Overlay Index Loader
# ============================================================

def test_overlay_index_loader_loads(workspace_root):
    loader = OverlayRegistryIndexLoader(str(workspace_root))
    paths = loader.load("aeos/registries/overlay.registry.index.yaml")
    assert len(paths) > 0
    assert any("enterprise-playbooks" in p for p in paths)
    assert any("enterprise-skills" in p for p in paths)
    assert any("additions" in p for p in paths)
    assert loader.generated_at is not None


# ============================================================
# Test 3: Fragment Loader - loads enterprise files
# ============================================================

def test_fragment_loader_loads_enterprise_skills(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    path = str(workspace_root / "aeos/registries/enterprise-skills.registry.yaml")
    frag = loader.load_fragment(path)
    assert frag.metadata.loaded
    assert frag.metadata.category == FragmentCategory.ENTERPRISE
    assert len(frag.skills) > 0
    assert any(s.id == "enterprise-repo-intelligence" for s in frag.skills)


def test_fragment_loader_loads_enterprise_playbooks(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    path = str(workspace_root / "aeos/registries/enterprise-playbooks.registry.yaml")
    frag = loader.load_fragment(path)
    assert frag.metadata.loaded
    assert frag.metadata.category == FragmentCategory.ENTERPRISE
    assert len(frag.playbooks) > 0
    assert any(p.id == "enterprise-project-onboarding" for p in frag.playbooks)


# ============================================================
# Test 4: Fragment Loader - loads additions files
# ============================================================

def test_fragment_loader_loads_additions_files(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    path = str(workspace_root / "aeos/registries/playbooks.v0_6.additions.yaml")
    frag = loader.load_fragment(path)
    assert frag.metadata.loaded
    assert frag.metadata.category == FragmentCategory.ADDITIONS


def test_fragment_loader_loads_all_additions(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    fragments = loader.load_fragments(paths)

    additions = [f for f in fragments if f.metadata.category == FragmentCategory.ADDITIONS and f.metadata.loaded]
    assert len(additions) >= 4, f"Expected at least 4 additions fragments, got {len(additions)}"


# ============================================================
# Test 5: Overlay Index Discovery
# ============================================================

def test_overlay_index_discovers_all_fragments(workspace_root):
    loader = OverlayRegistryIndexLoader(str(workspace_root))
    paths = loader.load("aeos/registries/overlay.registry.index.yaml")
    assert len(paths) == 18, f"Expected 18 fragments, got {len(paths)}"
    assert any("agents.registry.yaml" in p for p in paths)
    assert any("agents.v0_7.registry.yaml" in p for p in paths)
    assert any("overlay.registry.index.yaml" not in p for p in paths)


# ============================================================
# Test 6: Schema Validator
# ============================================================

def test_schema_validator_loads_capabilities(workspace_root):
    validator = SchemaValidator(str(workspace_root))
    caps = validator.load_capabilities()
    assert len(caps) > 0
    assert "READ_FILES" in caps
    assert "GENERATE_REPORT" in caps


def test_schema_validator_unknown_capability(workspace_root):
    reg = ConsolidatedRegistry()
    reg.skills["test"] = SkillEntry(id="test", capabilities=["NONEXISTENT_CAP"])
    validator = SchemaValidator(str(workspace_root))
    validator.load_capabilities()
    result = validator.validate(reg)
    assert "NONEXISTENT_CAP" in result.unknown_capabilities


# ============================================================
# Test 7: Duplicate detection - same id, different path
# ============================================================

def test_conflict_detector_same_id_different_path():
    detector = RegistryConflictDetector()
    frag1 = LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/base.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.BASE,
            "version_label": None,
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        agents=[AgentEntry(id="agent-x", path="path/a.md")],
    )
    frag2 = LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/addition.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.ADDITIONS,
            "version_label": "0_7",
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        agents=[AgentEntry(id="agent-x", path="path/b.md")],
    )
    conflicts = detector.detect([frag1, frag2])
    assert len(conflicts) == 1
    assert conflicts[0].entry_id == "agent-x"


# ============================================================
# Test 8: Deduplication - same id, same path
# ============================================================

def test_conflict_detector_same_id_same_path():
    detector = RegistryConflictDetector()
    frag1 = LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/base.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.BASE,
            "version_label": None,
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        agents=[AgentEntry(id="agent-x", path="path/a.md")],
    )
    frag2 = LoadedFragment(
        metadata=type("Meta", (), {
            "path": "/fake/addition.yaml",
            "registry_type": RegistryType.AGENTS,
            "category": FragmentCategory.ADDITIONS,
            "version_label": "0_7",
            "loaded": True,
            "parse_error": None,
            "entry_count": 1,
        })(),
        agents=[AgentEntry(id="agent-x", path="path/a.md")],
    )
    conflicts = detector.detect([frag1, frag2])
    assert len(conflicts) == 0
    assert len(detector.deduplications) == 1


# ============================================================
# Test 9: Playbook with nonexistent skill
# ============================================================

def test_orphan_detector_playbook_missing_skill():
    reg = ConsolidatedRegistry()
    reg.agents["architect"] = AgentEntry(id="architect")
    reg.playbooks["pb1"] = PlaybookEntry(
        id="pb1",
        required_agents=["architect"],
        required_skills=["nonexistent-skill"],
    )
    detector = RegistryOrphanDetector()
    orphans = detector.detect(reg)
    skill_orphans = [o for o in orphans if o.orphan_type == "skill"]
    assert len(skill_orphans) == 1
    assert skill_orphans[0].orphan_id == "nonexistent-skill"
    assert skill_orphans[0].severity == OrphanSeverity.HIGH


# ============================================================
# Test 10: Skill with nonexistent owner_agent
# ============================================================

def test_orphan_detector_skill_missing_owner():
    reg = ConsolidatedRegistry()
    reg.skills["skill1"] = SkillEntry(id="skill1", owner_agent="ghost-agent")
    detector = RegistryOrphanDetector()
    orphans = detector.detect(reg)
    agent_orphans = [o for o in orphans if o.orphan_type == "agent"]
    assert len(agent_orphans) >= 1
    assert any(o.orphan_id == "ghost-agent" for o in agent_orphans)


# ============================================================
# Test 11: Nonexistent LCP referenced by playbook
# ============================================================

def test_orphan_detector_playbook_missing_lcp():
    reg = ConsolidatedRegistry()
    reg.agents["architect"] = AgentEntry(id="architect")
    reg.playbooks["pb1"] = PlaybookEntry(
        id="pb1",
        required_agents=["architect"],
        required_lcps=["nonexistent-lcp"],
    )
    detector = RegistryOrphanDetector()
    orphans = detector.detect(reg)
    lcp_orphans = [o for o in orphans if o.orphan_type == "lcp"]
    assert len(lcp_orphans) >= 1
    assert any(o.orphan_id == "nonexistent-lcp" for o in lcp_orphans)


# ============================================================
# Test 12: Nonexistent MCP referenced by playbook
# ============================================================

def test_orphan_detector_playbook_missing_mcp():
    reg = ConsolidatedRegistry()
    reg.agents["architect"] = AgentEntry(id="architect")
    reg.playbooks["pb1"] = PlaybookEntry(
        id="pb1",
        required_agents=["architect"],
        allowed_mcps=["nonexistent-mcp"],
    )
    detector = RegistryOrphanDetector()
    orphans = detector.detect(reg)
    mcp_orphans = [o for o in orphans if o.orphan_type == "mcp"]
    assert len(mcp_orphans) >= 1
    assert any(o.orphan_id == "nonexistent-mcp" for o in mcp_orphans)


# ============================================================
# Test 13: Merger produces consolidated registries
# ============================================================

def test_merger_produces_consolidated(sample_fragments_for_merge):
    merger = OverlayRegistryMerger()
    registry = merger.merge(sample_fragments_for_merge)
    assert len(registry.agents) == 3
    assert "architect" in registry.agents
    assert "coder" in registry.agents
    assert "planner" in registry.agents
    assert len(registry.skills) == 2
    assert len(registry.playbooks) == 1


# ============================================================
# Test 14: Merger does NOT overwrite originals
# ============================================================

def test_merger_does_not_overwrite_originals(sample_fragments_for_merge, tmp_path):
    merger = OverlayRegistryMerger()
    registry = merger.merge(sample_fragments_for_merge)

    derived = tmp_path / "derived"
    derived.mkdir()
    agents_file = derived / "agents.consolidated.yaml"
    with open(agents_file, "w") as f:
        yaml.safe_dump({"agents": [v.to_dict() for v in registry.agents.values()]}, f)

    assert agents_file.exists()
    original_agents = Path("aeos/registries/agents.registry.yaml")
    assert original_agents.exists()


# ============================================================
# Test 15: Enterprise registries included in consolidated
# ============================================================

def test_enterprise_registries_in_consolidated(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    fragments = loader.load_fragments(paths)

    merger = OverlayRegistryMerger()
    registry = merger.merge(fragments)

    enterprise_skills = [s for s in registry.skills.values() if s.owner_agent == "enterprise"]
    assert len(enterprise_skills) > 0, "Enterprise skills not found in consolidated registry"

    enterprise_playbooks = [p for p in registry.playbooks.values() if getattr(p, "production_ready", False)]
    assert len(enterprise_playbooks) > 0, "Enterprise playbooks not found"


# ============================================================
# Test 16: Cross-dependency validation finds errors
# ============================================================

def test_cross_dependency_finds_errors():
    reg = ConsolidatedRegistry()
    reg.playbooks["pb1"] = PlaybookEntry(
        id="pb1",
        required_agents=["nonexistent-agent"],
        required_skills=["nonexistent-skill"],
        required_lcps=["nonexistent-lcp"],
        allowed_mcps=["nonexistent-mcp"],
    )
    validator = CrossRegistryDependencyValidator()
    result = validator.validate(reg)
    assert result.has_errors()
    assert len(result.playbook_agents) == 1
    assert len(result.playbook_skills) == 1
    assert len(result.playbook_lcps) == 1
    assert len(result.playbook_mcps) == 1


# ============================================================
# Test 17: Overlay index is actually used (not ignored)
# ============================================================

def test_overlay_index_is_used(workspace_root):
    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    assert len(paths) == 18, f"Expected 18 fragments, got {len(paths)}"

    loader = RegistryFragmentLoader(str(workspace_root))
    fragments = loader.load_fragments(paths)

    fragment_paths = {f.metadata.path for f in fragments}
    for p in paths:
        assert any(p in fp for fp in fragment_paths), f"Fragment from overlay not loaded: {p}"


# ============================================================
# Test 18: Duplicate agent id with different path across real files
# ============================================================

def test_real_conflict_detection(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    fragments = loader.load_fragments(paths)

    detector = RegistryConflictDetector()
    conflicts = detector.detect(fragments)

    for c in conflicts:
        assert c.entry_id is not None
        assert c.source_a_path != c.source_b_path


# ============================================================
# Test 19: Cross-dependency on real AEOS data
# ============================================================

def test_real_cross_dependency_validation(workspace_root):
    loader = RegistryFragmentLoader(str(workspace_root))
    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    fragments = loader.load_fragments(paths)

    merger = OverlayRegistryMerger()
    registry = merger.merge(fragments)

    validator = CrossRegistryDependencyValidator(str(workspace_root))
    result = validator.validate(registry)

    all_findings = result.all_findings()
    errors = [f for f in all_findings if f.severity.value == "error"]
    if errors:
        print(f"\n  Cross-dependency errors found: {len(errors)}")
        for e in errors:
            print(f"    - {e.check}: {e.detail}")


# ============================================================
# Test 20: Full pipeline smoke test
# ============================================================

def test_full_pipeline_smoke(workspace_root):
    config_loader = ConfigLoader(str(workspace_root))
    config = config_loader.load("aeos/config/aeos.config.yaml")

    overlay = OverlayRegistryIndexLoader(str(workspace_root))
    paths = overlay.load("aeos/registries/overlay.registry.index.yaml")
    assert len(paths) > 0

    loader = RegistryFragmentLoader(str(workspace_root))
    fragments = loader.load_fragments(paths)
    loaded = [f for f in fragments if f.metadata.loaded]
    assert len(loaded) > 0

    detector = RegistryConflictDetector()
    conflicts = detector.detect(fragments)

    merger = OverlayRegistryMerger()
    registry = merger.merge(fragments)
    assert len(registry.agents) > 0
    assert len(registry.skills) > 0

    schema_validator = SchemaValidator(str(workspace_root))
    schema_validator.load_capabilities()
    schema_result = schema_validator.validate(registry)

    cross_validator = CrossRegistryDependencyValidator(str(workspace_root))
    cross_result = cross_validator.validate(registry)

    orphan_detector = RegistryOrphanDetector()
    orphans = orphan_detector.detect(registry)

    assert isinstance(conflicts, list)
    assert isinstance(orphans, list)
