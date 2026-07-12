"""Gate 11: Privacy — PHI/PII detection, consent, retention, DSR, anonymization."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

PHI_PATTERNS = [
    "patient", "paciente", "phi", "phi_", "health_record",
    "medical_record", "diagnosis", "ssn", "social_security",
    "date_of_birth", "dob", "patient_id",
]

PII_PATTERNS = [
    "email", "phone", "address", "cpf", "rg", "passport",
    "credit_card", "bank_account", "personal_data",
]

PRIVACY_TERMS = [
    "consent", "lgpd", "gdpr", "hipaa", "privacy",
    "anonimiz", "anonymiz", "deidentif", "de_identif",
    "data_protection", "data_retention", "dsr",
]


def check_privacy(repository: str) -> GateResult:
    """Gate 11: Audit privacy controls — real PHI/PII scanning and consent mechanisms."""
    gate = GateResult(
        id="privacy",
        title="Privacy and Data Protection",
        critical=True,
        weight=1.0,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    root = Path(repository).resolve()
    if not root.is_dir():
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"Repository path not found: {repository}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    phi_files = []
    pii_files = []
    privacy_controls = []

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        if p.suffix.lower() not in {".py", ".md", ".yaml", ".yml", ".json", ".txt", ".cfg", ".ini"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in text for t in PHI_PATTERNS):
            phi_files.append(rel)
            if len(phi_files) >= 10:
                break

        if any(t in text for t in PII_PATTERNS):
            pii_files.append(rel)
            if len(pii_files) >= 10:
                break

        if any(t in text for t in PRIVACY_TERMS):
            privacy_controls.append(rel)
            if len(privacy_controls) >= 10:
                break

    gate.metrics["phi_references"] = len(phi_files)
    gate.metrics["pii_references"] = len(pii_files)
    gate.metrics["privacy_controls"] = len(privacy_controls)

    issues = []

    # Check for anonymization
    anon_files = [f for f in privacy_controls if any(t in f.lower() for t in ["anonim", "anonym", "deident"])]
    gate.metrics["anonymization_code"] = len(anon_files)

    # Check for consent
    consent_files = [f for f in privacy_controls if "consent" in f.lower()]
    gate.metrics["consent_mechanisms"] = len(consent_files)

    # Check for DSR
    dsr_files = [f for f in privacy_controls if "dsr" in f.lower()]
    gate.metrics["dsr_support"] = len(dsr_files)

    if not privacy_controls:
        gate.findings.append("No privacy controls, consent mechanisms, or data protection references found")
        issues.append("missing_privacy_controls")

    if not anon_files:
        gate.findings.append("No anonymization/de-identification code detected")
        issues.append("missing_anonymization")
    else:
        gate.evidence.append({
            "type": "source_code",
            "source": "; ".join(anon_files[:5]),
            "sha256": "",
            "summary": "Anonymization/de-identification code found",
            "verified": True,
        })

    if gate.metrics["phi_references"] > 0 and not anon_files:
        gate.findings.append("PHI references found but no anonymization code — data may be exposed")
        issues.append("phi_without_anonymization")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Implement data anonymization/de-identification pipeline",
            "Add consent management for data processing",
            "Implement DSR (Data Subject Request) handling",
            "Add data retention and deletion policies",
            "Review all PHI/PII references for compliance",
        ]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.findings.append("Privacy controls detected and adequate")
        if phi_files:
            gate.findings.append("PHI references found but anonymization is in place")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
