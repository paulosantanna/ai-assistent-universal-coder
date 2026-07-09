from dataclasses import dataclass, field
from typing import List

@dataclass
class ArtifactProvenance:
    artifact_path: str
    builder: str
    source_ref: str
    commit_sha: str | None = None
    build_command: str | None = None
    materials: List[str] = field(default_factory=list)
    sha256: str | None = None

class ProvenanceValidator:
    def validate(self, provenance: ArtifactProvenance) -> dict:
        missing = []
        for field_name in ["artifact_path", "builder", "source_ref", "sha256"]:
            if not getattr(provenance, field_name):
                missing.append(field_name)
        return {"status": "PASS" if not missing else "BLOCKED", "missing": missing}
