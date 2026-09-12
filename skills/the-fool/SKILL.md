---
name: the-fool
description: "Assimilated TLC critical-challenge skill (the-fool 2.0.0). Stress-test a plan, decision, or claim. Triggers: challenge this, devil's advocate, pre-mortem, red team, audit evidence, find blind spots. Do not use to build the plan or decide (the-jury decides)."
---

# The Fool

Assimilated from installed `the-fool` 2.0.0. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. Modes are internal lenses, not new agents.

## Mission

Steelman, then challenge. Five modes: Socratic assumptions, dialectic counter-argument, pre-mortem, red team, evidence audit. Critique only; do not implement the solution.

## Activation

- User wants a structured challenge, pre-mortem, red team, or evidence audit before committing.

## Non-activation

- Building the plan or writing the implementation.
- A verdict is required (`the-jury`).

## Critical rules

1. Steelman and confirm before challenging. Never strawman.
2. Select mode with the user when tools allow; otherwise pick from `references/mode-selection-guide.md` and say which mode ran.
3. Load the matching reference file before generating challenges.
4. Present 3-5 strongest challenges, then synthesize after the user responds.
5. Follow `references/ORIGINAL_SKILL.md` plus `references/cognitive-bias-inventory.md` on every pass.

## Lenses (never new agents)

- `SocraticLens` — `references/socratic-questioning.md`
- `DialecticLens` — `references/dialectic-synthesis.md`
- `PremortemLens` — `references/pre-mortem-analysis.md`
- `RedTeamLens` — `references/red-team-adversarial.md`
- `EvidenceAuditLens` — `references/evidence-audit.md`
