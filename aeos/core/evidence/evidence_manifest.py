from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.evidence.evidence_models import EvidenceManifest
from aeos.core.evidence.hash_utils import sha256, sha256_file


STAGE_RUNTIME = "runtime"
STAGE_EVAL = "eval"
STAGE_JUDGE = "judge"
STAGE_READINESS = "readiness"
STAGE_FINAL = "final"

STAGE_FILENAMES = {
    STAGE_RUNTIME: "runtime-evidence-manifest.json",
    STAGE_EVAL: "eval-evidence-manifest.json",
    STAGE_JUDGE: "judge-evidence-manifest.json",
    STAGE_READINESS: "readiness-evidence-manifest.json",
    STAGE_FINAL: "evidence-manifest.json",
}

IMMUTABLE_EXTENSIONS = {".json", ".md"}
MUTABLE_BEFORE_FINALIZE = {"hash-chain.jsonl", "audit-log.jsonl"}
EXCLUDED_FROM_SELF_HASH = {"evidence-manifest.json", "runtime-evidence-manifest.json", "eval-evidence-manifest.json", "judge-evidence-manifest.json", "readiness-evidence-manifest.json"}


def _infer_workspace_root(evidence_dir: Path) -> Path:
    """Walk up from evidence_dir to find the directory containing .aeos."""
    p = evidence_dir
    for _ in range(6):
        if (p / ".aeos").is_dir():
            return p
        parent = p.parent
        if parent == p:
            break
        p = parent
    return evidence_dir.parent.parent


class EvidenceManifestGenerator:
    def __init__(self, execution_id: str, evidence_dir: str, workspace_root: str = ""):
        self.execution_id = execution_id
        self.evidence_dir = Path(evidence_dir)
        self.workspace_root = Path(workspace_root) if workspace_root else _infer_workspace_root(self.evidence_dir)
        self.manifest = EvidenceManifest(
            execution_id=execution_id,
            generated_at=__import__("aeos.core.evidence.evidence_models", fromlist=["now_iso"]).now_iso(),
        )

    def add_file(self, filepath: str, record_count: int = 0) -> None:
        fp = Path(filepath)
        if fp.exists():
            file_hash = sha256_file(str(fp))
            try:
                rel = str(fp.relative_to(self.workspace_root))
            except ValueError:
                rel = str(fp)
            self.manifest.files.append({
                "path": rel,
                "sha256": file_hash,
                "size_bytes": fp.stat().st_size,
                "record_count": record_count,
            })
            self.manifest.total_records += record_count

    def add_directory(self, directory: str, extensions: tuple[str, ...] = (".json", ".jsonl", ".md")) -> None:
        dp = Path(directory)
        if not dp.exists():
            return
        for fp in sorted(dp.iterdir()):
            if fp.is_file() and fp.suffix in extensions:
                self.add_file(str(fp))

    def generate(self, output_path: str) -> str:
        manifest_str = json.dumps(self.manifest.to_dict(), indent=2, ensure_ascii=False)
        self.manifest.manifest_sha256 = sha256(manifest_str)
        final = self.manifest.to_dict()
        fp = Path(output_path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)
        return str(fp)


def compute_manifest_hash(manifest_dict: dict[str, Any]) -> str:
    """Compute SHA256 the same way the generator does.
    
    The generator computes the hash from the dict BEFORE setting manifest_sha256,
    which includes the field but with its default empty string value.
    So we must set manifest_sha256 to "" instead of removing it.
    """
    copy = dict(manifest_dict)
    copy["manifest_sha256"] = ""
    clean = json.dumps(copy, indent=2, ensure_ascii=False)
    return sha256(clean)


