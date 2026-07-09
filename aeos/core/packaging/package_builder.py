import json
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from aeos.core.evidence.evidence_manifest import is_finalized, FINALIZED_MARKER
from aeos.core.packaging.package_models import (
    PackageBuildRequest, PackageBuildResult, PackageStatus, PackageManifest,
)
from aeos.core.packaging.package_manifest import PackageManifestHandler
from aeos.core.packaging.package_policy import PackagePolicy


class PackageBuilder:

    EVIDENCE_DIR = ".aeos/evidence"
    REPORTS_DIR = ".aeos/reports"
    PACKAGES_DIR = ".aeos/packages"

    def __init__(self, workspace_root: str | Path):
        self.workspace_root = Path(workspace_root).resolve()

    def create_package(self, request: PackageBuildRequest) -> PackageBuildResult:
        execution_dir = self.workspace_root / self.EVIDENCE_DIR / request.execution_id
        if not execution_dir.exists():
            return PackageBuildResult(
                package_path="",
                manifest=PackageManifest(execution_id=request.execution_id, package_id="", created_at=""),
                status=PackageStatus.FAILED,
                error=f"Execution directory not found: {execution_dir}",
            )

        if not is_finalized(execution_dir):
            return PackageBuildResult(
                package_path="",
                manifest=PackageManifest(execution_id=request.execution_id, package_id="", created_at=""),
                status=PackageStatus.FAILED,
                error=f"Execution {request.execution_id} is not finalized (no .finalized marker). "
                      "Run 'judge run --execution-id <id>' first to finalize evidence.",
            )

        output_dir = self.workspace_root / request.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        package_name = f"aeos-package-{request.execution_id}.zip"
        package_path = output_dir / package_name

        files_to_include: list[Path] = []
        file_entries: list[dict] = []

        if request.include_evidence:
            for f in sorted(execution_dir.rglob("*")):
                if f.is_file() and f.name != FINALIZED_MARKER:
                    files_to_include.append(f)

        reports_dir = self.workspace_root / self.REPORTS_DIR
        if request.include_reports and reports_dir.exists():
            for f in sorted(reports_dir.rglob("*")):
                if f.is_file():
                    files_to_include.append(f)

        judge_result_dir = execution_dir / "judge-result"
        if request.include_judge and judge_result_dir.exists():
            for f in sorted(judge_result_dir.rglob("*")):
                if f.is_file() and f not in files_to_include:
                    files_to_include.append(f)

        eval_scorecard = execution_dir / "eval-scorecard.json"
        if request.include_evals and eval_scorecard.exists():
            if eval_scorecard not in files_to_include:
                files_to_include.append(eval_scorecard)

        readiness_scorecard = execution_dir / "production-readiness-scorecard.json"
        if request.include_readiness and readiness_scorecard.exists():
            if readiness_scorecard not in files_to_include:
                files_to_include.append(readiness_scorecard)

        for f in files_to_include:
            rel_path = f.relative_to(self.workspace_root)
            file_entries.append({
                "path": str(rel_path.as_posix()),
                "size": f.stat().st_size,
                "sha256": self._hash_file(f),
            })

        manifest = PackageManifestHandler.create_manifest(request.execution_id, file_entries)
        manifest_path = PackageManifestHandler.write_manifest(manifest, output_dir)

        file_entries.append({
            "path": PackageManifestHandler.MANIFEST_FILENAME,
            "size": manifest_path.stat().st_size,
            "sha256": manifest.manifest_sha256,
        })

        package_path = self._build_zip(package_path, files_to_include, manifest_path)
        manifest.sha256 = self._hash_file(package_path)
        PackageManifestHandler.write_manifest(manifest, output_dir)

        manifest_path.unlink()

        return PackageBuildResult(
            package_path=str(package_path),
            manifest=manifest,
            status=PackageStatus.BUILDING,
        )

    def _build_zip(self, package_path: Path, files: list[Path], manifest_path: Path) -> Path:
        import zipfile
        with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(manifest_path, PackageManifestHandler.MANIFEST_FILENAME)
            for f in files:
                rel_path = f.relative_to(self.workspace_root)
                zf.write(f, str(rel_path.as_posix()))
        return package_path

    def _hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()