"""Evidence collection and verification utilities."""

from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any
from .models import EvidenceItem, EvidenceType, CommandRecord


def evidence_from_command(
    record: CommandRecord,
    source_label: str = "",
    summary: str = "",
) -> EvidenceItem:
    """Create an EvidenceItem from a CommandRecord."""
    content = f"exit={record.exit_code} cmd={record.command}"
    sha = hashlib.sha256(content.encode()).hexdigest()
    return EvidenceItem(
        type=EvidenceType.COMMAND_OUTPUT,
        source=source_label or record.command,
        sha256=sha,
        summary=summary or f"Exit code: {record.exit_code}",
        verified=record.exit_code == 0,
    )


def evidence_from_file_hash(file_path: str | Path, summary: str = "") -> EvidenceItem | None:
    """Create an EvidenceItem from a file's SHA-256 hash."""
    path = Path(file_path)
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return EvidenceItem(
        type=EvidenceType.FILE_HASH,
        source=str(path),
        sha256=h.hexdigest(),
        summary=summary or f"SHA-256 of {path.name}",
        verified=True,
    )


def evidence_from_metric(name: str, value: Any, summary: str = "") -> EvidenceItem:
    """Create an EvidenceItem from a metric value."""
    content = f"{name}={value}"
    sha = hashlib.sha256(content.encode()).hexdigest()
    return EvidenceItem(
        type=EvidenceType.METRIC,
        source=f"metric:{name}",
        sha256=sha,
        summary=summary or f"{name}: {value}",
        verified=True,
    )


def evidence_from_source_code(file_path: str | Path, summary: str = "") -> EvidenceItem | None:
    """Create an EvidenceItem referencing source code content."""
    path = Path(file_path)
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return EvidenceItem(
        type=EvidenceType.SOURCE_CODE,
        source=str(path),
        sha256=h.hexdigest(),
        summary=summary or f"Source: {path.name}",
        verified=True,
    )
