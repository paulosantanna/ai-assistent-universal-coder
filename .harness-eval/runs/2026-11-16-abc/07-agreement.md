# Harness Eval: Judge Agreement (Track B)

> Run dir: `.harness-eval\runs\2026-11-16-abc`
> Trap gate: PASS (misses=0)
> Bands: Ship = dual REDUNDANT + J2 cost≤1; Review = dual KEEP; Hold = disagree / missing

## What these words mean

| Word | Meaning | You should |
|------|---------|------------|
| **Ship** | Both judges: text is redundant and cheap to rediscover | Delete / trim |
| **Review** | Both judges: keep (not redundant) | Leave alone |
| **Hold** | Judges disagreed or score missing | Do nothing yet |
| **Trap PASS** | Planted traps scored correctly | Trust Ship |

This track answers: *would an agent rediscover this without the harness?* Not the same as usefulness (`10-usefulness-agreement.md`).

## Executive summary

- Real claims scored: 1071
- Ship: **1**
- Review: **830**
- Hold: **240**
- Trap misses: none

## Discrimination (plants)

| ID | Expected family | J2 family |
|----|-----------------|-----------|
| P003 | REDUNDANT | REDUNDANT |
| P004 | REDUNDANT | REDUNDANT |
| P005 | KEEP | KEEP |
| P006 | KEEP | KEEP |

Ship by tier: {'T0': 1}
Hold by tier: {'T0': 20, 'T1': 220}

## Ship

| ID | Tier | Source | J1 | J2 cost/class | Quote |
|----|------|--------|----|---------------|-------|
| C020 | T0 | `AGENTS.md` | REDUNDANT-GENERAL | 1/REDUNDANT-GENERAL | Think before coding. |

## Hold

