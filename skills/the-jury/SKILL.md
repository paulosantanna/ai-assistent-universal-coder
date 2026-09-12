---
name: the-jury
description: "Assimilated TLC decision panel (the-jury 1.0.0). Convene a 3-5 juror protocol and emit one verdict. Triggers: convene a jury, have agents debate and decide, get a panel to decide, monte um juri, tribunal de agentes. Do not use only to critique (the-fool) or to implement the solution."
---

# The Jury

Assimilated from installed `the-jury` 1.0.0 (Felipe Rodrigues / Tech Lead's Club). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. Jurors are sequential or parallel **lenses**, never spawned agent identities.

## Mission

Frame a decidable question, run a blind-then-deliberate panel of 3 or 5 orthogonal lenses, tally, and emit one verdict with dissent and a next action.

## Activation

- User asks for a jury, panel, multi-perspective decision, or "monte um júri".

## Non-activation

- Critique without a decision (`the-fool`).
- Building the plan or writing the code.
- Simple factual lookup.

## Critical rules

1. Do not register or spawn another agent. Simulate jurors as work units of `codenavi-agent`. Blind Round 1 before any juror sees another position.
2. Always emit a verdict. No abstention.
3. When Python can run, tally with `scripts/tally.py --input jury.json`.
4. Read `references/juror-archetypes.md` and `references/deliberation-craft.md` before assembly.
5. Follow the verdict block and flip/bandwagon rules in `references/ORIGINAL_SKILL.md`.

## Continuity

Promote only the accepted verdict and its riskiest assumption into `MEMORY.md` when they are durable project decisions.
