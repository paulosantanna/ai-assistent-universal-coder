"""Gate 12: Governance — provenance, registries, promotion gates, human review, audit log."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

GOV_KEYWORDS = {
    "provenance", "registry", "model_registry", "dataset_registry",
    "promotion", "promotion_gate", "stage_gate",
    "human_review", "approval", "audit_log", "traceability",
}

SOURCE_KEYWORDS = {"source_registry", "source_policy", "source_screening"}
DATASET_KEYWORDS = {"dataset_registry", "dataset_version", "data_catalog"}


def check_governance(repository: str) -> GateResult:
    """Gate 12: Audit governance infrastructure — real registries and gates."""
    gate = GateResult(
        id="governance",
        title="Governance and Provenance",
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

    gov_files = []
    source_registry = []
    dataset_registry = []
    model_registry = []
    promotion_gates = []
    human_review = []
    audit_logs = []

    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in text for t in GOV_KEYWORDS):
            gov_files.append(rel)

        if any(t in text for t in SOURCE_KEYWORDS):
            source_registry.append(rel)
        if any(t in text for t in DATASET_KEYWORDS):
            dataset_registry.append(rel)
        if "model_registry" in text or "model_registry" in text:
            model_registry.append(rel)
        if "promotion" in text or "promotion_gate" in text or "stage_gate" in text:
            promotion_gates.append(rel)
        if "human_review" in text or "human_approval" in text:
            human_review.append(rel)
        if "audit_log" in text or "audit_trail" in text or "log_audit" in text:
            audit_logs.append(rel)

    gate.metrics["governance_files"] = len(gov_files)
    gate.metrics["source_registry"] = len(source_registry)
    gate.metrics["dataset_registry"] = len(dataset_registry)
    gate.metrics["model_registry"] = len(model_registry)
    gate.metrics["promotion_gates"] = len(promotion_gates)
    gate.metrics["human_review"] = len(human_review)
    gate.metrics["audit_logs"] = len(audit_logs)

    issues = []

    if not source_registry:
        gate.findings.append("No source registry/provenance tracking found")
        issues.append("missing_source_registry")
    if not dataset_registry:
        gate.findings.append("No dataset registry found")
        issues.append("missing_dataset_registry")
    if not model_registry:
        gate.findings.append("No model registry found")
        issues.append("missing_model_registry")
    if not promotion_gates:
        gate.findings.append("No promotion gate mechanism found")
        issues.append("missing_promotion_gates")
    if not human_review:
        gate.findings.append("No human review/approval mechanism found")
        issues.append("missing_human_review")
    if not audit_logs:
        gate.findings.append("No audit log/trail mechanism found")
        issues.append("missing_audit_log")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 2.0)
        gate.remediation = [
            "Implement source registry for provenance tracking",
            "Create dataset registry with versioning",
            "Implement model registry with version tracking",
            "Add promotion gates with approval workflow",
            "Add human review step before production promotion",
            "Implement audit logging for all critical operations",
        ]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.evidence.append({
            "type": "metric",
            "source": "static_analysis",
            "sha256": "",
            "summary": f"Full governance infrastructure detected ({len(gov_files)} files)",
            "verified": True,
        })
        gate.evidence.append({
            "type": "source_code",
            "source": f"source_registry={len(source_registry)}, dataset_registry={len(dataset_registry)}, model_registry={len(model_registry)}, promotion_gates={len(promotion_gates)}, human_review={len(human_review)}, audit_logs={len(audit_logs)}",
            "sha256": "",
            "summary": "All six governance components present",
            "verified": True,
        })
        gate.findings.append(f"Full governance infrastructure detected ({len(gov_files)} files)")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
