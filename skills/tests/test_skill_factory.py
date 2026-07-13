from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "skill-factory" / "scripts" / "skill_factory.py"
spec = importlib.util.spec_from_file_location("skill_factory", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

def test_slugify():
    assert module.slugify("Security Audit Skill") == "security-audit-skill"

def test_required_sections_present():
    skill_md = Path(__file__).resolve().parents[1] / "skill-factory" / "SKILL.md"
    findings = module.validate_package(skill_md.parent)
    assert not [f for f in findings if f.severity == "ERROR"], [f.render() for f in findings]

def test_architecture_files():
    assert "SKILL.md" in module.architecture_files(1)
    assert "scripts" in module.architecture_files(2)
    assert "knowledge" in module.architecture_files(3)
