from pathlib import Path
import argparse
import importlib.util

import yaml

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "skill_factory.py"
spec = importlib.util.spec_from_file_location("skill_factory", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

def test_slugify():
    assert module.slugify("Security Audit Skill") == "security-audit-skill"

def test_required_sections_present():
    skill_md = Path(__file__).resolve().parents[1] / "SKILL.md"
    findings = module.validate_package(skill_md.parent)
    assert not [f for f in findings if f.severity == "ERROR"], [f.render() for f in findings]

def test_architecture_files():
    assert "SKILL.md" in module.architecture_files(1)
    assert "scripts" in module.architecture_files(2)
    assert "knowledge" in module.architecture_files(3)
    assert "evaluation" in module.architecture_files(3)


def test_generated_skill_has_agent_knowledge_and_evaluator_layers(tmp_path):
    args = argparse.Namespace(
        name="Layered Audit Skill",
        description="Audit a repository with evidence-backed findings",
        activation="the user requests a layered audit",
        category="AUDIT",
        level=1,
        risk="MEDIUM",
        output=str(tmp_path),
        force=False,
        registry=None,
        register=False,
    )

    assert module.generate(args) == 0
    package = tmp_path / "layered-audit-skill"
    skill_text = (package / "SKILL.md").read_text(encoding="utf-8")

    assert "architecture_level: 3" in skill_text
    assert (package / "AGENT.md").exists()
    assert (package / "knowledge" / "NEGATIVE_KNOWLEDGE.md").exists()
    assert (package / "knowledge" / "POSITIVE_KNOWLEDGE.md").exists()
    assert (package / "memory" / "OPEN_RISKS.md").exists()
    assert (package / "evaluation" / "HONEST_EVALUATOR.md").exists()
    assert not [f for f in module.validate_package(package) if f.severity == "ERROR"]


def test_generated_skill_registers_for_immediate_consumption(tmp_path):
    workspace = tmp_path / "workspace"
    registry = workspace / "aeos" / "registries" / "skills.registry.yaml"
    output = workspace / "aeos" / "skills" / "generated"
    registry.parent.mkdir(parents=True)
    registry.write_text("skills:\n", encoding="utf-8")

    args = argparse.Namespace(
        name="Instant Consumption Skill",
        description="Generate immediately consumable skill output",
        activation="the user requests instant consumption",
        category="DOCUMENTATION",
        level=2,
        risk="LOW",
        output=str(output),
        force=False,
        registry=str(registry),
        register=True,
    )

    assert module.generate(args) == 0
    data = yaml.safe_load(registry.read_text(encoding="utf-8"))
    entry = next(item for item in data["skills"] if item["id"] == "instant-consumption-skill")

    assert entry["path"] == "aeos/skills/generated/instant-consumption-skill/SKILL.md"
    assert entry["owner_agent"] == "documenter"
    assert "WRITE_SANDBOX_FILES" in entry["capabilities"]
