"""Legacy models — maintained for backward compatibility.

New code should import from `medical_research_mcp.audit.models`.
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Status(str, Enum):
    PASS = "PASS"
    BLOCKED = "BLOCKED"
    REWORK_REQUIRED = "REWORK_REQUIRED"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    UNVERIFIED = "UNVERIFIED"


class EvidenceRecord(BaseModel):
    id: str
    source: str
    source_type: str
    retrieved_at: str
    title: str
    claim: str | None = None
    identifiers: dict[str, str] = Field(default_factory=dict)
    provenance: list[str] = Field(default_factory=list)
    disease: list[str] = Field(default_factory=list)
    subgroups: list[str] = Field(default_factory=list)
    comorbidities: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    status: Literal["RAW", "SCREENED", "EXTRACTED", "VALIDATED", "REJECTED", "SUPERSEDED"] = "RAW"


class DiseaseProfile(BaseModel):
    disease: str
    aliases: list[str] = Field(default_factory=list)
    subgroups: list[str] = Field(default_factory=list)
    comorbidities: list[str] = Field(default_factory=list)
    biomarkers: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    intervention_classes: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    id: str
    category: str
    severity: Severity
    summary: str
    evidence: list[str] = Field(default_factory=list)
    remediation: str | None = None
    blocking: bool = False


class AuditResult(BaseModel):
    target: str
    status: Status
    score: float = Field(ge=0, le=10)
    findings: list[Finding] = Field(default_factory=list)
    evidence: dict[str, Any] = Field(default_factory=dict)


class ValidationCriterion(BaseModel):
    id: str
    name: str
    weight: float = Field(gt=0)
    mandatory: bool = True
    passed: bool = False
    evidence: list[str] = Field(default_factory=list)
    reason: str | None = None


class ValidationReport(BaseModel):
    score: float = Field(ge=0, le=10)
    accepted: bool
    status: Status
    criteria: list[ValidationCriterion]
    blocking_reasons: list[str] = Field(default_factory=list)
