# CodENavi Continuity Standard

Version: 1.0.0  
Governance: CodENavi v1  
Owner: `codenavi-agent`

## Purpose

Every material workspace must preserve execution continuity without turning transient logs into permanent memory. The canonical quartet lives under `.notebook/`:

1. `HANDOFF.md`
2. `MEMORY.md`
3. `PROGRESS.md`
4. `LEARNING.md`

These files are complementary. Duplication is a defect; cross-link instead.

## HANDOFF.md

Use when work pauses, crosses a session boundary, changes operator/tooling context, or ends with remaining work.

Required sections:
- Objective
- Last verified state
- Working set / touched paths
- Decisions already made
- Blockers and risks
- Evidence pointers
- Exact next actions
- Validation still required
- Updated timestamp/date

Rules:
- compressed and executable, not a chronological diary;
- only the last verified state may be stated as fact;
- unfinished or uncertain items are labeled explicitly;
- do not copy full logs from `PROGRESS.md`;
- never include secrets or private chain-of-thought.

## MEMORY.md

Durable project memory contains only information expected to remain useful across future missions.

Eligible content:
- validated architectural decisions;
- stable invariants and constraints;
- verified environment/project facts;
- accepted user/product decisions;
- durable dependency/runtime compatibility facts;
- durable pointers to canonical docs/code.

Each entry includes:
- fact/decision;
- evidence/source pointer;
- rationale when a decision was made;
- status (`active`, `superseded`, `deprecated`);
- `Updated:` date.

Not eligible:
- current task status;
- speculative hypotheses;
- raw transcripts/logs;
- secrets, credentials or personal data;
- facts without evidence when evidence is reasonably obtainable.

## PROGRESS.md

`PROGRESS.md` is the live source of truth for the current mission.

Checklist states:
- `[ ]` pending
- `[~]` active
- `[x]` completed and verified
- `[!]` blocked

Required sections:
- Mission and success criteria
- Current phase
- Live checklist
- Verification gates/results
- Detailed factual log
- Open decisions/blockers
- Updated timestamp/date

Rules:
- update at meaningful step or batch boundaries;
- a task becomes `[x]` only after its acceptance gate is satisfied;
- log facts, commands/outcomes and evidence pointers; do not write hidden reasoning;
- preserve failed attempts when they materially explain the root cause or prevent repetition;
- when a mission ends, keep the final verified state until a new mission deliberately resets the file.

## LEARNING.md

Learning is promoted after verification, not during speculation.

Each learning entry includes:
- Context/trigger
- Failure mode or problem
- Root cause
- Verified correction or prevention
- Reuse scope / when the lesson applies
- Evidence pointers
- Confidence (`high`, `medium`, `low`)
- `Updated:` date

Promotion gate:
- the lesson is supported by observable evidence;
- it is more general than one transient task status;
- it does not duplicate a `MEMORY.md` invariant;
- it contains no secret or private chain-of-thought.

If a lesson becomes false, correct or deprecate it immediately.

## Lifecycle integration

- **BRIEFING:** read INDEX + MEMORY + current HANDOFF/PROGRESS; create missing quartet from templates.
- **RECON:** reconcile continuity files against repository evidence.
- **PLAN:** populate/update PROGRESS with measurable gates.
- **EXECUTE:** maintain PROGRESS continuously.
- **VERIFY:** close checklist items only with evidence.
- **DEBRIEF:** refresh HANDOFF, promote durable MEMORY, promote generalized LEARNING, repair stale entries.

## Templates

Canonical templates are stored in `templates/codenavi-continuity/`. New governed workspaces must materialize all four files under `.notebook/` before material work when they are absent.

## Safety

Continuity artifacts are repository/project state, not a secret store. They must never contain raw secrets, auth tokens, passwords, session cookies, private keys, personal data beyond what the repository already legitimately requires, or private chain-of-thought. Use opaque references and masked metadata when a sensitive dependency must be identified.

## Completion gate

A material mission is not continuity-complete when:
- `PROGRESS.md` contradicts the verified state;
- remaining work exists but `HANDOFF.md` does not state exact next actions;
- durable decisions were made but `MEMORY.md` remains stale;
- a reusable root-cause lesson was proven but `LEARNING.md` was not considered for promotion;
- any continuity file contains a secret or unsupported factual claim.
