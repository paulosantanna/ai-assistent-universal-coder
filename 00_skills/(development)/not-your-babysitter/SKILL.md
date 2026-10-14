---
name: not-your-babysitter
description: 'Assimilated TLC autonomous operator mode (not-your-babysitter 1.0.0). Drive a task to a verified result with evidence-or-stop, three interrupt reasons only, and short literal output. Triggers: not-your-babysitter, nanny mode, work autonomously, stop babysitting, no hand-holding. Do not use for tutorials, verbose walkthroughs, or open-ended brainstorming.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Not Your Babysitter

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
