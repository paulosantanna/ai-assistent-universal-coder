from pathlib import Path

from medical_research_mcp.dependency_security import (
    inventory_dependencies,
    vulnerability_source_policy,
)


def test_inventory_python_and_npm(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("httpx==0.28.1\n", encoding="utf-8")
    (tmp_path / "package.json").write_text(
        '{"dependencies":{"example-package":"1.2.3"}}',
        encoding="utf-8",
    )
    dependencies = inventory_dependencies(str(tmp_path))
    assert any(item["name"] == "httpx" for item in dependencies)
    assert any(item["ecosystem"] == "npm" for item in dependencies)


def test_vulnerability_policy_is_multi_source() -> None:
    policy = vulnerability_source_policy()
    assert {"OSV", "NVD", "CISA KEV", "FIRST EPSS", "vendor advisories"} <= set(policy)
