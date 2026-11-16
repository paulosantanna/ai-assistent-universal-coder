# Harness Eval: Judge Agreement (Track B)

> Run dir: `/agent/repos/ai-assistent-universal-coder/.harness-eval/runs/2026-11-13-full`
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

- Real claims scored: 1014
- Ship: **0**
- Review: **1010**
- Hold: **4**
- Trap misses: none

## Discrimination (plants)

| ID | Expected family | J2 family |
|----|-----------------|-----------|
| P003 | REDUNDANT | REDUNDANT |
| P004 | REDUNDANT | REDUNDANT |
| P005 | KEEP | KEEP |
| P006 | KEEP | KEEP |

Ship by tier: {}
Hold by tier: {'T1': 4}

## Ship

| ID | Tier | Source | J1 | J2 cost/class | Quote |
|----|------|--------|----|---------------|-------|

## Hold

| ID | Tier | Reason | J1 | J2 | Quote |
|----|------|--------|----|----|-------|
| C733 | T1 | disagree | KEEP-COMPRESSED | 1/REDUNDANT-GENERAL | Review pull requests as an independent evidence-based reviewer. Use when the user requests pr review |
| C736 | T1 | disagree | KEEP-COMPRESSED | 1/REDUNDANT-GENERAL | Perform severity-ranked, evidence-backed PR review. Use when the user requests pr reviewer advanced  |
| C748 | T1 | disagree | KEEP-COMPRESSED | 1/REDUNDANT-GENERAL | Analyze Python AI/RAG systems for production readiness. Use when the user requests python ai product |
| C811 | T1 | disagree | KEEP-COMPRESSED | 1/REDUNDANT-GENERAL | Implement, diagnose, modernize and migrate real Rust projects with version-correct APIs, minimal dif |

## Review (KEEP family)

1010 claims. See J1/J2 score tables for detail.

## Action guidance

- **T0 Ship:** edit always-on rules now.
- **T1 Ship:** skill cleanup backlog.
- **T2 Ship:** routing/pointer hygiene.
- **Hold:** do not trim.

