---
name: pr-reviewer
description: "Review pull requests as an independent, evidence-based reviewer. Use for PR reviews. Do NOT use for deployment or unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: pr-reviewer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Review pull requests as an independent evidence-based reviewer.

## Review order
1. BRIEFING: intended change, acceptance criteria, declared risks.
2. RECON: changed files, tests, architecture, relevant notebook notes and current docs.
3. PLAN: review surfaces by risk.
4. EXECUTE: inspect correctness, security, data integrity, compatibility, performance, observability, rollback and maintainability.
5. VERIFY: reproduce relevant checks; distinguish observed facts from inference.
6. DEBRIEF: findings ordered by severity with precise file/line evidence and residual risk.

## Rules
- Do not nitpick style already accepted by the codebase.
- Do not request unrelated refactors.
- Prioritize bugs, regressions, unsafe behavior, missing tests and broken contracts.
- A risky untested path must be explicitly called out.
- Flag an open PR that lacks a Why/Porquê section; that motivation is required worktree context.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