def verify_staged_manifest(manifest_path: Path, workspace_root: Optional[Path] = None) -> dict[str, Any]:
    """Verify a staged manifest file's hash integrity.
    
    Resolves referenced files relative to workspace_root (defaults to
    manifest's parent dir if not provided, then grandparent, etc.
    to find .aeos directory).
    
    Returns dict with: passed, stored_hash, computed_hash, files_ok, file_errors
    """
    result = {
        "passed": False,
        "stored_hash": "",
        "computed_hash": "",
        "files_ok": 0,
        "file_errors": [],
        "manifest_name": manifest_path.name,
    }
    if not manifest_path.exists():
        result["file_errors"].append(f"Manifest not found: {manifest_path}")
        return result

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        result["file_errors"].append(f"Cannot read manifest: {e}")
        return result

    stored_hash = manifest.get("manifest_sha256", "")
    computed_hash = compute_manifest_hash(manifest)
    result["stored_hash"] = stored_hash
    result["computed_hash"] = computed_hash

    if not stored_hash:
        result["file_errors"].append("No manifest_sha256 field in manifest")
        return result

    if computed_hash != stored_hash:
        result["file_errors"].append(
            f"Hash mismatch: stored={stored_hash[:16]}..., computed={computed_hash[:16]}..."
        )
        return result

    base_dirs = []
    if workspace_root:
        base_dirs.append(workspace_root)
    base_dirs.append(manifest_path.parent)
    parent = manifest_path.parent.parent
    for _ in range(4):
        if parent.exists():
            base_dirs.append(parent)
        parent = parent.parent

    for fe in manifest.get("files", []):
        fpath = fe.get("path", "")
        if Path(fpath).is_absolute():
            full_path = Path(fpath)
        else:
            full_path = None
            for bd in base_dirs:
                candidate = bd / fpath
                if candidate.exists():
                    full_path = candidate
                    break
            if full_path is None:
                full_path = base_dirs[0] / fpath
        if not full_path.exists():
            result["file_errors"].append(f"Referenced file missing: {fpath}")
            continue
        expected_hash = fe.get("sha256", "")
        if expected_hash:
            actual_hash = sha256_file(str(full_path))
            if actual_hash != expected_hash:
                result["file_errors"].append(
                    f"File hash mismatch: {fpath} (expected={expected_hash[:16]}..., actual={actual_hash[:16]}...)"
                )
                continue
        result["files_ok"] += 1

    result["passed"] = len(result["file_errors"]) == 0
    return result


