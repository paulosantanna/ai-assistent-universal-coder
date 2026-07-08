# Skill: Security Audit

## Mission

Audit a repository for security vulnerabilities, exposed secrets, dependency risks, and compliance gaps.

## Allowed Actions

- Read files (excluding resolved secret values).
- List directories.
- Scan for secret patterns without revealing values.
- Scan dependency manifests for CVEs.
- Scan git history for committed secrets.
- Scan configuration files for security misconfigurations.
- Generate security reports.

## Forbidden Actions

- Print or log secret values.
- Write secrets to any file.
- Execute code from repository.
- Access production environments.
- Disable or bypass security controls.
- Modify security configurations without approval.

## Inputs

- workspace path
- scan scope (files, git history, dependencies)
- severity threshold

## Outputs

- secrets-audit-report.md
- dependency-audit-report.md
- configuration-audit-report.md
- compliance-report.md
- remediation-recommendations.md

## Evidence Required

- matched pattern locations (file + line, no value)
- dependency names and versions
- configuration files inspected
- git history commits inspected
- severity classification for each finding

## Quality Gates

- Must never expose secret values.
- Must classify each finding by severity.
- Must distinguish confirmed from potential findings.
- Must provide remediation steps for each finding.
- Must pass redaction validation.
