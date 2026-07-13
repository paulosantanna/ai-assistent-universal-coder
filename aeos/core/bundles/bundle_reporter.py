import os
import subprocess
from pathlib import Path
from .bundle_models import BundleManifest

def generate_report(manifest: BundleManifest, out_path: str) -> None:
    content = f"""# AEOS Bundle Report: {manifest.name}

## Metadata
- **Phase**: {manifest.phase}
- **Bundle ID**: {manifest.bundle_id}
- **Execution ID**: {manifest.execution_id}
- **Created At**: {manifest.created_at_utc}
- **SHA256**: {manifest.bundle.sha256}

## Git Status
- **Source Repository**: {manifest.source_repository}
- **Source Branch**: {manifest.source_branch}
- **Base Commit**: {manifest.base_commit}
- **Head Commit**: {manifest.head_commit}
- **Total Commits**: {manifest.commit_count}

## Files
- Added: {len(manifest.files_added)}
- Modified: {len(manifest.files_modified)}
- Deleted: {len(manifest.files_deleted)}

## Quality Gates
- **Security Scan**: {manifest.security.status}
- **Tests**: {manifest.tests.status} ({manifest.tests.passed} passed)
- **Judge**: {manifest.judge.status} ({manifest.judge.score}/10)
- **Evidence**: {manifest.evidence.status}
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_patch(target_dir: str, base_commit: str, head_commit: str, out_path: str) -> None:
    res = subprocess.run(["git", "diff", f"{base_commit}..{head_commit}"], cwd=target_dir, capture_output=True, text=True)
    if res.returncode == 0:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res.stdout)
