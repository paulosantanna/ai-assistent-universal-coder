---
name: notebook-intelligence
description: "Maintain compact, fresh project intelligence in .notebook/. Use for notebook maintenance. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: notebook-intelligence

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Maintain compact, fresh project intelligence in `.notebook/` using progressive disclosure.

## Rules
- Read `INDEX.md` first; load only notes relevant to the current mission.
- One concept per note; prefer pointers over pasted source.
- Categories: flows, patterns, gotchas, domain, graph.
- INDEX entries are one line, <= ~100-char summary, 2–4 discriminative tags.
- Every note has Entry and Updated date.
- Update/archive stale information immediately.
- Never promote guesses or raw logs into project intelligence.

## Debrief
After a material change, determine whether code/architecture/business behavior invalidated any indexed note and repair the knowledge in the same mission.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
