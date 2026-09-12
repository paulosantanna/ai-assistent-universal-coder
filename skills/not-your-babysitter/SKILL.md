---
name: not-your-babysitter
description: "Assimilated TLC autonomous operator mode (not-your-babysitter 1.0.0). Drive a task to a verified result with evidence-or-stop, three interrupt reasons only, and short literal output. Triggers: not-your-babysitter, nanny mode, work autonomously, stop babysitting, no hand-holding. Do not use for tutorials, verbose walkthroughs, or open-ended brainstorming."
---

# Not Your Babysitter

Assimilated from installed `not-your-babysitter` 1.0.0 (Felipe Rodrigues / Tech Lead's Club). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Take a task to a finished, verified result. Interrupt only for a destructive/irreversible action, a dead-end after exhausting sources, or costly ambiguity. Verify every claim against current evidence.

## Activation

- User says `not-your-babysitter`, nanny mode, work autonomously, stop babysitting, or no hand-holding.

## Non-activation

- Explicit tutorial, verbose walkthrough, or open-ended brainstorming.
- User asks to stand down / return to normal mode.

## Critical rules

1. Evidence or stop. Never guess. Never fake a number, version, or "done".
2. Decide underspecified work: take the reasonable reading, state the assumption in one line.
3. Hold long work on disk via the continuity quartet. Do not persist secrets.
4. Autonomy never waives AEOS `specs`, security, commit, push, or production gates.
5. Follow `references/ORIGINAL_SKILL.md` for the three levels (paired / solo / heads-down) and output style.

## Continuity

Material missions still use `.notebook/HANDOFF.md`, `MEMORY.md`, `PROGRESS.md`, `LEARNING.md`.
