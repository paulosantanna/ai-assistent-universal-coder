---
name: security-best-practices
description: "Assimilated OpenAI/TLC language-specific security review. Use when the user asks for security best practices, a secure-by-default review, or a vulnerability report for Python, JavaScript/TypeScript or Go. Triggers: security best practices, security review, secure-by-default. Do not use for general review, threat modeling (security-threat-model), or ownership maps (security-ownership-map)."
---

# Security Best Practices

Assimilated from installed `security-best-practices` 1.0.0. Original contract: `references/ORIGINAL_SKILL.md`. Framework files live under `references/<language>-<framework>-<stack>-security.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Detect languages and frameworks in scope, load only matching reference files, then write secure-by-default code, flag high-impact issues, or produce a prioritized report with file:line evidence.

## Relationship to AEOS security skills

- Workspace web headers/CSP: `best-practices`.
- Enterprise/repo audit playbooks: `security-audit` / `enterprise-security-auditor`.
- Abuse-path threat model: `security-threat-model` (and existing `threat-modeler` when that playbook is selected).
- This skill does not waive AEOS security, `specs` or approval gates.

## Activation

- User explicitly asks for security best practices, a security report, or secure-by-default help in supported stacks.

## Non-activation

- General code review or debugging.
- Threat modeling (`security-threat-model`).
- Git ownership / bus factor (`security-ownership-map`).

## Critical rules

1. Identify frontend and backend stacks from the repo. Load every matching `references/` file; do not invent a stack.
2. If no reference matches, say so before writing a report. Verify current official guidance; do not treat the reference as live CVE truth.
3. Reports use file:line evidence, numeric finding IDs, severity sections, and an executive summary. Default path: `security_best_practices_report.md` unless the user names another.
4. Do not persist secrets found in the repo into the report, notebook or chat. Redact.
5. Follow report/fix rules in `references/ORIGINAL_SKILL.md`. Honor documented project overrides; record the bypass.
6. Commits and remediations only with explicit authorization when they mutate protected surfaces.

## Continuity

Promote only verified durable control decisions into `.notebook/MEMORY.md`.
