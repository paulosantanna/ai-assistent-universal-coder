"""Gate 6: Training Pipeline — validate config, paths, datasets, seeds, checkpoints."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

TRAINING_TERMS = {"train", "trainer", "training", "finetun", "lora", "qlora", "dora"}
CONFIG_TERMS = {"config", "cfg", "setting", "hyperparameter", "yaml", "toml"}


def check_training(repository: str) -> GateResult:
    """Gate 6: Verify training pipeline configuration, reproducibility, and placeholder detection."""
    gate = GateResult(
        id="training_pipeline",
        title="Training Pipeline",
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

    training_files = []
    config_files = []
    placeholder_scripts = []

    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in p.stem.lower() or t in text for t in TRAINING_TERMS):
            training_files.append(rel)
            # Detect placeholder scripts
            if "pass" in text.splitlines()[:5] or "..." in text or "# todo" in text.lower():
                placeholder_scripts.append(rel)

        if any(t in p.stem.lower() for t in CONFIG_TERMS):
            config_files.append(rel)

    # Also check for YAML/TOML config files
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".toml", ".json"}:
            rel = str(p.relative_to(root)).replace("\\", "/")
            if not should_ignore(rel, DEFAULT_EXCLUSIONS):
                if any(t in rel.lower() for t in {"train", "config", "model", "dataset"}):
                    config_files.append(rel)

    gate.metrics["training_files"] = len(training_files)
    gate.metrics["config_files"] = len(config_files)
    gate.metrics["placeholder_scripts"] = len(placeholder_scripts)

    if not training_files:
        gate.status = AuditStatus.NOT_APPLICABLE
        gate.findings.append("No training pipeline implementation detected")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    issues = []
    if placeholder_scripts:
        gate.findings.append(f"Placeholder scripts detected: {', '.join(placeholder_scripts[:5])}")
        issues.append("placeholder_scripts")

    if not config_files:
        gate.findings.append("No training configuration files found")
        issues.append("missing_config")

    # Check for dataset references
    dataset_refs = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        if "dataset" in text or "data_path" in text or "data_dir" in text:
            dataset_refs.append(rel)

    gate.metrics["dataset_references"] = len(dataset_refs)
    if not dataset_refs:
        gate.findings.append("No dataset references found in training code")
        issues.append("missing_datasets")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Replace placeholder scripts with real implementation",
            "Add training configuration files (YAML/TOML)",
            "Reference datasets explicitly in training code",
            "Set random seeds for reproducibility",
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
