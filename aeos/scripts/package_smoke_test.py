#!/usr/bin/env python3
"""
AEOS Package Smoke Test
Tests package creation, verification, and security blocking.
"""
import sys
import json
import zipfile
from pathlib import Path
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def test_create_and_verify():
    tmp = Path(tempfile.mkdtemp())
    ev_dir = tmp / ".aeos" / "evidence" / "exec-pkg-smoke"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "runtime-request.jsonl").write_text('{"test": true}')
    (ev_dir / "judge-result.json").write_text(json.dumps({"status": "PASS", "score": 0.95}))

    from aeos.core.packaging.package_builder import PackageBuilder
    from aeos.core.packaging.package_models import PackageBuildRequest, PackageStatus
    from aeos.core.packaging.package_verifier import PackageVerifier

    builder = PackageBuilder(workspace_root=str(tmp))
    result = builder.create_package(PackageBuildRequest(execution_id="exec-pkg-smoke"))
    assert result.status == PackageStatus.BUILDING, f"Build failed: {result.error}"
    pkg_path = Path(result.package_path)
    assert pkg_path.exists(), "Package file not created"
    print(f"  [PASS] Package created at {pkg_path}")

    verify_result = PackageVerifier.verify(pkg_path)
    assert verify_result.verified, f"Verify failed: {verify_result.errors}"
    assert verify_result.manifest_present
    assert verify_result.checksum_match
    print("  [PASS] Package verified successfully")


def test_block_path_traversal():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "malicious.zip"
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
        zf.writestr("../../etc/passwd", "gotcha")

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert result.path_traversal_detected
    print("  [PASS] Path traversal blocked")


def test_block_absolute_path():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "absolute.zip"
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
        zf.writestr("/etc/shadow", "gotcha")

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert result.absolute_path_detected
    print("  [PASS] Absolute path blocked")


def test_block_git_dir():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "gitleak.zip"
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
        zf.writestr("src/.git/config", "leak")

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert result.git_dir_detected
    print("  [PASS] .git directory blocked")


def test_block_hash_mismatch():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "badhash.zip"
    import hashlib
    manifest = {"sha256": "0" * 64, "files": []}
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package-manifest.json", json.dumps(manifest))

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert not result.checksum_match
    print("  [PASS] Hash mismatch blocked")


def test_block_no_manifest():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "nomanifest.zip"
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("random.txt", "data")

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert not result.manifest_present
    print("  [PASS] Missing manifest blocked")


def test_block_secrets():
    tmp = Path(tempfile.mkdtemp())
    pkg_path = tmp / "secrets.zip"
    with zipfile.ZipFile(pkg_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("package-manifest.json", json.dumps({"sha256": "abc"}))
        zf.writestr(".env", "GH_TOKEN=ghp_1234567890abcdef")

    from aeos.core.packaging.package_verifier import PackageVerifier
    result = PackageVerifier.verify(pkg_path)
    assert not result.verified
    assert result.secrets_detected
    print("  [PASS] Secrets blocked")


def test_reporter():
    tmp = Path(tempfile.mkdtemp())
    from aeos.core.packaging.package_reporter import PackageReporter
    from aeos.core.packaging.package_models import PackageBuildResult, PackageManifest, PackageStatus, PackageVerifyResult

    build_result = PackageBuildResult(
        package_path=str(tmp / "test.zip"),
        manifest=PackageManifest(execution_id="exec-001", package_id="pkg-001", created_at="2025-01-01T00:00:00"),
        status=PackageStatus.VERIFIED,
    )
    report = PackageReporter.generate_build_report(build_result)
    assert "Package Build Report" in report
    print("  [PASS] Build report generated")

    verify_result = PackageVerifyResult(
        package_path=str(tmp / "test.zip"),
        verified=True,
        checksum_match=True,
        manifest_present=True,
        path_traversal_detected=False,
        absolute_path_detected=False,
        git_dir_detected=False,
        secrets_detected=False,
    )
    report = PackageReporter.generate_verify_report(verify_result)
    assert "Package Verification Report" in report
    print("  [PASS] Verify report generated")


def main():
    print("=" * 60)
    print("AEOS Package Smoke Test")
    print("=" * 60)
    failures = 0
    tests = [
        ("create_and_verify", test_create_and_verify),
        ("block_path_traversal", test_block_path_traversal),
        ("block_absolute_path", test_block_absolute_path),
        ("block_git_dir", test_block_git_dir),
        ("block_hash_mismatch", test_block_hash_mismatch),
        ("block_no_manifest", test_block_no_manifest),
        ("block_secrets", test_block_secrets),
        ("reporter", test_reporter),
    ]
    for name, fn in tests:
        try:
            fn()
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            import traceback
            traceback.print_exc()
            failures += 1
    print()
    if failures == 0:
        print(f"PACKAGE SMOKE TEST PASSED ({len(tests)}/{len(tests)})")
        return 0
    else:
        print(f"PACKAGE SMOKE TEST FAILED ({len(tests)-failures}/{len(tests)} failures={failures})")
        return 1


if __name__ == "__main__":
    sys.exit(main())