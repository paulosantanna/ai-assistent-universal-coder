"""Security Secrets Audit Playbook — detects secrets without exposing values."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from aeos_workbench.scanner.scanner import ProjectScanner

SECRET_PATTERNS = [
    (r'(?i)password\s*[=:]\s*[\'"][^\'"]+[\'"]', "password-assignment", "high"),
    (r'(?i)secret\s*[=:]\s*[\'"][^\'"]+[\'"]', "secret-assignment", "high"),
    (r'(?i)api[_-]?key\s*[=:]\s*[\'"][^\'"]+[\'"]', "api-key", "high"),
    (r'(?i)token\s*[=:]\s*[\'"][^\'"]+[\'"]', "token-assignment", "high"),
    (r'AKIA[0-9A-Z]{16}', "aws-access-key", "critical"),
    (r'sk-[a-zA-Z0-9]{20,}', "openai-secret-key", "critical"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "private-key", "critical"),
    (r'-----BEGIN CERTIFICATE-----', "certificate", "medium"),
    (r'(?i)jdbc:[a-z]+://[^\s]+', "jdbc-connection-string", "medium"),
    (r'(?i)mongodb(?:\+srv)?://[^\s]+', "mongodb-connection-string", "medium"),
    (r'(?i)redis://[^\s]+', "redis-connection-string", "medium"),
    (r'(?i)postgresql://[^\s]+', "postgres-connection-string", "medium"),
    (r'(?i)mysql://[^\s]+', "mysql-connection-string", "medium"),
]

SAFE_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".conf"}
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", ".exe", ".dll", ".so", ".bin", ".pyc"}


class SecretsAuditPlaybook:
    def __init__(self, sandbox_writer, rollback_manager, step_engine, execution_id: str, reports_dir: Path, evidence_dir: Path):
        self.sandbox_writer = sandbox_writer
        self.rollback_manager = rollback_manager
        self.step_engine = step_engine
        self.execution_id = execution_id
        self.reports_dir = reports_dir / execution_id
        self.evidence_dir = evidence_dir / execution_id
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.generated_artifacts: list[dict] = []
        self.risks: list[str] = []
        self.findings: list[dict] = []

    def _redact_value(self, text: str) -> str:
        return re.sub(r'([\'"])([^\'"]+)([\'"])', r'\1****\3', text)

    def execute(self, target_path: Path) -> dict:
        step_id = self.step_engine.register_step({
            "step_id": "secrets-scan",
            "skill": "security-audit",
            "status": "running",
            "inputs": {"target_path": str(target_path)},
            "outputs": {},
            "evidence": [],
            "permission_decisions": [],
            "risks": [],
            "errors": [],
        })

        scanner = ProjectScanner(target_path)
        scan_result = scanner.scan()
        findings = []
        files_checked = 0

        for f in scan_result.get("files", []):
            fpath = Path(target_path) / f["path"]
            ext = fpath.suffix.lower()
            if ext in BINARY_EXTENSIONS:
                continue
            if not fpath.is_file():
                continue
            if f.get("size", 0) > 512 * 1024:
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            files_checked += 1
            for pattern, label, severity in SECRET_PATTERNS:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count("\n") + 1
                    findings.append({
                        "type": label,
                        "severity": severity,
                        "file": f["path"],
                        "line": line_num,
                        "recommendation": self._get_recommendation(label, severity),
                    })

        sorted_findings = sorted(findings, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["severity"], 99))
        self.findings = sorted_findings

        self.step_engine.update_step(step_id, {
            "status": "completed",
            "outputs": {
                "files_checked": files_checked,
                "findings_count": len(sorted_findings),
                "critical_count": sum(1 for f in sorted_findings if f["severity"] == "critical"),
                "high_count": sum(1 for f in sorted_findings if f["severity"] == "high"),
            },
            "evidence": [
                {"type": "secret-scan", "files_checked": files_checked, "findings": len(sorted_findings)}
            ],
        })
        self.step_engine.save_all()

        self._generate_report(sorted_findings, files_checked)
        self._save_raw_findings(sorted_findings, files_checked)

        return {
            "generated_artifacts": self.generated_artifacts,
            "risks": self.risks,
            "findings_count": len(sorted_findings),
        }

    def _get_recommendation(self, label: str, severity: str) -> str:
        recommendations = {
            "password-assignment": "Move password to environment variable or secret manager",
            "secret-assignment": "Move secret to environment variable or secret manager",
            "api-key": "Use managed API key service (e.g., AWS Secrets Manager, HashiCorp Vault)",
            "token-assignment": "Store token in runtime environment variable",
            "aws-access-key": "Revoke key and use IAM roles or AWS Secrets Manager",
            "openai-secret-key": "Use environment variable for API key",
            "private-key": "Store private key in secure keystore or HSM",
            "certificate": "Use certificate manager (e.g., cert-manager, ACM)",
            "jdbc-connection-string": "Externalize connection strings to environment variables",
            "mongodb-connection-string": "Externalize connection strings to environment variables",
            "redis-connection-string": "Externalize connection strings to environment variables",
            "postgres-connection-string": "Externalize connection strings to environment variables",
            "mysql-connection-string": "Externalize connection strings to environment variables",
        }
        return recommendations.get(label, "Review and secure this value")

    def _generate_report(self, findings: list[dict], files_checked: int):
        critical = [f for f in findings if f["severity"] == "critical"]
        high = [f for f in findings if f["severity"] == "high"]
        medium = [f for f in findings if f["severity"] == "medium"]
        low = [f for f in findings if f["severity"] == "low"]

        content = f"""# Security Secrets Audit Report

