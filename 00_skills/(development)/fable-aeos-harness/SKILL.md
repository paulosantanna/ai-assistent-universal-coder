---
name: fable-aeos-harness
description: "Execution harness wrapping all AEOS skills with the Fable problem-solving loop. Use to run AEOS skills under Fable. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-aeos-harness

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Enforce Fable Method governance across ALL AEOS skills inside AEOS v1.1.

Read `00_skills/(development)/fable/SKILL.md` for the governing problem-solving loop. The retired aeos-prefixed package is not a second agent or a runtime dependency.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
