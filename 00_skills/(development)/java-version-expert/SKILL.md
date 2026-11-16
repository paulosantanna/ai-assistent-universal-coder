---
name: java-version-expert
description: "Route Java work to the exact verified JDK profile, loading only needed knowledge. Use for JDK version routing. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: java-version-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Route Java work to the exact verified JDK profile without loading unrelated version knowledge.

## Invoke when
- a Java repository must be created, diagnosed, modernized or migrated;
- the target JDK is unknown or multiple JDKs coexist;
- framework/build compatibility must be resolved before implementation.

## Lifecycle
**BRIEFING** — objective, target repository, runtime constraints, acceptance criteria.

**RECON** — inspect `pom.xml`/Gradle, toolchains, CI, container/runtime, framework versions and production JDK. Never infer the target from syntax alone.

**PLAN** — select exactly one primary version expert (`java-expert-17`, `java-expert-21`, `java-expert-25`, `java-expert-26`) plus migration references only when required.

**EXECUTE** — preserve project conventions; use only APIs/features supported by the verified target; keep changes surgical.

**VERIFY** — compile/test with the declared toolchain and verify framework/plugin/runtime compatibility from current official documentation.

**DEBRIEF** — evidence, changed files, test/build result, residual compatibility risks and notebook updates.

## Token contract
Read this file first. Then read `references/INDEX.md`. Load only the references selected by mission/version. Do not load all JDK profiles into one context.

## Stop conditions
- JDK source/target/runtime cannot be established;
- framework/plugin compatibility is unresolved for a material change;
- requested API behavior cannot be verified from project evidence or current authoritative documentation.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