| ID | Tier | Reason | J1 | J2 | Quote |
|----|------|--------|----|----|-------|
| C010 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Inspect the existing codebase before modifying it. |
| C011 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Prefer project conventions and existing patterns over introducing new ones. |
| C012 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Verify current APIs, framework behavior and dependency versions against project evidence and current |
| C015 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-POLICY | Choose the simplest sufficient approach. |
| C016 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-POLICY | Make trade-offs explicit when more than one valid approach exists. |
| C017 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-POLICY | Define verification checkpoints before execution. |
| C018 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Keep the change surgical: every changed line must trace to the mission objective. |
| C021 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Write the minimum code that solves the requested problem. |
| C022 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Do not add features, abstractions, configurability, speculative optimization or unrelated refactors. |
| C023 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Match existing naming, file organization, error handling, import style, formatting and language conv |
| C024 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Use current, non-deprecated APIs and idiomatic patterns. |
| C026 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-CAVEAT | Handle realistic errors. Never swallow errors silently. |
| C030 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | Verify behavior and contracts, not implementation details. |
| C051 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | **Think Before Coding** — state assumptions; ask when uncertainty materially blocks safe execution;  |
| C052 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | **Simplicity First** — minimum code, no speculative architecture. |
| C053 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | **Surgical Changes** — no adjacent cleanup unless directly caused by this mission. |
| C057 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | **Dependencies and Imports** — reuse what exists; additions require rationale and verification. |
| C059 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-POLICY | **Testing** — test contracts/behavior; reproduce bugs first when possible. |
| C060 | T0 | disagree | REDUNDANT-GENERAL | 3/KEEP-POLICY | **Comments** — explain why; preserve correct existing comments. |
| C071 | T0 | disagree | REDUNDANT-GENERAL | 0/KEEP-POLICY | Record observations and measurable impacts, not opinions. |
| C093 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C096 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C099 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C105 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C108 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C111 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C117 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C120 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C129 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C135 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C138 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C141 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C144 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C147 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C162 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C168 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C174 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C195 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C201 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C204 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C207 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C213 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C216 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C219 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C225 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C231 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C243 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C246 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C261 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C267 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C270 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C276 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C297 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C300 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C306 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C312 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C315 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C318 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C324 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C327 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C342 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C360 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C369 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C375 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C381 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C384 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C387 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C390 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C393 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C396 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C399 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C402 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C408 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C411 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C414 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C420 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C426 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C429 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C435 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C444 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C450 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C453 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C462 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C465 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C471 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C477 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C480 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C486 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C495 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C501 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C504 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C513 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C519 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C525 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C528 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C531 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C546 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C552 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C564 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C567 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C576 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C579 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C582 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C585 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C600 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C606 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C609 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C612 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C624 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C627 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C636 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C639 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C648 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C651 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C660 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C675 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C687 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C696 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C705 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C708 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C714 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C717 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C723 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C726 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C729 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C732 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C744 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C747 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C750 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C756 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C762 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C765 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C774 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C780 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C783 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C786 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C798 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C801 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C804 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C813 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C819 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C837 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C852 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C855 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C861 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C867 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C873 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C879 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C882 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C885 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C891 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C894 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C900 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C903 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C906 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C912 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C915 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C927 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C930 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C936 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C939 | T1 | disagree | REDUNDANT-CODE | 3/KEEP-POLICY | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C951 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C969 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C975 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C987 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C990 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C993 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C996 | T1 | disagree | KEEP-POLICY | 1/REDUNDANT-CODE | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1000 | T1 | missing-score | — | — | Make pages citable by AI answer engines (GEO): schema, llms.txt, structure. Use for GEO or AI citabi |
| C1001 | T1 | missing-score | — | — | Read and follow `00_skills/(quality)/tlc-generative-engine-optimization/SKILL.md` and its relevant l |
| C1002 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1003 | T1 | missing-score | — | — | Implement planned work: extract a checklist, build it, prove each check. Use for 'build this ticket' |
| C1004 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/tlc-implement/SKILL.md` and its relevant local modules. |
| C1005 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1006 | T1 | missing-score | — | — | Turn a decided PRD or design doc into tasks with observable criteria. Use for task cutting. Do NOT u |
| C1007 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/tlc-plan/SKILL.md` and its relevant local modules. |
| C1008 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1009 | T1 | missing-score | — | — | Interview an idea into a PRD: problem, success, boundaries, journeys. Use for 'write the PRD'. Do NO |
| C1010 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/tlc-prd/SKILL.md` and its relevant local modules. |
| C1011 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1012 | T1 | missing-score | — | — | TLC spec-driven 4.0.0: specify, design, tasks, execute with EARS and proof checks. Use for feature s |
| C1013 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/tlc-spec-driven/SKILL.md` and its relevant local modules. |
| C1014 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1015 | T1 | missing-score | — | — | TLC spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for plan feature or  |
| C1016 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/tlc-spec-lean/SKILL.md` and its relevant local modules. |
| C1017 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1018 | T1 | missing-score | — | — | Prevent token waste with scoped prompts, compact context and narrow lenses. Use for token budget gov |
| C1019 | T1 | missing-score | — | — | Read and follow `00_skills/(learning)/token-budget-governor/SKILL.md` and its relevant local modules |
| C1020 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1021 | T1 | missing-score | — | — | Audit whether AEOS code and playbooks enforce Tool Router for external actions. Use for Tool Router  |
| C1022 | T1 | missing-score | — | — | Read and follow `00_skills/(tooling)/tool-router-audit/SKILL.md` and its relevant local modules. |
| C1023 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1024 | T1 | missing-score | — | — | Build AI features with TypeSafe models (Jev): typed judgments as code primitives. Use for programmab |
| C1025 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/typesafe-ai/SKILL.md` and its relevant local modules. |
| C1026 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1027 | T1 | missing-score | — | — | Audit an environment inventory for conflicting versions and unmet runtime needs. Use for environment |
| C1028 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/unique-environment-auditor/SKILL.md` and its relevant local |
| C1029 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1030 | T1 | missing-score | — | — | Plan and generate sandbox-first projects from zero to production for any stack. Use for project gene |
| C1031 | T1 | missing-score | — | — | Read and follow `00_skills/(creation)/universal-project-factory/SKILL.md` and its relevant local mod |
| C1032 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1033 | T1 | missing-score | — | — | Validate AEOS against v1.0 release gates and generate a blocking report. Use for v1 readiness checks |
| C1034 | T1 | missing-score | — | — | Read and follow `00_skills/(quality)/v1-readiness-auditor/SKILL.md` and its relevant local modules. |
| C1035 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1036 | T1 | missing-score | — | — | Deploy apps and websites to Vercel, including previews. Use for Vercel deploys or live links. Do NOT |
| C1037 | T1 | missing-score | — | — | Read and follow `00_skills/(cloud)/vercel-deploy/SKILL.md` and its relevant local modules. |
| C1038 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1039 | T1 | missing-score | — | — | Video-first cold outreach: personalized video at scale, async selling, AI demos. Use for video prosp |
| C1040 | T1 | missing-score | — | — | Read and follow `00_skills/(gtm)/video-outreach/SKILL.md` and its relevant local modules. |
| C1041 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1042 | T1 | missing-score | — | — | Voice interface for AEOS; activation is consent for authorized audio only. Use for voice input or tr |
| C1043 | T1 | missing-score | — | — | Read and follow `00_skills/(tooling)/voiceai/SKILL.md` and its relevant local modules. |
| C1044 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1045 | T1 | missing-score | — | — | Transcribe authorized bare audio offline with local Whisper. Use for offline transcription. Do NOT u |
| C1046 | T1 | missing-score | — | — | Read and follow `00_skills/(tooling)/vox-aurum/SKILL.md` and its relevant local modules. |
| C1047 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1048 | T1 | missing-score | — | — | Assess CVE and EOL risk. Use for CVE checks. Do NOT use for base sync, patching or invented versions |
| C1049 | T1 | missing-score | — | — | Read and follow `00_skills/(security)/vuln-obsol-recon/SKILL.md` and its relevant local modules. |
| C1050 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1051 | T1 | missing-score | — | — | Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performa |
| C1052 | T1 | missing-score | — | — | Read and follow `00_skills/(quality)/web-accessibility/SKILL.md` and its relevant local modules. |
| C1053 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1054 | T1 | missing-score | — | — | Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. |
| C1055 | T1 | missing-score | — | — | Read and follow `00_skills/(quality)/web-best-practices/SKILL.md` and its relevant local modules. |
| C1056 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1057 | T1 | missing-score | — | — | Review UI code against Web Interface Guidelines: visual and interaction patterns. Use for 'review my |
| C1058 | T1 | missing-score | — | — | Read and follow `00_skills/(design)/web-design-guidelines/SKILL.md` and its relevant local modules. |
| C1059 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1060 | T1 | missing-score | — | — | Multi-area web audit: performance, accessibility, SEO, best practices. Use for 'audit my site'. Do N |
| C1061 | T1 | missing-score | — | — | Read and follow `00_skills/(quality)/web-quality-audit/SKILL.md` and its relevant local modules. |
| C1062 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1063 | T1 | missing-score | — | — | Generate synthetic WhatsApp-style conversation fixtures for testing. Use for chat fixtures. Do NOT u |
| C1064 | T1 | missing-score | — | — | Read and follow `00_skills/(tooling)/whatsapp-simulator/SKILL.md` and its relevant local modules. |
| C1065 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1066 | T1 | missing-score | — | — | Staff-level WordPress super-skill: site mapping, clean-code changes, plugins, themes. Use for WordPr |
| C1067 | T1 | missing-score | — | — | Read and follow `00_skills/(development)/wordpress-expert/SKILL.md` and its relevant local modules. |
| C1068 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1069 | T1 | missing-score | — | — | Resolve the smallest compatible workbench profile from scope and constraints. Use for profile select |
| C1070 | T1 | missing-score | — | — | Read and follow `00_skills/(tooling)/workbench-profile-resolver/SKILL.md` and its relevant local mod |
| C1071 | T1 | missing-score | — | — | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |

## Review (KEEP family)

830 claims. See J1/J2 score tables for detail.

## Action guidance

- **T0 Ship:** edit always-on rules now.
- **T1 Ship:** skill cleanup backlog.
- **T2 Ship:** routing/pointer hygiene.
- **Hold:** do not trim.

