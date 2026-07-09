import json
import re
import zipfile
import hashlib
from pathlib import Path
from typing import Optional
from aeos.core.packaging.package_models import PackageVerifyResult, PackageManifest
from aeos.core.packaging.package_manifest import PackageManifestHandler
from aeos.core.packaging.package_policy import PackagePolicy


SECRET_PATTERNS: list[bytes | re.Pattern] = [
    re.compile(rb'(?<![a-zA-Z])sk-[A-Za-z0-9]{10,}'),
    b"ghp_", b"gho_", b"ghu_", b"ghs_",
    b"xoxb-", b"xapp-", b"AKIA", b"-----BEGIN RSA PRIVATE KEY-----",
]


class PackageVerifier:

    @staticmethod
    def verify(package_path: str | Path) -> PackageVerifyResult:
        pkg_path = Path(package_path)
        if not pkg_path.exists():
            return PackageVerifyResult(
                package_path=str(pkg_path),
                verified=False,
                checksum_match=False,
                manifest_present=False,
                path_traversal_detected=False,
                absolute_path_detected=False,
                git_dir_detected=False,
                secrets_detected=False,
                errors=[f"Package not found: {pkg_path}"],
            )

        errors: list[str] = []
        path_traversal = False
        absolute_path = False
        git_dir = False
        secrets = False
        manifest_present = False
        manifest_data: Optional[dict] = None

        try:
            with zipfile.ZipFile(pkg_path, "r") as zf:
                names = zf.namelist()

                if PackageManifestHandler.MANIFEST_FILENAME in names:
                    manifest_present = True
                    with zf.open(PackageManifestHandler.MANIFEST_FILENAME) as mf:
                        manifest_data = json.loads(mf.read().decode("utf-8"))
                else:
                    errors.append("Missing package-manifest.json")

                for name in names:
                    if ".." in name or name.startswith("/"):
                        path_traversal = True
                        errors.append(f"Path traversal detected: {name}")
                    if name.startswith("/") or name.startswith("\\"):
                        absolute_path = True
                        errors.append(f"Absolute path detected: {name}")
                    if ".git" in name.split("/"):
                        git_dir = True
                        errors.append(f".git directory included: {name}")

                    if not secrets:
                        info = zf.getinfo(name)
                        if info.file_size > 0 and info.file_size < 10 * 1024 * 1024:
                            content = zf.read(name)
                            for pattern in SECRET_PATTERNS:
                                if isinstance(pattern, re.Pattern):
                                    if pattern.search(content):
                                        secrets = True
                                        errors.append(f"Secret pattern detected in: {name}")
                                        break
                                elif isinstance(pattern, bytes):
                                    if pattern in content:
                                        secrets = True
                                        errors.append(f"Secret pattern detected in: {name}")
                                        break

        except zipfile.BadZipFile:
            return PackageVerifyResult(
                package_path=str(pkg_path),
                verified=False,
                checksum_match=False,
                manifest_present=manifest_present,
                path_traversal_detected=path_traversal,
                absolute_path_detected=absolute_path,
                git_dir_detected=git_dir,
                secrets_detected=secrets,
                errors=["Bad ZIP file"],
            )

        checksum_match = True
        if manifest_data and manifest_data.get("sha256"):
            file_hash = PackageVerifier._hash_file(pkg_path)
            checksum_match = file_hash == manifest_data["sha256"]
            if not checksum_match:
                errors.append("SHA256 hash mismatch between package and manifest")

        verified = (
            manifest_present
            and checksum_match
            and not path_traversal
            and not absolute_path
            and not git_dir
            and not secrets
            and len(errors) == 0
        )

        if not verified and not errors:
            errors.append("Package verification failed")

        return PackageVerifyResult(
            package_path=str(pkg_path),
            verified=verified,
            checksum_match=checksum_match,
            manifest_present=manifest_present,
            path_traversal_detected=path_traversal,
            absolute_path_detected=absolute_path,
            git_dir_detected=git_dir,
            secrets_detected=secrets,
            errors=errors,
        )

    @staticmethod
    def _hash_file(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()