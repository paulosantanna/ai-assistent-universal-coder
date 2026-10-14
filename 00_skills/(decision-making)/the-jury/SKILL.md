---
name: "the-jury"
description: "Evaluate a decidable question through 3 or 5 orthogonal sequential lenses of codenavi-agent, then tally a verdict with dissent and evidence. Use for monte um júri, painel de decisão or compare options through multiple perspectives. Do NOT use to spawn agents, claim independent cognition, merely critique (the-fool) or implement the decision."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# the-jury

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Frame a decidable question/options, 2–4 rubric criteria, shared evidence and confidence rule. Read retained juror-archetypes and deliberation-craft for applicable methods.
2. Use [juror lens](lenses/the-jury.md) for each of 3 or 5 orthogonal perspectives: strongest proponent, strongest opponent, integrator and justified domain lenses. All are sequential procedures of codenavi-agent, not new identities.
3. Record every Round 1 position, 2–4 concrete arguments, A/B/C/D evidence grade, assumptions and 0–100 confidence before synthesis. Avoid relying on earlier lens opinions; disclose that true context isolation is unavailable.
4. In Round 2, use anonymized positions, steelman the strongest opposition, rebut concretely, name falsifying evidence and examine one bias. Revise only for cited new argument/evidence; log reason for flip.
5. Use scripts/tally.py against its documented input schema to tally, then present one verdict, dissent, riskiest assumption and next action. Missing evidence remains explicit; a procedural verdict is not approval to act.

Input: frame/rubric/evidence. Output: recorded lens opinions and deterministic tally with uncertainty. Source: IMG_2771–IMG_2772. Do not spawn/register agent profiles or equate self-review with independent adjudication.

## Examples and failure handling

Example: “compare migrate versus tune through a jury” → record three orthogonal positions, anonymized deliberation, cited flips and deterministic tally. Failure: missing evidence → keep its grade/confidence low and disclose the gap; no spawned panel or implicit authorization.

## Retained resources

- Read [retained deliberation-craft](references/deliberation-craft.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained juror-archetypes](references/juror-archetypes.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained ORIGINAL_SKILL](references/ORIGINAL_SKILL.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained package-notes](references/package-notes.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained tlc](references/tlc) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
