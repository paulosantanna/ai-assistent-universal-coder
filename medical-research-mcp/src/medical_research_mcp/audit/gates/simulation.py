"""Gate 8: Simulation — verify boundary between computational hypothesis and clinical evidence."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

SIMULATION_TERMS = {
    "simulation", "simulator", "causal", "molecular_dynamics",
    "virtual_screening", "docking", "md_simulation",
}

DANGEROUS_CLAIMS = {
    "cure", "curar", "cura", "proven", "comprovadamente",
    "guaranteed", "garantido", "milagre", "miracle",
}

GOVERNANCE_TERMS = {"governance", "ethics", "approval", "review", "board"}


def check_simulation(repository: str) -> GateResult:
    """Gate 8: Audit simulation safety — prevent cure/efficacy claims, validate governance."""
    gate = GateResult(
        id="simulation",
        title="Simulation Safety and Governance",
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

    sim_files = []
    dangerous_claims_found = []
    governance_files = []
    file_count = 0
    MAX_FILES = 2000  # Limit to avoid timeout on large repos

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        file_count += 1
        if file_count > MAX_FILES:
            gate.limitations.append(f"File scan limited to {MAX_FILES} files for performance")
            break

        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue

        if p.suffix.lower() not in {".py", ".md", ".json", ".yaml", ".yml", ".txt", ".cfg", ".ini", ".toml"}:
            continue

        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in text for t in SIMULATION_TERMS):
            sim_files.append(rel)

        if any(t in text for t in DANGEROUS_CLAIMS):
            dangerous_claims_found.append(f"{rel}: matched dangerous claim pattern")

        if any(t in text for t in GOVERNANCE_TERMS):
            governance_files.append(rel)

    gate.metrics["simulation_files"] = len(sim_files)
    gate.metrics["dangerous_claims"] = len(dangerous_claims_found)
    gate.metrics["governance_files"] = len(governance_files)
    gate.metrics["files_scanned"] = min(file_count, MAX_FILES)

    if not sim_files:
        gate.status = AuditStatus.NOT_APPLICABLE
        gate.findings.append("No simulation code detected")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    issues = []

    if dangerous_claims_found:
        gate.findings.extend(dangerous_claims_found[:5])
        gate.status = AuditStatus.FAIL
        gate.score = 0.0
        issues.append("dangerous_claims")
        gate.remediation.append("Remove unsupported cure/efficacy claims from simulation code")
        gate.remediation.append("Add disclaimers about computational hypothesis vs clinical evidence")

    if not governance_files:
        gate.findings.append("No governance or ethics oversight detected for simulation")
        issues.append("missing_governance")
        gate.remediation.append("Add ethics/governance review for simulation experiments")

    if not issues:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.findings.append(f"Simulation implementation found ({len(sim_files)} files) — no dangerous claims")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
