---
name: pr-reviewer
description: Review pull requests as an independent evidence-based reviewer. Use when the user requests pr reviewer or invokes pr-reviewer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: pr-reviewer

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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
- Flag an open PR that lacks a Why/Porquê section; that motivation is required worktree context.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
