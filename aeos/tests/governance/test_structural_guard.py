from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "structural_guard.py"
spec = importlib.util.spec_from_file_location("structural_guard", MODULE_PATH)
structural_guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["structural_guard"] = structural_guard
spec.loader.exec_module(structural_guard)


def test_structural_guard_detects_nested_src(tmp_path: Path):
    nested = tmp_path / "src" / "src" / "pkg"
    nested.mkdir(parents=True)
    (nested / "module.py").write_text("x = 1\n", encoding="utf-8")

    findings = structural_guard.check_no_nested_src(tmp_path)

    assert [finding.code for finding in findings] == ["NESTED_SRC_FILE"]


def test_structural_guard_detects_conflict_markers(tmp_path: Path):
    (tmp_path / "bad.yaml").write_text("<<<<<<< ours\nvalue: 1\n>>>>>>> theirs\n", encoding="utf-8")

    findings = structural_guard.check_no_conflict_markers(tmp_path)

    assert {finding.code for finding in findings} == {"MERGE_CONFLICT_MARKER"}


def test_structural_guard_detects_manifest_cache_entries(tmp_path: Path):
    manifest = tmp_path / "MANIFEST.json"
    manifest.write_text(
        json.dumps({"files": [{"path": "pkg/__pycache__/module.cpython-312.pyc"}]}),
        encoding="utf-8",
    )

    findings = structural_guard.check_manifests(tmp_path)

    assert [finding.code for finding in findings] == ["MANIFEST_FORBIDDEN_ARTIFACT"]


def test_structural_guard_detects_duplicate_registry_ids(tmp_path: Path):
    registry_dir = tmp_path / "aeos" / "registries"
    registry_dir.mkdir(parents=True)
    (registry_dir / "skills.registry.yaml").write_text(
        "skills:\n"
        "  - id: duplicate\n"
        "  - id: duplicate\n",
        encoding="utf-8",
    )

    findings = structural_guard.check_registries(tmp_path)

    assert [finding.code for finding in findings] == ["DUPLICATE_REGISTRY_ID"]


def test_structural_guard_detects_tracked_ide_files(tmp_path: Path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.PIPE)
    idea = tmp_path / ".idea"
    idea.mkdir()
    (idea / "workspace.xml").write_text("<project />\n", encoding="utf-8")
    subprocess.run(["git", "add", ".idea/workspace.xml"], cwd=tmp_path, check=True)

    findings = structural_guard.check_no_tracked_ide_files(tmp_path)

    assert [finding.code for finding in findings] == ["TRACKED_IDE_FILE"]
