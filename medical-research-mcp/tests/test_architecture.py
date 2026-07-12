from pathlib import Path

from medical_research_mcp.AI_architecture import recommend_architecture
from medical_research_mcp.repository import architecture_inventory, scan_repository


def test_repository_scan_discovers_pipeline_and_tests(tmp_path: Path) -> None:
    (tmp_path / "train_model.py").write_text("print('train')", encoding="utf-8")
    (tmp_path / "test_train.py").write_text("def test_x(): assert True", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'", encoding="utf-8")
    scan = scan_repository(str(tmp_path))
    assert "train_model.py" in scan["pipeline_candidates"]
    assert "test_train.py" in scan["tests"]
    assert "pyproject.toml" in scan["manifests"]


def test_small_team_defaults_to_modular_monolith(tmp_path: Path) -> None:
    (tmp_path / "training.py").write_text("", encoding="utf-8")
    result = recommend_architecture(str(tmp_path), team_size=2, deployment_targets=1)
    assert result["recommendation"] == "modular_monolith"


def test_architecture_inventory_has_expected_areas(tmp_path: Path) -> None:
    (tmp_path / "rag_engine.py").write_text("", encoding="utf-8")
    inventory = architecture_inventory(str(tmp_path))
    assert "knowledge" in inventory["areas"]
    assert inventory["areas"]["knowledge"]
