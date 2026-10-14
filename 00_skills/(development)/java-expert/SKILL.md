---
name: java-expert
description: Implement, diagnose, modernize and migrate real Java projects with version-correct APIs, minimal diffs and evidence-backed verification. Use when the user requests java expert or invokes java-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission
Implement, diagnose, modernize and migrate real Java projects with version-correct APIs, minimal diffs and evidence-backed verification.

## Routing
1. Detect `maven.compiler.release`, source/target, Gradle toolchain, runtime/container JDK and CI matrix.
2. Route to the exact version skill: `java-17-expert`, `java-21-expert`, `java-25-expert` or `java-26-expert`.
3. Use the matching `docs-java-*` MCP for signatures, release behavior and migration deltas.
4. Preserve repository framework/style conventions; never modernize syntax merely because a newer JDK exists.

## Execution
BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

For migrations: baseline build/tests/performance → dependency/plugin compatibility → staged toolchain/runtime change → behavior/security/performance verification → rollback/documentation.

## Token discipline
Read `references/INDEX.md`; then load only the version/reference modules required by the mission. Follow `TOKEN_PROFILE.yaml`.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [verification.md](references/verification.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [version-routing.md](references/version-routing.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
