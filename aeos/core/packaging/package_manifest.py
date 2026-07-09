import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from aeos.core.packaging.package_models import PackageManifest


class PackageManifestHandler:

    MANIFEST_FILENAME = "package-manifest.json"

    @staticmethod
    def create_manifest(execution_id: str, files: list[dict]) -> PackageManifest:
        total_size = sum(f.get("size", 0) for f in files)
        manifest = PackageManifest(
            package_id=f"pkg-{execution_id}",
            execution_id=execution_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            total_files=len(files),
            total_size_bytes=total_size,
            files=files,
        )
        serialized = json.dumps(manifest.__dict__, sort_keys=True, default=str)
        manifest.manifest_sha256 = hashlib.sha256(serialized.encode()).hexdigest()
        return manifest

    @staticmethod
    def write_manifest(manifest: PackageManifest, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / PackageManifestHandler.MANIFEST_FILENAME
        data = manifest.__dict__.copy()
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return manifest_path

    @staticmethod
    def read_manifest(manifest_path: Path) -> Optional[PackageManifest]:
        if not manifest_path.exists():
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PackageManifest(**data)

    @staticmethod
    def compute_manifest_hash(manifest_path: Path) -> Optional[str]:
        if not manifest_path.exists():
            return None
        with open(manifest_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()