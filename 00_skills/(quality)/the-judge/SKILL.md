---
name: the-judge
description: "Evidence-first PR judge: repo checks, correctness, security, one GitHub review. Use for 'review this PR' or 'julgue esse PR'. Do NOT use for CI fixes."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.4.0
  owner_agent: codenavi-agent
---

# The Judge

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Evidence-first pull request judge that reviews a PR and posts one consolidated GitHub review with inline comments via the gh CLI. Runs the repo's own deterministic checks first, researches current official docs before any claim about external libraries or APIs, then reviews correctness, security, structural quality (code judo, spaghetti growth, file-size limits), and AI slop including useless code comments. Every finding must carry evidence, every comment passes a deterministic noise gate before posting, and the verdict (APPROVE, COMMENT, REQUEST_CHANGES) is weighed by findings.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Non-Negotiables](references/instructions/02-non-negotiables.md) — when in scope.
- 3. [Severity and Verdict](references/instructions/03-severity-and-verdict.md) — when in scope.
- 4. [Workflow](references/instructions/04-workflow.md) — at this step.
- 5. [Summary Body Template](references/instructions/05-summary-body-template.md) — when in scope.
- 6. [Convergence Contract](references/instructions/06-convergence-contract.md) — before acting.
- 7. [Examples](references/instructions/07-examples.md) — when choosing an output or matching a use case.
- 8. [Troubleshooting](references/instructions/08-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
