---
name: resolver-comentarios
description: "Resolve concrete PR review comments after inspecting code and verifying fixes. Use for PR comment fixes. Do NOT use for deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# resolver-comentarios

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Photographic-name compatibility skill. Resolve review comments through the canonical `pr-comment-resolver` capability using evidence, surgical changes and verification. The alias exists to preserve the photographed workspace UX.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
