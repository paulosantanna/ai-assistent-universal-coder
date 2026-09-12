---
name: learning-opportunities
description: "Assimilated TLC learning-opportunities 1.1.0. Offer optional 10-15 minute exercises after architectural work so the user practices instead of only consuming generated code. Triggers: learning exercise, help me understand, teach me, why does this work, after new files/modules. Do not use for urgent debugging, hotfixes, or when the user says just ship it."
---

# Learning Opportunities

Assimilated from installed `learning-opportunities` 1.1.0 (Chris Hicks / Felipe Rodrigues). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

After substantial design or new-module work, offer one short optional exercise (predict-then-observe, generate-then-compare, or teach-it-back). Pause after each question and wait for the user.

## Relationship to AEOS continuity

Session exercises are teaching, not durable project intelligence. Promote into `.notebook/LEARNING.md` only through `learning-curator` after a verified trigger, root cause, correction and evidence. Do not dump exercise transcripts into MEMORY.

## Activation

- User asks for a learning exercise, to understand the code, or "why does this work".
- After new files, schema changes, architectural refactors, or unfamiliar patterns — offer once, then wait.

## Non-activation

- User declined an exercise this session, already completed two, or said ship/hotfix/urgent.
- Pure debugging with no teaching request.

## Critical rules

1. Always ask first: one sentence, optional, ~10-15 minutes. Do not insist.
2. After a question: stop. No hints, suggested answers, or "think about...".
3. Be direct when the answer is wrong; then explore the gap.
4. Point the user at files before pasting code. Read `references/PRINCIPLES.md` when choosing a technique.
5. Follow types, anti-patterns and examples in `references/ORIGINAL_SKILL.md`.
6. Never persist secrets or private chain-of-thought in notebook artifacts.

## Continuity

At most two exercises per session. Offers stay optional.
