---
name: risk-classifier
description: "Classify change risk: scope, impact, reversibility, coverage. Use for risk classification. Do NOT use outside authorized scope or to expose secrets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Risk Classifier Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
