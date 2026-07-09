import pytest
import json
import zipfile
from pathlib import Path
from aeos.core.packaging.package_builder import PackageBuilder
from aeos.core.packaging.package_models import PackageBuildRequest, PackageStatus
from aeos.core.evidence.evidence_manifest import mark_finalized


class TestPackageBuilder:
    def test_create_package_creates_zip(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "runtime-request.jsonl").write_text('{"test": true}')
        (exec_dir / "judge-result.json").write_text(json.dumps({"status": "PASS", "score": 0.95}))
        mark_finalized(exec_dir)

        builder = PackageBuilder(workspace_root=str(tmp_path))
        request = PackageBuildRequest(execution_id="exec-001")
        result = builder.create_package(request)

        assert result.status == PackageStatus.BUILDING
        assert result.package_path is not None
        pkg_path = Path(result.package_path)
        assert pkg_path.exists()
        assert pkg_path.suffix == ".zip"

    def test_create_package_missing_execution(self, tmp_path: Path):
        builder = PackageBuilder(workspace_root=str(tmp_path))
        request = PackageBuildRequest(execution_id="nonexistent")
        result = builder.create_package(request)
        assert result.status == PackageStatus.FAILED
        assert "not found" in (result.error or "")

    def test_package_contains_manifest(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "runtime-request.jsonl").write_text('{"test": true}')
        mark_finalized(exec_dir)

        builder = PackageBuilder(workspace_root=str(tmp_path))
        request = PackageBuildRequest(execution_id="exec-001")
        result = builder.create_package(request)

        with zipfile.ZipFile(result.package_path, "r") as zf:
            names = zf.namelist()
            assert "package-manifest.json" in names

    def test_package_contains_evidence_files(self, tmp_path: Path):
        exec_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        exec_dir.mkdir(parents=True, exist_ok=True)
        (exec_dir / "runtime-request.jsonl").write_text('{"test": true}')
        subdir = exec_dir / "subdir"
        subdir.mkdir(parents=True, exist_ok=True)
        (subdir / "data.json").write_text('{"key": "val"}')
        mark_finalized(exec_dir)

        builder = PackageBuilder(workspace_root=str(tmp_path))
        request = PackageBuildRequest(execution_id="exec-001")
        result = builder.create_package(request)

        with zipfile.ZipFile(result.package_path, "r") as zf:
            names = zf.namelist()
            evidence_files = [n for n in names if "runtime-request.jsonl" in n or "data.json" in n]
            assert len(evidence_files) > 0
