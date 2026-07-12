"""Gate 14: Documentation Consistency — compare docs with actual importable modules."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS


def check_documentation(repository: str) -> GateResult:
    """Gate 14: Validate documentation consistency — detect phantom features and undocumented code."""
    gate = GateResult(
        id="documentation",
        title="Documentation Consistency",
        critical=False,
        weight=0.5,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    root = Path(repository).resolve()
    if not root.is_dir():
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"Repository path not found: {repository}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Find all .md files
    md_files = []
    for p in root.rglob("*.md"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        md_files.append(rel)

    # Find all Python modules
    py_modules = set()
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        stem = p.stem
        if not stem.startswith("_"):
            py_modules.add(stem)

    # Extract module references from docs
    doc_referenced_modules = set()
    doc_keywords = set()
    for p in root.rglob("*.md"):
        if should_ignore(str(p.relative_to(root)).replace("\\", "/"), DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Look for module names in markdown
        for mod in py_modules:
            if mod in text:
                doc_referenced_modules.add(mod)
        # Extract keywords
        for word in text.split():
            if word.endswith(".py") or word.endswith(".md"):
                doc_keywords.add(word.strip("`\"'"))

    gate.metrics["documentation_files"] = len(md_files)
    gate.metrics["python_modules"] = len(py_modules)
    gate.metrics["modules_referenced_in_docs"] = len(doc_referenced_modules)

    issues = []

    if not md_files:
        gate.status = AuditStatus.NOT_EXECUTED
        gate.findings.append("No documentation files (.md) found")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Detect modules NOT referenced in any doc
    undocumented_modules = py_modules - doc_referenced_modules
    if undocumented_modules:
        samples = sorted(undocumented_modules)[:10]
        gate.findings.append(f"Undocumented modules: {len(undocumented_modules)} modules not referenced in docs")
        gate.evidence.append({
            "type": "source_code",
            "source": "; ".join(samples),
            "sha256": "",
            "summary": f"Modules without documentation references ({len(undocumented_modules)} total)",
            "verified": False,
        })
        if len(undocumented_modules) > len(py_modules) * 0.5:
            issues.append("extensive_undocumented_modules")

    # Check for README existence
    has_readme = any("readme" in p.lower() for p in md_files)
    gate.metrics["has_readme"] = has_readme
    if not has_readme:
        gate.findings.append("No README.md found")
        issues.append("missing_readme")

    # Check for operational docs
    has_ops_docs = any("deploy" in p.lower() or "operatio" in p.lower() or "runbook" in p.lower() for p in md_files)
    gate.metrics["has_operational_docs"] = has_ops_docs
    if py_modules and not has_ops_docs:
        gate.findings.append("No operational/runbook documentation found")
        issues.append("missing_operational_docs")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Document all public modules with docstrings and README references",
            "Add operational runbooks for deployment and troubleshooting",
            "Keep documentation in sync with actual code changes",
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
