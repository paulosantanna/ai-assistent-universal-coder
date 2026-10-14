---
name: java-migration
description: Analyze Java projects and perform version migrations, API replacements, and build configuration updates. Use when the user requests java migration or invokes java-migration. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: Java Migration

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
