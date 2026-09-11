---
name: pr-reviewer
description: "Use for Skill: pr-reviewer."
---

# Skill: pr-reviewer
Governance: CodENavi v1

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