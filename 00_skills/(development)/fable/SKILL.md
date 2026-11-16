---
name: fable
description: "Standard problem-solving loop: classify, gather evidence, act surgically, verify. Use for non-trivial tasks. Do NOT use for trivial one-step answers."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Provide enterprise-grade Fable Method problem-solving loop capability inside AEOS v1.1.

Refer to `.agents/skills/fable/SKILL.md` and `.agents/skills/fable/references/` for full method specifications.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
