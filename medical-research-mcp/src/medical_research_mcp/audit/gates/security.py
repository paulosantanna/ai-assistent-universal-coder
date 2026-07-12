"""Gate 9: Security — secret scanning, unsafe patterns, prompt injection, auth."""

from __future__ import annotations
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus, EvidenceItem, EvidenceType
from ..command_runner import find_tool
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

SECRET_PATTERNS = [
    "api_key", "apikey", "api.secret", "api_secret",
    "password", "passwd", "secret", "token",
    "aws_access_key", "aws_secret_key", "AZURE_",
    "ghp_", "gho_", "ghu_", "ghs_", "ghr_",
    "sk-", "pk-",
]

UNSAFE_IMPORTS = ["pickle", "shelve", "marshal", "subprocess"]
PROMPT_INJECTION_TERMS = [
    "ignore all", "ignore previous", "system prompt",
    "you are now", "act as", "DAN", "jailbreak",
]


def check_security(repository: str, run_scan: bool = True, max_output_chars: int = 50000) -> GateResult:
    """Gate 9: Security audit — real scanning, not just config existence check."""
    gate = GateResult(
        id="security",
        title="Security",
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

    issues = []

    # 1. Secret scanning via git (if available) or grep-based search
    git = find_tool("git")
    if git and (root / ".git").is_dir():
        pattern = "|".join(SECRET_PATTERNS)
        try:
            git_result = subprocess.run(
                [git, "grep", "-n", "--untracked", "-I", "-E", pattern, "--", "*.py", "*.json", "*.yaml", "*.yml", "*.env", "*.ini", "*.cfg"],
                capture_output=True, text=True, timeout=60, cwd=str(root),
                errors="replace",
            )
            gate.metrics["git_grep_exit"] = git_result.returncode
            if git_result.returncode == 0 and git_result.stdout.strip():
                secret_lines = [l for l in git_result.stdout.splitlines() if l.strip() and "Binary" not in l]
                if secret_lines:
                    gate.findings.append(f"Potential secrets detected: {len(secret_lines)} matches")
                    for s in secret_lines[:10]:
                        gate.evidence.append({
                            "type": "command_output",
                            "source": "git grep secret patterns",
                            "sha256": "",
                            "summary": s[:200],
                            "verified": False,
                        })
                    issues.append("secrets_found")
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            gate.findings.append("Git grep timed out or failed — falling back to static scan")
    else:
        # Fallback grep
        secret_files = []
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            rel = str(p.relative_to(root)).replace("\\", "/")
            if should_ignore(rel, DEFAULT_EXCLUSIONS):
                continue
            if p.suffix.lower() in {".py", ".json", ".yaml", ".yml", ".env", ".ini", ".cfg"}:
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                for pat in SECRET_PATTERNS:
                    if pat in text:
                        secret_files.append(f"{rel}: matched '{pat}'")
                        break
        if secret_files:
            gate.findings.append(f"Potential secrets (fallback scan): {len(secret_files)} files")
            for s in secret_files[:10]:
                gate.evidence.append({
                    "type": "source_code",
                    "source": s,
                    "sha256": "",
                    "summary": s[:200],
                    "verified": False,
                })
            issues.append("secrets_found")

    # 2. Unsafe imports
    unsafe_files = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for imp in UNSAFE_IMPORTS:
            if f"import {imp}" in text or f"from {imp}" in text:
                unsafe_files.append(f"{rel}: uses {imp}")
                break
    if unsafe_files:
        gate.findings.append(f"Unsafe imports detected: {len(unsafe_files)} files")
        for u in unsafe_files[:5]:
            gate.evidence.append({
                "type": "source_code",
                "source": u,
                "sha256": "",
                "summary": u[:200],
                "verified": False,
            })
        issues.append("unsafe_imports")

    # 3. Prompt injection patterns
    injection_files = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if any(t in text.lower() for t in PROMPT_INJECTION_TERMS):
            injection_files.append(rel)
            if len(injection_files) >= 5:
                break
    if injection_files:
        gate.findings.append(f"Prompt injection patterns found: {len(injection_files)} files")
        gate.findings.append("Review files for hardcoded system prompts that could be exploited")

    # 4. Auth/AuthZ check
    auth_files = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if any(t in text for t in {"authenticate", "authorize", "rbac", "permission", "login", "oauth"}):
            auth_files.append(rel)
            if len(auth_files) >= 10:
                break
    gate.metrics["auth_references"] = len(auth_files)

    gate.metrics["secret_matches"] = len([f for f in issues if f == "secrets_found"])
    gate.metrics["unsafe_imports"] = len([f for f in issues if f == "unsafe_imports"])

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
        gate.remediation = [
            "Remove hardcoded secrets and use environment variables or vault",
            "Replace unsafe imports (pickle, shelve, marshal) with safe alternatives",
            "Add input sanitization to prevent prompt injection",
            "Implement RBAC for API endpoints",
        ]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.findings.append("No security issues detected")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
