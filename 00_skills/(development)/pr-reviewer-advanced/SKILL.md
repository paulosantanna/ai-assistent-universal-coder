---
name: pr-reviewer-advanced
description: "Perform severity-ranked, evidence-backed PR reviews. Use for deep PR reviews. Do NOT use for deployment or unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Advanced PR Reviewer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Perform severity-ranked, evidence-backed PR review.

## Review dimensions
Correctness, contracts, concurrency, data integrity, security, performance, backward compatibility, tests, observability, documentation and architectural boundaries.

Findings include file/location, failure scenario, impact, evidence and minimal remediation. Avoid speculative nitpicks; prioritize defects that can actually occur. Missing Why/Porquê on the PR body is a review defect because later worktrees lose the motivation for the change.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
