"""Gate 7: Continual Learning — replay buffer, versioning, regression gate, adapter isolation."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

CL_TERMS = {
    "continual_learning", "continual learning", "replay", "buffer",
    "experience_replay", "elastic_weight", "ewc", "si", "synaptic",
    "intelligence", "progressive", "lwf", "icarl",
}

VERSIONING_TERMS = {"version", "registry", "model_registry", "dataset_registry"}
ADAPTER_TERMS = {"adapter", "lora", "qlora", "dora", "lorahub"}


def check_continual_learning(repository: str) -> GateResult:
    """Gate 7: Audit continual learning infrastructure."""
    gate = GateResult(
        id="continual_learning",
        title="Continual Learning",
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

    cl_files = []
    versioning_files = []
    adapter_files = []

    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in text for t in CL_TERMS):
            cl_files.append(rel)
        if any(t in text for t in VERSIONING_TERMS):
            versioning_files.append(rel)
        if any(t in text for t in ADAPTER_TERMS):
            adapter_files.append(rel)

    gate.metrics["cl_files"] = len(cl_files)
    gate.metrics["versioning_files"] = len(versioning_files)
    gate.metrics["adapter_files"] = len(adapter_files)

    if not cl_files and not adapter_files:
        gate.status = AuditStatus.NOT_APPLICABLE
        gate.findings.append("No continual learning implementation detected")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    issues = []

    if not cl_files:
        gate.findings.append("Continual learning files not found")
        issues.append("missing_cl_implementation")
    elif versioning_files:
        gate.findings.append("Continual learning detected — checking versioning and replay buffer")
    else:
        gate.findings.append("CL implementation found but no versioning/registry detected")
        issues.append("missing_versioning")

    if adapter_files:
        gate.findings.append(f"Adapter-based learning detected ({len(adapter_files)} files)")
        gate.metrics["adapter_isolation"] = True
    else:
        gate.findings.append("No adapter isolation mechanism detected")
        issues.append("missing_adapter_isolation")

    # Check for regression gate
    regression_found = any("regression" in Path(f).stem.lower() for f in cl_files) if cl_files else False
    gate.metrics["regression_gate"] = regression_found
    if not regression_found:
        gate.findings.append("No regression gate detected for continual learning")
        issues.append("missing_regression_gate")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Implement replay buffer for experience rehearsal",
            "Add versioned model and dataset registries",
            "Implement adapter isolation for safe updates",
            "Add regression gate to prevent catastrophic forgetting",
            "Implement approval gate before model promotion",
        ]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