**Execution ID:** {self.execution_id}
**Generated At:** {datetime.now(timezone.utc).isoformat()}
**Files Checked:** {files_checked}
**Total Findings:** {len(findings)}

## Summary

| Severity | Count |
|----------|-------|
| Critical | {len(critical)} |
| High | {len(high)} |
| Medium | {len(medium)} |
| Low | {len(low)} |

## Security Notice

> ⚠️ **WARNING:** This report contains references to potential secret patterns.
> Actual secret values are NEVER included in this report.
> All findings are redacted for security.

## Findings

"""
        if not findings:
            content += "No potential secrets detected.\n"
        else:
            content += "| # | Type | Severity | File | Line | Recommendation |\n"
            content += "|---|------|----------|------|------|---------------|\n"
            for i, f in enumerate(findings, 1):
                escaped_file = f["file"].replace("|", "\\|")
                content += f"| {i} | {f['type']} | {f['severity']} | `{escaped_file}` | ~{f['line']} | {f['recommendation']} |\n"

        content += """
## Remediation Plan

"""
        if critical:
            content += "### Critical Findings\n"
            content += "1. **Immediate action required:** Review and rotate exposed credentials.\n"
            content += "2. Remove hardcoded secrets from source code.\n"
            content += "3. Use environment variables or secret manager.\n"
            content += "4. Scan git history for exposed secrets.\n\n"

        if high:
            content += "### High Findings\n"
            content += "1. Move secrets to environment variables or secret store.\n"
            content += "2. Audit access logs for unauthorized use.\n"
            content += "3. Consider key rotation.\n\n"

        if medium or low:
            content += "### Medium/Low Findings\n"
            content += "1. Review flagged files and assess risk.\n"
            content += "2. Externalize hardcoded configuration values.\n"
            content += "3. Add pre-commit hooks for secret detection.\n\n"

        content += """## Recommendations

1. **Install pre-commit hooks** with `detect-secrets` or `truffleHog`
2. **Use `.gitignore`** to exclude `.env*` and `secrets/**` files
3. **Audit git history** for committed secrets
4. **Set up CI/CD scanning** with GitHub secret scanning or similar
5. **Rotate any exposed credentials** immediately

---
*Generated by AEOS v0.2 Security Secrets Audit Playbook*
*No secret values were exposed in this report.*
"""
        report_path = self.reports_dir / "security-secrets-audit.md"
        report_path.write_text(content, encoding="utf-8")
        self.rollback_manager.register_generated_file(report_path, f"reports/{self.execution_id}/security-secrets-audit.md", content[:100])

        self.generated_artifacts.append({
            "name": "security-secrets-audit.md",
            "path": str(report_path),
            "type": "security-report",
            "size": len(content.encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def _save_raw_findings(self, findings: list[dict], files_checked: int):
        safe_findings = []
        for f in findings:
            safe_findings.append({
                "type": f["type"],
                "severity": f["severity"],
                "file": f["file"],
                "line": f["line"],
                "recommendation": f["recommendation"],
            })
        data = {
            "execution_id": self.execution_id,
            "files_checked": files_checked,
            "total_findings": len(findings),
            "findings": safe_findings,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        path = self.evidence_dir / "secret-scan-result.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        self.rollback_manager.register_generated_file(path, f"evidence/{self.execution_id}/secret-scan-result.json", json.dumps(data)[:100])
        self.generated_artifacts.append({
            "name": "secret-scan-result.json",
            "path": str(path),
            "type": "evidence",
            "size": len(json.dumps(data).encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })