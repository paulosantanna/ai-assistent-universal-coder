from __future__ import annotations

from pathlib import Path
from typing import Any

from aeos.core.evidence.evidence_manifest import EvidenceManifestGenerator


class EvidenceReporter:
    def __init__(self, evidence_dir: str = ".aeos/evidence"):
        self.evidence_dir = Path(evidence_dir)

    def generate_manifest(self, execution_id: str, record_counts: dict[str, int]) -> str:
        gen = EvidenceManifestGenerator(execution_id, str(self.evidence_dir))
        base = self.evidence_dir / execution_id

        for record_type, count in record_counts.items():
            fp = base / f"{record_type}s.jsonl"
            if fp.exists():
                gen.add_file(str(fp), record_count=count)

        hash_fp = base / "hash-chain.jsonl"
        if hash_fp.exists():
            gen.add_file(str(hash_fp))

        audit_fp = base / "audit-log.jsonl"
        if audit_fp.exists():
            gen.add_file(str(audit_fp))

        manifest_path = base / "evidence-manifest.json"
        return gen.generate(str(manifest_path))
