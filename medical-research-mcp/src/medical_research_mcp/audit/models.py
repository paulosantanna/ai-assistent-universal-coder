"""Data models for the Medical AI Audit V2 framework."""

from __future__ import annotations
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class AuditStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_EXECUTED = "NOT_EXECUTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceType(str, Enum):
    COMMAND_OUTPUT = "command_output"
    FILE_HASH = "file_hash"
    TEST_REPORT = "test_report"
    SOURCE_CODE = "source_code"
    METRIC = "metric"
    ARTIFACT = "artifact"


class EvidenceItem(BaseModel):
    type: EvidenceType
    source: str
    sha256: str
    summary: str
    verified: bool = True


class CommandRecord(BaseModel):
    command: str
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    truncated: bool = False
    duration_ms: float = 0.0
    timed_out: bool = False


class GateResult(BaseModel):
    id: str
    title: str
    critical: bool = True
    status: AuditStatus = AuditStatus.NOT_EXECUTED
    score: float | None = None
    weight: float = 1.0
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: float = 0.0
    commands: list[CommandRecord] = Field(default_factory=list)
    evidence: list[EvidenceItem | dict] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    findings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    remediation: list[str] = Field(default_factory=list)
    blocked_by: list[str] = Field(default_factory=list)


class AuditConfig(BaseModel):
    repository: str
    mode: str = "structural"
    timeout_seconds: int = 900
    run_tests: bool = True
    run_security: bool = True
    run_dependency_audit: bool = True
    read_only: bool = True
    max_output_chars: int = 50000
    verbosity: str = "normal"
    extra_exclusions: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    target: str
    mode: str
    started_at: str
    finished_at: str
    duration_ms: float
    status: AuditStatus
    score: float | None = None
    coverage: float | None = None
    executed_gates: int = 0
    total_gates: int = 0
    attempted_gates: int = 0
    completed_gates: int = 0
    blocked_gates: int = 0
    critical_not_executed: list[str] = Field(default_factory=list)
    critical_blocked: list[str] = Field(default_factory=list)
    gates: dict[str, GateResult] = Field(default_factory=dict)
    executive_summary: str = ""
    findings: list[str] = Field(default_factory=list)
    report_path: str | None = None
    report_sha256: str | None = None
    limitations: list[str] = Field(default_factory=list)


class JudgeVerdict(BaseModel):
    accepted: bool
    original_score: float | None = None
    adjusted_score: float | None = None
    original_status: AuditStatus | None = None
    adjusted_status: AuditStatus | None = None
    reasons: list[str] = Field(default_factory=list)
    evidence_issues: list[str] = Field(default_factory=list)
    score_issues: list[str] = Field(default_factory=list)
    contradiction_issues: list[str] = Field(default_factory=list)
