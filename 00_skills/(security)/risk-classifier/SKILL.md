---
name: risk-classifier
description: Classify the risk level of proposed changes — considering scope, impact, reversibility, test coverage, and security implications. Use when the user requests risk classifier or invokes risk-classifier. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Risk Classifier Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

**ID:** risk-classifier
**Version:** 1.0.0
**Owner Agent:** codenavi-agent
**Risk Level:** low

## Mission
Classify the risk level of proposed changes — considering scope, impact, reversibility, test coverage, and security implications.

## Scope
- Analyze proposed changes and context
- Classify each change with risk level
- Generate mitigation recommendations for high/critical risks

## Allowed Actions
- `filesystem.read` — read patches, analysis reports
- `generate_evidence` — register risk classifications

## Forbidden Actions
- Modify any file
- Block or approve changes directly (decision is input for Judge)
- Override deterministic Judge rules

## Required Capabilities
- ANALYZE_RISK
- GENERATE_REPORT

## Required Evidence
- Patch/source analysis (SHA-256)
- Risk classification report

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- Risk levels must be one of: low, medium, high, critical
- High/critical MUST have mitigation strategy
- Classification must cite evidence

## Output Schema
```json
{
  "overall_risk": "medium",
  "risks": [
    {"risk": "API breakage", "level": "high", "mitigation": "Add deprecation warning, keep backward compat for 1 release",
     "evidence": ["src/api/v1/users.py:45"]},
    {"risk": "Security regression", "level": "medium", "mitigation": "Add input validation tests",
     "evidence": ["src/auth/validator.py:12"]}
  ],
  "safe_to_propose": true
}
```

## Blocking Conditions
- High risk without any mitigation
- Risk classification contradicts obvious severity
- Insufficient evidence for classification

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
