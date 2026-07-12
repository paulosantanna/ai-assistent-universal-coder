"""Gate 1: Repository Hygiene — real file scanning, not just directory existence."""

from __future__ import annotations
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, BINARY_EXTENSIONS, DEFAULT_EXCLUSIONS


SUSPICIOUS_PATTERNS: list[str] = [
    "secret", "password", "credential", "token", "apikey", "api_key",
    ".env", "id_rsa", "id_dsa", "private_key", "key.pem",
    "config.json", "credentials", "secrets",
]

SUSPICIOUS_EXTENSIONS: set[str] = {
    ".env", ".key", ".pem", ".cert", ".crt", ".p12", ".pfx",
    ".ovpn", ".vpn",
}


def _fast_scan(root: Path, max_samples: int = 5) -> dict:
    """Scan repository structure without loading the full file list into memory."""
    categories: dict[str, list[str]] = {
        "generated": [],
        "temporary": [],
        "duplicate": [],
        "artifact": [],
        "suspicious": [],
        "large": [],
    }
    total_files = 0
    total_size = 0
    suffix_counts: Counter = Counter()
    ignored_count = 0

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            ignored_count += 1
            continue
        total_files += 1
        size = p.stat().st_size
        total_size += size
        suffix_counts[p.suffix.lower()] += 1

        if size > 10 * 1024 * 1024:
            if len(categories["large"]) < max_samples:
                categories["large"].append(f"{rel} ({size / 1024 / 1024:.1f} MB)")

        name_lower = p.name.lower()
        if any(sp in name_lower for sp in SUSPICIOUS_PATTERNS):
            if len(categories["suspicious"]) < max_samples:
                categories["suspicious"].append(rel)

        if p.suffix.lower() in SUSPICIOUS_EXTENSIONS:
            if len(categories["suspicious"]) < max_samples:
                if rel not in categories["suspicious"]:
                    categories["suspicious"].append(rel)

        if name_lower in {"tmp", "temp"} or name_lower.startswith("tmp") or name_lower.endswith(".tmp"):
            if len(categories["temporary"]) < max_samples:
                categories["temporary"].append(rel)

        if p.suffix.lower() in BINARY_EXTENSIONS:
            if len(categories["artifact"]) < max_samples:
                categories["artifact"].append(rel)

    return {
        "total_files": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "ignored_count": ignored_count,
        "suffixes": dict(suffix_counts.most_common(20)),
        "categories": categories,
    }


def check_repository_hygiene(repository: str) -> GateResult:
    """Gate 1: Verify repository hygiene — no generated/temp/suspicious files versioned."""
    gate = GateResult(
        id="repository_hygiene",
        title="Repository Hygiene",
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

    scan = _fast_scan(root)

    gate.metrics["total_files"] = scan["total_files"]
    gate.metrics["total_size_mb"] = scan["total_size_mb"]
    gate.metrics["ignored_count"] = scan["ignored_count"]
    gate.metrics["top_suffixes"] = scan["suffixes"]

    issues: list[str] = []
    for cat, items in scan["categories"].items():
        if items:
            gate.evidence.append({
                "type": "source_code" if cat != "artifact" else "artifact",
                "source": f"category:{cat}",
                "sha256": "",
                "summary": f"{len(items)} sample(s) in category '{cat}': {', '.join(items)}",
                "verified": False,
            })
            issues.append(f"Found {cat} files: {', '.join(items)}")

    if issues:
        gate.findings.extend(issues)
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 2.0)
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.evidence.append({
            "type": "metric",
            "source": "static_analysis",
            "sha256": "",
            "summary": f"Repository hygiene clean: {scan['total_files']} files, no issues detected",
            "verified": True,
        })

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
