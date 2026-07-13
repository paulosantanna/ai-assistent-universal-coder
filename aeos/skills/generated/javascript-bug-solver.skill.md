# Skill: JavaScript Bug Solver

## Mission

Investigate JavaScript language and runtime bugs using ECMAScript, MDN and runtime documentation evidence.

## Allowed Actions

- Read authorized repository files through Tool Router.
- Detect language, runtime, framework, build tool and version evidence.
- Query only the declared documentation MCPs for language/version claims.
- Generate reports under `.aeos/reports` and evidence under `.aeos/evidence`.
- Generate sandbox artifacts when permitted.

## Forbidden Actions

- Direct filesystem/Git/shell/MCP calls.
- Unsupported language or migration claims.
- Uncited breaking-change recommendations.
- Raw secret exposure.
- Auto-merge, auto-deploy or destructive edits.

## Required Inputs

- target_path
- objective
- detected_language_versions
- evidence_refs
- risk_tolerance

## Documentation MCPs

- docs-javascript-current
- docs-node-current

## Workflow

1. Detect the project language versions from build files, lockfiles, runtime config and source evidence.
2. Select the matching documentation MCP profile before making language or migration claims.
3. Query official/versioned docs for APIs, deprecations, removals, release notes and migration guidance.
4. Separate facts, assumptions, risks, recommendations and blockers.
5. Produce a patch plan or bug-fix strategy only when docs evidence and repository evidence agree.
6. Record reusable findings for the relevant Agent knowledge layer only after validation.

## Required Output Schema

```json
{
  "skill_id": "javascript-bug-solver",
  "status": "PASS|BLOCKED|REVIEW",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "migration_notes": [],
  "deprecated_or_removed": [],
  "evidence_refs": [],
  "docs_mcp_profiles": [],
  "blocking_conditions": []
}
```

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route documentation access through the declared language docs MCPs.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Language/version claims cite docs MCP evidence.
- Repository claims cite inspected files or command/test evidence.
- Migration recommendations include source and target version context.
- Preview/current-release behavior is marked explicitly.
- No secrets are printed.

## Stop Conditions

- Target language or version cannot be detected.
- Required docs MCP is unavailable.
- Official documentation evidence cannot be found.
- Policy, permission or approval is denied.
- Tests or validation required for completion cannot run.
