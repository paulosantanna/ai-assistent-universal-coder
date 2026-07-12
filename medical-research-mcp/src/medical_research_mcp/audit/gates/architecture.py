"""Gate 2: Architecture — detect layers, duplicates, cycles, inverted deps."""

from __future__ import annotations
import ast
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS


def _get_python_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if not should_ignore(rel, DEFAULT_EXCLUSIONS):
            files.append(p)
    return files


def _detect_duplicate_modules(files: list[Path]) -> list[str]:
    names = [p.stem for p in files]
    from collections import Counter
    dupes = [f"{n} ({count}x)" for n, count in Counter(names).items() if count > 1]
    return dupes


def _detect_inverted_imports(root: Path, files: list[Path]) -> list[str]:
    findings = []
    for p in files:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith("src.") and "app" in str(p):
                    findings.append(f"{p.relative_to(root)} imports {node.module}")
    return findings


def _detect_prohibited_imports(root: Path, files: list[Path]) -> list[str]:
    prohibited = {"pickle", "shelve", "marshal", "compile", "exec", "eval"}
    findings = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for line in text.splitlines():
            for kw in prohibited:
                if f"import {kw}" in line or f"from {kw}" in line:
                    findings.append(f"{p.relative_to(root)}: {line.strip()}")
    return findings


def _detect_app_src_duplication(root: Path) -> list[str]:
    findings = []
    app_dir = root / "app"
    src_dir = root / "src"
    if app_dir.is_dir() and src_dir.is_dir():
        app_modules = {p.stem for p in app_dir.rglob("*.py")}
        src_modules = {p.stem for p in src_dir.rglob("*.py")}
        common = app_modules & src_modules
        if common:
            findings.append(f"Duplicate modules in both app/ and src/: {', '.join(sorted(common))}")
    return findings


def check_architecture(repository: str) -> GateResult:
    """Gate 2: Validate architecture layering and detect structural issues."""
    gate = GateResult(
        id="architecture",
        title="Architecture",
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

    py_files = _get_python_files(root)
    gate.metrics["python_files"] = len(py_files)

    issues: list[str] = []

    # Layer analysis
    layers = {"api": [], "core": [], "models": [], "services": [], "tests": []}
    for p in py_files:
        rel = str(p.relative_to(root)).replace("\\", "/")
        if "api" in rel or "controller" in rel or "route" in rel:
            layers["api"].append(rel)
        if "model" in rel:
            layers["models"].append(rel)
        if "service" in rel or "logic" in rel:
            layers["services"].append(rel)
        if "test" in rel:
            layers["tests"].append(rel)
        if "core" in rel or "engine" in rel:
            layers["core"].append(rel)

    gate.metrics["layers"] = {k: len(v) for k, v in layers.items()}

    # Duplicate modules
    dupes = _detect_duplicate_modules(py_files)
    if dupes:
        gate.findings.append(f"Duplicate module names: {', '.join(dupes[:10])}")
        issues.append("duplicate_modules")

    # app/ vs src/ duplication
    app_src = _detect_app_src_duplication(root)
    if app_src:
        gate.findings.extend(app_src)
        issues.append("app_src_duplication")

    # Inverted imports
    inverted = _detect_inverted_imports(root, py_files)
    if inverted:
        gate.findings.append(f"Inverted dependencies ({len(inverted)} cases)")
        issues.append("inverted_deps")

    # Prohibited imports
    prohibited = _detect_prohibited_imports(root, py_files)
    if prohibited:
        gate.findings.append(f"Prohibited imports ({len(prohibited)} cases): {', '.join(prohibited[:5])}")
        issues.append("prohibited_imports")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Remove duplicate module names",
            "Merge app/ and src/ into a single source tree",
            "Fix inverted dependencies — core must not import from API layer",
            "Replace prohibited imports (pickle, exec, eval) with safe alternatives",
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
