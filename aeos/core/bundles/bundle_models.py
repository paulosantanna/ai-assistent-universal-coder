from pydantic import BaseModel, Field
from typing import List, Optional

class BundleTests(BaseModel):
    command: str = ""
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    status: str = "BLOCKED"

class BundleJudge(BaseModel):
    status: str = "BLOCKED"
    score: float = 0.0
    evidence_ref: str = ""

class BundleEvidence(BaseModel):
    status: str = "BLOCKED"
    manifest_hash: str = ""

class BundleSecurity(BaseModel):
    secret_scan: str = "FAIL"
    forbidden_files_detected: List[str] = Field(default_factory=list)
    status: str = "FAIL"

class BundleFile(BaseModel):
    filename: str = ""
    sha256: str = ""
    size_bytes: int = 0
    verified: bool = False
    heads: List[str] = Field(default_factory=list)

class BundleRollback(BaseModel):
    strategy: str = ""
    base_commit: str = ""

class BundleManifest(BaseModel):
    schema_version: str = "1.0"
    bundle_id: str = ""
    phase: str = ""
    name: str = ""
    execution_id: str = ""
    created_at_utc: str = ""
    aeos_version: str = "2.0.0"
    source_repository: str = ""
    source_branch: str = ""
    target_repository_expected: str = ""
    base_commit: str = ""
    head_commit: str = ""
    commit_count: int = 0
    commits: List[str] = Field(default_factory=list)
    files_added: List[str] = Field(default_factory=list)
    files_modified: List[str] = Field(default_factory=list)
    files_deleted: List[str] = Field(default_factory=list)
    tests: BundleTests = Field(default_factory=BundleTests)
    judge: BundleJudge = Field(default_factory=BundleJudge)
    evidence: BundleEvidence = Field(default_factory=BundleEvidence)
    security: BundleSecurity = Field(default_factory=BundleSecurity)
    bundle: BundleFile = Field(default_factory=BundleFile)
    rollback: BundleRollback = Field(default_factory=BundleRollback)