class StagedManifestBuilder:
    """Builds evidence manifests in stages A-E."""

    def __init__(self, execution_id: str, evidence_dir: str, workspace_root: str = ""):
        self.execution_id = execution_id
        self.evidence_dir = Path(evidence_dir)
        self.workspace_root = workspace_root or str(_infer_workspace_root(self.evidence_dir))

    def _build_generator(self, stage: str) -> EvidenceManifestGenerator:
        return EvidenceManifestGenerator(self.execution_id, str(self.evidence_dir), self.workspace_root)

    def _output_path(self, stage: str) -> str:
        return str(self.evidence_dir / STAGE_FILENAMES[stage])

    def finalize_runtime_manifest(self) -> str:
        """Stage A: Runtime evidence manifest."""
        gen = self._build_generator(STAGE_RUNTIME)
        stage_files = [
            "runtime-request.jsonl",
            "runtime-result.jsonl",
            "tool_decision.jsonl",
            "tool_result.jsonl",
            "skill-result.jsonl",
            "skill-contract-validation.jsonl",
            "permission_decisions.jsonl",
            "policy_decisions.jsonl",
            "governance_decisions.jsonl",
        ]
        for sf in stage_files:
            fp = self.evidence_dir / sf
            if fp.exists():
                gen.add_file(str(fp))

        hash_chain = self.evidence_dir / "hash-chain.jsonl"
        if hash_chain.exists():
            gen.add_file(str(hash_chain))
        audit_log = self.evidence_dir / "audit-log.jsonl"
        if audit_log.exists():
            gen.add_file(str(audit_log))

        return gen.generate(self._output_path(STAGE_RUNTIME))

    def finalize_eval_manifest(self) -> str:
        """Stage B: Evaluation evidence manifest."""
        gen = self._build_generator(STAGE_EVAL)
        stage_files = [
            "eval-suite-results.jsonl",
            "eval-scorecard.json",
        ]
        for sf in stage_files:
            fp = self.evidence_dir / sf
            if fp.exists():
                gen.add_file(str(fp))

        reports_dir = self.evidence_dir.parent.parent / "reports" / self.execution_id
        eval_report = reports_dir / "evaluation-harness-report.md"
        if eval_report.exists():
            gen.add_file(str(eval_report))

        return gen.generate(self._output_path(STAGE_EVAL))

    def finalize_judge_manifest(self) -> str:
        """Stage C: Judge evidence manifest."""
        gen = self._build_generator(STAGE_JUDGE)
        stage_files = [
            "judge-input.json",
            "judge-result.json",
            "judge-scorecard.json",
        ]
        for sf in stage_files:
            fp = self.evidence_dir / sf
            if fp.exists():
                gen.add_file(str(fp))

        reports_dir = self.evidence_dir.parent.parent / "reports" / self.execution_id
        judge_report = reports_dir / "judge-report.md"
        if judge_report.exists():
            gen.add_file(str(judge_report))

        return gen.generate(self._output_path(STAGE_JUDGE))

    def finalize_readiness_manifest(self) -> str:
        """Stage D: Readiness evidence manifest."""
        gen = self._build_generator(STAGE_READINESS)
        stage_files = [
            "production-readiness-scorecard.json",
        ]
        for sf in stage_files:
            fp = self.evidence_dir / sf
            if fp.exists():
                gen.add_file(str(fp))

        reports_dir = self.evidence_dir.parent.parent / "reports" / self.execution_id
        readiness_report = reports_dir / "production-readiness-report.md"
        if readiness_report.exists():
            gen.add_file(str(readiness_report))

        return gen.generate(self._output_path(STAGE_READINESS))

    def finalize_evidence_manifest(self, extra_evidence_dirs: Optional[list[str]] = None) -> str:
        """Stage E: Final bundle manifest.
        
        Includes all staged manifests, but NOT itself (evidence-manifest.json).
        
        Args:
            extra_evidence_dirs: Additional evidence directories to search
                                 for staged manifests (e.g. eval dir, readiness dir).
        """
        gen = self._build_generator(STAGE_FINAL)

        search_dirs = [self.evidence_dir]
        if extra_evidence_dirs:
            search_dirs.extend(Path(d) for d in extra_evidence_dirs)

        seen = set()
        for sd in search_dirs:
            for so in [STAGE_FILENAMES[s] for s in [STAGE_RUNTIME, STAGE_EVAL, STAGE_JUDGE, STAGE_READINESS]]:
                fp = sd / so
                if fp.exists() and str(fp) not in seen:
                    seen.add(str(fp))
                    gen.add_file(str(fp))

        hash_chain = self.evidence_dir / "hash-chain.jsonl"
        if hash_chain.exists():
            gen.add_file(str(hash_chain))
        audit_log = self.evidence_dir / "audit-log.jsonl"
        if audit_log.exists():
            gen.add_file(str(audit_log))

        return gen.generate(self._output_path(STAGE_FINAL))

    def verify_all_manifests(self) -> dict[str, Any]:
        """Verify all staged manifests plus final."""
        workspace_root = Path(self.workspace_root) if self.workspace_root else None
        results = {}
        all_passed = True
        for stage in [STAGE_RUNTIME, STAGE_EVAL, STAGE_JUDGE, STAGE_READINESS, STAGE_FINAL]:
            fp = self.evidence_dir / STAGE_FILENAMES[stage]
            if not fp.exists():
                results[stage] = {"passed": False, "file_errors": [f"Manifest not found: {fp}"]}
                all_passed = False
                continue
            result = verify_staged_manifest(fp, workspace_root)
            results[stage] = result
            if not result["passed"]:
                all_passed = False

        return {
            "passed": all_passed,
            "execution_id": self.execution_id,
            "manifests": results,
        }

    def verify_manifest(self, stage: str) -> dict[str, Any]:
        """Verify a single staged manifest."""
        workspace_root = Path(self.workspace_root) if self.workspace_root else None
        fp = self.evidence_dir / STAGE_FILENAMES.get(stage, stage)
        if not fp.exists():
            return {"passed": False, "file_errors": [f"Manifest not found: {fp}"]}
        return verify_staged_manifest(fp, workspace_root)
