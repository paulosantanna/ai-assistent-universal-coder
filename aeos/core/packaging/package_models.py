from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from datetime import datetime


class PackageStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    VERIFIED = "verified"
    FAILED = "failed"
    CORRUPT = "corrupt"


@dataclass
class PackageManifest:
    package_id: str
    execution_id: str
    created_at: str
    version: str = "1.0.0"
    total_files: int = 0
    total_size_bytes: int = 0
    sha256: str = ""
    files: list[dict] = field(default_factory=list)
    manifest_sha256: str = ""


@dataclass
class PackageBuildRequest:
    execution_id: str
    output_dir: str = ".aeos/packages"
    include_evidence: bool = True
    include_reports: bool = True
    include_judge: bool = True
    include_evals: bool = True
    include_readiness: bool = True


@dataclass
class PackageBuildResult:
    package_path: str
    manifest: PackageManifest
    status: PackageStatus
    error: Optional[str] = None


@dataclass
class PackageVerifyResult:
    package_path: str
    verified: bool
    checksum_match: bool
    manifest_present: bool
    path_traversal_detected: bool
    absolute_path_detected: bool
    git_dir_detected: bool
    secrets_detected: bool
    errors: list[str] = field(default_factory=list)