---
name: decomposition-planning-roadmap
description: "Create decomposition plans and migration roadmaps for splitting monoliths. Use for extraction order. Do NOT use for domain analysis (domain-analysis)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Decomposition Planning and Roadmap

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Creates step-by-step decomposition plans and migration roadmaps for breaking apart monolithic applications.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [How to Use](references/instructions/02-how-to-use.md) — when in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when in scope.
- 4. [Core Concepts](references/instructions/04-core-concepts.md) — when in scope.
- 5. [Analysis Process](references/instructions/05-analysis-process.md) — when in scope.
- 6. [Output Format](references/instructions/06-output-format.md) — before acting.
- 7. [Analysis Checklist](references/instructions/07-analysis-checklist.md) — when in scope.
- 8. [Implementation Notes](references/instructions/08-implementation-notes.md) — when in scope.
- 9. [Best Practices](references/instructions/09-best-practices.md) — when in scope.
- 10. [Integration with Other Skills](references/instructions/10-integration-with-other-skills.md) — when in scope.
- 11. [Next Steps](references/instructions/11-next-steps.md) — at this step.
- 12. [Notes](references/instructions/12-notes.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
