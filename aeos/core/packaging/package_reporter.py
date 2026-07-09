from datetime import datetime, timezone
from pathlib import Path
from aeos.core.packaging.package_models import PackageManifest, PackageBuildResult, PackageVerifyResult


class PackageReporter:

    @staticmethod
    def generate_build_report(result: PackageBuildResult) -> str:
        lines = [
            "# AEOS Package Build Report",
            "",
            f"- **Package**: {result.package_path}",
            f"- **Status**: {result.status.value}",
            f"- **Execution ID**: {result.manifest.execution_id}",
            f"- **Total Files**: {result.manifest.total_files}",
            f"- **Total Size**: {result.manifest.total_size_bytes} bytes",
            f"- **SHA256**: {result.manifest.sha256}",
            f"- **Manifest SHA256**: {result.manifest.manifest_sha256}",
            f"- **Timestamp**: {datetime.now(timezone.utc).isoformat()}",
        ]
        if result.error:
            lines.extend(["", "## Errors", "", result.error])
        return "\n".join(lines)

    @staticmethod
    def generate_verify_report(result: PackageVerifyResult) -> str:
        status = "PASS" if result.verified else "FAIL"
        lines = [
            "# AEOS Package Verification Report",
            "",
            f"- **Package**: {result.package_path}",
            f"- **Verified**: {status}",
            f"- **Manifest Present**: {result.manifest_present}",
            f"- **Checksum Match**: {result.checksum_match}",
            f"- **Path Traversal**: {result.path_traversal_detected}",
            f"- **Absolute Path**: {result.absolute_path_detected}",
            f"- **Git Dir**: {result.git_dir_detected}",
            f"- **Secrets**: {result.secrets_detected}",
            f"- **Timestamp**: {datetime.now(timezone.utc).isoformat()}",
        ]
        if result.errors:
            lines.extend(["", "## Errors", ""])
            for e in result.errors:
                lines.append(f"- {e}")
        return "\n".join(lines)