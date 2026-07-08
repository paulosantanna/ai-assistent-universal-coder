# Playbook: Python AI Hardening

## Objective

Audit and harden a Python AI project for production readiness, covering security, dependency health, RAG pipeline safety, and code quality.

## Preconditions

- Workspace path exists.
- Python source files detected.
- AI framework detected (FastAPI, RAG pipeline, training scripts).
- MCPs for filesystem read/write and git available.
- LCPs for global rules, python-ai, and security-governance loaded.

## Agents

- Root Agent
- Architect Agent
- Coder Agent
- Security Agent
- Judge Agent

## Skills

- python-rag-audit
- security-audit

## MCPs

- filesystem-readonly
- filesystem-write-sandbox
- git-readonly
- git-write-branch

## Steps

1. Load project context and Python AI LCPs.
2. Scan Python dependencies for known vulnerabilities.
3. Audit RAG pipeline for prompt injection risks.
4. Audit data processing for PII/PHI exposure.
5. Check for hardcoded secrets and API keys.
6. Validate model loading and serialization safety.
7. Review training pipeline for data leakage.
8. Generate hardening report with fixes.
9. Apply non-destructive fixes to sandbox.
10. Generate final security audit report.
11. Send outputs to Judge Agent.
12. Generate judge-report.md.

## Blocking Conditions

- Hardcoded secrets detected.
- Unpatched critical vulnerabilities.
- PII/PHI exposure without safeguards.
- No rollback plan for changes.

## Outputs

- .aeos/python-security-audit.md
- .aeos/dependency-scan.md
- .aeos/rag-safety-report.md
- .aeos/hardening-report.md
- .aeos/judge-report.md
