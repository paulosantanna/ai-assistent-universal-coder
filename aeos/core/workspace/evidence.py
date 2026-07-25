"""Contrato de autoridade para evidência do Workspace OS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class EvidenceVerification:
    accepted: bool
    verifier_id: str
    provenance: str
    reason: str = ""


class EvidenceVerifier(Protocol):
    """Autoridade injetada; o kernel não confia no autor da claim."""

    def verify(
        self,
        *,
        execution_id: str,
        task_id: str,
        task_revision: int,
        evidence_type: str,
        artifact_path: Path,
    ) -> EvidenceVerification: ...
