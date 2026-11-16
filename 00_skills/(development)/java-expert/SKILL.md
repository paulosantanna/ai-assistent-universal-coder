---
name: java-expert
description: "Implement, diagnose and migrate Java projects with version-correct APIs and evidence. Use for Java work. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [verification.md](references/verification.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [version-routing.md](references/version-routing.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
