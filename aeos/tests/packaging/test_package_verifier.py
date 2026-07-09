import pytest
import json
import zipfile
import hashlib
from pathlib import Path
from aeos.core.packaging.package_verifier import PackageVerifier


class TestPackageVerifier:
    def _create_valid_zip(self, tmp_path: Path) -> Path:
        pkg_path = tmp_path / "test-package.zip"
        manifest = {
            "package_id": "test",
            "execution_id": "exec-001",
            "created_at": "2025-01-01T00:00:00",
            "total_files": 1,
            "total_size_bytes": 15,
            "manifest_sha256": "abc123",
            "files": [{"path": "test.txt", "size": 15, "sha256": "abc"}],
        }
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps(manifest))
            zf.writestr("test.txt", "Hello, World!\n")
        return pkg_path

    def test_verify_valid_package(self, tmp_path: Path):
        pkg_path = self._create_valid_zip(tmp_path)
        result = PackageVerifier.verify(pkg_path)
        assert result.verified
        assert result.manifest_present
        assert result.checksum_match
        assert not result.path_traversal_detected
        assert not result.absolute_path_detected
        assert not result.git_dir_detected
        assert not result.secrets_detected

    def test_verify_missing_file(self, tmp_path: Path):
        result = PackageVerifier.verify(tmp_path / "nonexistent.zip")
        assert not result.verified
        assert "not found" in result.errors[0]

    def test_block_path_traversal(self, tmp_path: Path):
        pkg_path = tmp_path / "traversal.zip"
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
            zf.writestr("../outside.txt", "malicious")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert result.path_traversal_detected

    def test_block_absolute_path(self, tmp_path: Path):
        pkg_path = tmp_path / "absolute.zip"
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
            zf.writestr("/etc/passwd", "malicious")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert result.absolute_path_detected

    def test_block_git_dir(self, tmp_path: Path):
        pkg_path = tmp_path / "git.zip"
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
            zf.writestr(".git/config", "malicious")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert result.git_dir_detected

    def test_block_hash_mismatch(self, tmp_path: Path):
        pkg_path = tmp_path / "hash_mismatch.zip"
        manifest = {
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            "files": [],
        }
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps(manifest))
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert not result.checksum_match

    def test_block_bad_zip(self, tmp_path: Path):
        pkg_path = tmp_path / "bad.zip"
        pkg_path.write_bytes(b"not a zip file")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified

    def test_block_secrets(self, tmp_path: Path):
        pkg_path = tmp_path / "secrets.zip"
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
            zf.writestr("config.txt", "api_key = sk-1234567890abcdef")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert result.secrets_detected

    def test_block_without_manifest(self, tmp_path: Path):
        pkg_path = tmp_path / "no_manifest.zip"
        with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("some_file.txt", "data")
        result = PackageVerifier.verify(pkg_path)
        assert not result.verified
        assert not result.manifest_present
        assert "Missing package-manifest.json" in result.errors
