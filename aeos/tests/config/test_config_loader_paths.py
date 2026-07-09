from pathlib import Path
from aeos.core.config.config_loader import ConfigLoader


def test_config_loader_uses_aeos_root(tmp_path: Path):
    aeos_root = tmp_path / "aeos-install"
    aeos_root.mkdir(parents=True)
    config_dir = aeos_root / "aeos" / "config"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "aeos.config.yaml"
    config_file.write_text("aeos:\n  name: test\n  version: 1.0\n  mode: development\nregistries:\n  skills: aeos/registries")

    loader = ConfigLoader(workspace_root=str(tmp_path), aeos_root=str(aeos_root))
    config = loader.load()
    assert config.name == "test"
    assert config.version == 1.0


def test_config_loader_uses_workspace_root_fallback(tmp_path: Path):
    config_dir = tmp_path / "aeos" / "config"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "aeos.config.yaml"
    config_file.write_text("aeos:\n  name: fallback\n  version: 1.0\n  mode: development\nregistries:\n  skills: aeos/registries")

    loader = ConfigLoader(workspace_root=str(tmp_path))
    config = loader.load()
    assert config.name == "fallback"


def test_config_loader_does_not_search_target(tmp_path: Path):
    target = tmp_path / "target-project"
    target.mkdir()
    aeos_root = tmp_path / "aeos-install"
    aeos_root.mkdir()
    config_dir = aeos_root / "aeos" / "config"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "aeos.config.yaml"
    config_file.write_text("aeos:\n  name: aeos\n  version: 1.0\n  mode: development\nregistries:\n  skills: aeos/registries")

    loader = ConfigLoader(workspace_root=str(target), aeos_root=str(aeos_root))
    config = loader.load()
    assert config.name == "aeos"
    assert (target / "aeos" / "config" / "aeos.config.yaml").exists() is False
