---
name: pr-comment-resolver
description: "Resolve PR review comments systematically, without blindly obeying incorrect feedback. Use for PR comment resolution. Do NOT use for deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# PR Comment Resolver

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Resolve pull-request review comments systematically without blindly obeying incorrect feedback.

## Workflow
Collect unresolved threads → classify correctness/security/style/question → inspect referenced code → reproduce concern when possible → accept/reject with technical rationale → implement minimal fix → run targeted/full verification → draft evidence-backed reply → resolve only when addressed.

Never modify unrelated code merely to satisfy stylistic preference.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
