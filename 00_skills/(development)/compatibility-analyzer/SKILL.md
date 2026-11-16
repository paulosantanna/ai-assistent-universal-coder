---
name: compatibility-analyzer
description: "Analyze dependency compatibility: version conflicts, peer deps, platform limits, breaking changes. Use for compat checks. Do NOT use for deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Compatibility Analyzer Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

**ID:** compatibility-analyzer
**Version:** 1.0.0
**Owner Agent:** codenavi-agent
**Risk Level:** medium

## Mission
Analyze dependency compatibility — version conflicts, peer dependency issues, platform constraints, breaking change risk.

## Scope
- Parse dependency version constraints
- Detect peer dependency mismatches
- Assess platform and OS compatibility
- Classify breaking change risk (patch/minor/major)

## Allowed Actions
- `filesystem.read` — read dependency files
- `generate_evidence` — register findings

## Forbidden Actions
- Update version constraints
- Install packages to resolve conflicts
- Run compatibility tooling that modifies files

## Required Capabilities
- READ_REPOSITORY
- ANALYZE_COMPATIBILITY
- GENERATE_REPORT

## Required Evidence
- Dependency files read (SHA-256)
- Compatibility matrix
- Conflict report

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- Every compatibility claim must cite source lines
- Breaking change risk must specify reason
- Matrix must be complete for all direct dependencies

## Output Schema
```json
{
  "compatibility_matrix": [
    {"dep": "react", "current": "18.2.0", "peer_required": ">=17", "compatible": true, "risk": "low"},
    {"dep": "typescript", "current": "5.0.0", "peer_required": ">=4.5", "compatible": true, "risk": "low"}
  ],
  "conflicts": [],
  "platform_issues": [],
  "breaking_change_risks": []
}
```

## Blocking Conditions
- Compatibility analysis is missing a required dependency
- Attempt to modify dependency files

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
