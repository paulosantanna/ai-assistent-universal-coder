---
name: java-migration
description: "Analyze Java projects and perform version migrations, API replacements and build updates. Use for Java migrations. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: Java Migration

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Analyze Java projects and perform version migrations, API replacements, and build configuration updates.

## Allowed Actions

- Read Java source files.
- Read build configuration (pom.xml, build.gradle).
- Read module descriptors.
- Detect deprecated APIs and suggest replacements.
- Apply code transformations within sandbox.
- Run build commands.
- Run test suites.
- Generate migration reports.

## Forbidden Actions

- Delete modules without evidence.
- Change public API without contract test.
- Upgrade major dependencies without compatibility check.
- Commit directly to main branch.
- Merge pull requests without approval.
- Deploy without approval.

## Inputs

- workspace path
- source Java version
- target Java version
- migration scope

## Outputs

- migration-report.md
- compatibility-report.md
- changed-files.md
- test-results.md

## Evidence Required

- dependency tree before/after
- build results
- test results
- changed files diff
- rollback plan

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Documentation Intelligence

Before recommending a Java version migration, select the source and target documentation MCPs from:

- `docs-java-11`
- `docs-java-17`
- `docs-java-21`
- `docs-java-25`
- `docs-java-26`

Use `language_docs.migration_delta` and `language_docs.lookup_symbol` for API, deprecation, removal and release-note claims. Mark unsupported or undocumented migration advice as `REVIEW` or `BLOCKED`.

## Quality Gates

- Must pass full test suite.
- Must not break public API without contract tests.
- Must document every change.
- Must verify build after migration.
- Must produce rollback plan.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
