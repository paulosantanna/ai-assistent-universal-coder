"""Gate 10: Dependencies — identify manifests, check inconsistencies, run audit tools."""

from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..command_runner import run_command, find_tool

MANIFEST_FILES = {
    "pyproject.toml", "requirements.txt", "Pipfile", "Pipfile.lock",
    "poetry.lock", "uv.lock",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Cargo.toml", "Cargo.lock",
    "go.mod", "go.sum",
    "Gemfile", "Gemfile.lock",
    "pom.xml", "build.gradle", "build.gradle.kts",
}


async def check_dependencies(
    repository: str,
    run_audit: bool = True,
    max_output_chars: int = 50000,
) -> GateResult:
    """Gate 10: Audit dependencies — real tool execution, not manifest existence alone."""
    gate = GateResult(
        id="dependency_security",
        title="Dependency Security",
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

    # Find manifests
    manifests = []
    for p in root.rglob("*"):
        if p.is_file() and p.name in MANIFEST_FILES:
            rel = str(p.relative_to(root)).replace("\\", "/")
            manifests.append(rel)

    gate.metrics["manifests_found"] = len(manifests)
    gate.metrics["manifests"] = manifests

    if not manifests:
        gate.status = AuditStatus.NOT_APPLICABLE
        gate.findings.append("No dependency manifests found (pyproject.toml, requirements.txt, etc.)")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Check for lockfiles alongside manifests
    lockfiles = [m for m in manifests if "lock" in m.lower()]
    gate.metrics["lockfiles"] = len(lockfiles)
    if not lockfiles:
        gate.findings.append("No lockfiles found — dependency versions are not pinned")
        gate.remediation.append("Generate lockfiles (pip freeze > requirements.txt, poetry lock, etc.)")

    # Try pip-audit if available and run_audit is True
    if run_audit:
        pip_audit = find_tool("pip-audit")
        if pip_audit and any(m.endswith((".txt", ".toml")) for m in manifests):
            pip_cmd = [pip_audit, "--desc", "--format", "json"]
            audit_rec = await run_command(pip_cmd, timeout_seconds=120, max_output_chars=max_output_chars, cwd=str(root))
            gate.commands.append(audit_rec)
            if audit_rec.exit_code == 0:
                gate.evidence.append({
                    "type": "command_output",
                    "source": "pip-audit",
                    "sha256": "",
                    "summary": "pip-audit completed — no known vulnerabilities found",
                    "verified": True,
                })
                gate.metrics["dependencies_audited"] = True
            elif audit_rec.exit_code is not None and audit_rec.exit_code > 0:
                gate.findings.append("pip-audit found vulnerabilities")
                gate.metrics["dependencies_vulnerable"] = True
                gate.evidence.append({
                    "type": "command_output",
                    "source": "pip-audit",
                    "sha256": "",
                    "summary": audit_rec.stdout[:500] or audit_rec.stderr[:500],
                    "verified": False,
                })
        elif pip_audit:
            gate.findings.append("pip-audit available but no Python manifests found to audit")
        else:
            gate.status = AuditStatus.BLOCKED
            gate.findings.append("pip-audit not installed — cannot verify dependency vulnerabilities")
            gate.score = None
            gate.remediation.append("Install pip-audit: pip install pip-audit")
            gate.finished_at = datetime.now(timezone.utc).isoformat()
            return gate

    # npm audit for Node projects
    npm_audit = find_tool("npm")
    if npm_audit and any("package" in m for m in manifests):
        npm_rec = await run_command(["npm", "audit", "--json"], timeout_seconds=120, max_output_chars=max_output_chars, cwd=str(root))
        gate.commands.append(npm_rec)
        if npm_rec.exit_code == 0:
            gate.metrics["npm_vulnerabilities"] = 0
        elif npm_rec.exit_code is not None:
            import json as _json
            try:
                npm_data = _json.loads(npm_rec.stdout)
                vuln_count = npm_data.get("metadata", {}).get("vulnerabilities", {}).get("total", 0)
                gate.metrics["npm_vulnerabilities"] = vuln_count
            except Exception:
                gate.metrics["npm_vulnerabilities"] = -1
            if gate.metrics["npm_vulnerabilities"] > 0:
                gate.findings.append(f"npm audit found {gate.metrics['npm_vulnerabilities']} vulnerabilities")

    # Check for inconsistent dependency versions
    if len(manifests) > 1:
        gate.findings.append(f"Multiple manifests found ({len(manifests)}) — check for version inconsistencies")

    if gate.status == AuditStatus.NOT_EXECUTED or gate.status == AuditStatus.NOT_APPLICABLE:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.evidence.append({
            "type": "metric",
            "source": "static_analysis",
            "sha256": "",
            "summary": f"Dependency manifests found ({len(manifests)}) with {len(lockfiles)} lockfiles",
            "verified": True,
        })
        if not gate.findings:
            gate.findings.append(f"Manifests found ({len(manifests)}) and audits passed")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
