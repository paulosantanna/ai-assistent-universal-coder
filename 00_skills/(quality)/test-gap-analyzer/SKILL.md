---
name: test-gap-analyzer
description: "Analyze test coverage gaps: untested modules and edge cases. Use for test gap analysis. Do NOT use as deployment approval or for unexecuted checks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Test Gap Analyzer Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

**ID:** test-gap-analyzer
**Version:** 1.0.0
**Owner Agent:** codenavi-agent
**Risk Level:** low

## Mission
Analyze the gap between source code and test coverage — identifying untested modules, functions, and edge cases.

## Scope
- Read source files and existing test files
- Map code paths to test coverage
- Identify untested functions, branches, error paths

## Allowed Actions
- `filesystem.read` — read source and test files
- `generate_evidence` — register gap findings

## Forbidden Actions
- Modify test files or source files
- Run test commands
- Write test files directly (use test-writer skill)

## Required Capabilities
- READ_REPOSITORY
- ANALYZE_TEST_COVERAGE
- GENERATE_REPORT

## Required Evidence
- Source files analyzed (paths with SHA-256)
- Test files analyzed (paths with SHA-256)
- Gap analysis report

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- Each gap must cite specific source line numbers
- Untested claims must be verifiable by file inspection

## Output Schema
```json
{
  "total_functions": 100,
  "tested_functions": 65,
  "untested_functions": [{"file": "src/service.py", "function": "calculate", "line": 42}],
  "coverage_pct": 65.0,
  "high_risk_gaps": [{"file": "src/auth.py", "function": "validate_token", "reason": "Security critical"}]
}
```

## Blocking Conditions
- Gap claims without source citations
- Attempts to modify test files

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
