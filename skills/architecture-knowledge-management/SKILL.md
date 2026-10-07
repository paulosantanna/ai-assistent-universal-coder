---
name: architecture-knowledge-management
description: 'Governs Architecture Knowledge Management (AKM) across ASRs, ADRs and the decision log: decides where architectural knowledge lives, audits it for missing, stale, contradictory or unrecorded decisions, assesses the team on the five-level decision adoption model, recovers past decisions from brownfield evidence, and plans review and reuse. Use when the user says "architecture knowledge management", "AKM", "gestão do conhecimento arquitetural", "audit our architecture decisions", "nobody knows why we chose X", "set up an ADR practice", "decision backlog" or "recuperar decisões de um sistema legado". Do NOT use for writing one ADR (use architecture-decision-record), for maintaining the log index (use architecture-decision-log), for triaging one requirement (use architecturally-significant-requirement), or for general project memory curation (use memory-curator).'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# Architecture Knowledge Management (AKM)

Governance: CodENavi v1. A skill of the single canonical `codenavi-agent`; it creates no other agent identity.

ADs, ASRs, ADRs and decision logs all sit within Architectural Knowledge Management (adr.github.io). This super-skill composes `architecturally-significant-requirement` (identify), `architecture-decision-record` (capture) and `architecture-decision-log` (log), and owns what none of them covers: where knowledge lives, audits, adoption level, retroactive recovery, review cadence and reuse. It has no script of its own; it reads their deterministic outputs through the `architecture-knowledge` MCP. Read `references/akm-lifecycle.md` before Step 2.

## Critical rules

1. One home per knowledge item; every other place links to it.
2. Every audit finding cites a file, record or tool output. Never invent the rationale of a past decision; write "rationale unknown".
3. Recommend the adoption level that fits the context; more process is not better by default.
4. Delegate: requirements to the ASR skill, records to the ADR skill, the index to the ADL skill. Never duplicate their work.
5. Retroactive ADRs are labeled as retroactive, dated with the capture date, and stay `proposed` until the decision owners confirm them.
6. Shared knowledge never contains secrets, personal data or confidential contract terms.

## Workflow

### Step 1: Frame the request

Name the system, the teams and the question: audit, setup of a decision practice, recovery of past decisions, or adoption assessment. State assumptions about scope.

### Step 2: Inventory the knowledge

Locate decision logs (`architecture-decision-log` locations), the ASR register, TDDs, PR Why sections and, in AEOS workspaces, `.notebook/MEMORY.md`. Scan each log with `architecture_knowledge.adl_index` (or `node skills/architecture-decision-log/scripts/adl_index.mjs <dir>`). Map what you found onto the placement table in `references/akm-lifecycle.md` section 3.

### Step 3: Audit

Run the checklist in `references/akm-lifecycle.md` section 4. Use `integrity` for log defects and `lifecycle.stale_proposals`, `lifecycle.undated` and `lifecycle.without_confirmation` for lifecycle gaps. Compare notes and memory entries with accepted ADRs for contradictions. Prioritize findings H, M or L.

### Step 4: Assess adoption

Rate the seven dimensions of the adoption model (usage scenario, scope and scale, structure and location, process and engagement, tool support and automation, review culture, learning). Report the as-is level, a justified to-be level and the smallest practice changes that reach it.

### Step 5: Recover unrecorded decisions

For brownfield systems, list candidate decisions from evidence, triage them with `architecturally-significant-requirement` and write the significant ones with `architecture-decision-record` following `references/akm-lifecycle.md` section 6.

### Step 6: Plan review and reuse

Give every accepted decision a confirmation method and a revisit trigger. Identify recurring decisions worth a reusable guidance entry and core decisions whose most responsible moment is now.

### Step 7: Report

Deliver findings with evidence and priority, the placement map, the adoption assessment and an action plan where each action names the skill that executes it. Keep transient audit status in `.notebook/PROGRESS.md`.

## Examples

### Example 1: Audit this workspace

User says: "Faça uma auditoria do conhecimento arquitetural deste repositório."
Actions: scan `aeos/docs/adr/`; read `.notebook/MEMORY.md`; run the checklist.
Result: one `proposed` ADR without a date; several durable decisions in `MEMORY.md` (for example the single-agent identity and the Python workspace policy) with no ADR, listed as retroactive candidates; adoption level 2 to 3 with a plan to triage the candidates and confirm ADR-0001.

### Example 2: Start a decision practice

User says: "We want to start using ADRs in our team."
Actions: pick the log location and MADR 4.0.0; adopt the ASR Test for triage, START and ecADR for readiness and done, one review mode, and index regeneration in CI or review.
Result: a one-page practice proposal targeting adoption level 3, with the first ADR recorded as an example.

### Example 3: Nobody knows why

User says: "Why did we choose Kafka? Nobody remembers."
Actions: search PRs, commits, TDDs and runbooks for evidence; triage the decision; write a retroactive ADR.
Result: a `proposed` retroactive ADR citing its evidence, with "rationale unknown" where nothing was found and a request to the original owners to confirm it.

## Troubleshooting

- No decision log exists: switch from audit to setup (Example 2).
- Rationale cannot be found: record it as unknown with low confidence; do not reconstruct motives.
- Teams resist the practice: choose the lowest adoption level that removes the stated pain and start with a single ADR.
- A memory note contradicts an accepted ADR: the ADR stands until a superseding or deprecating record exists; correct the note.
- Too many candidate decisions: triage with the ASR Test; only significant ones become ADRs.
- `adl_index` fails with `SCAN_FAILED`: point it at the log directory, not the repository root.

## Relationship to other skills

- Composes `architecturally-significant-requirement`, `architecture-decision-record` and `architecture-decision-log`.
- `memory-curator` and `learning-curator` keep durable facts and lessons; decisions themselves stay in ADRs.
- `technical-design-doc-creator` holds design detail; `the-jury` settles contested decisions; `adr-decision-writer` emits evidence-only ADR candidates for enterprise reports.

## Continuity

Audit results are transient and go to `.notebook/PROGRESS.md`. Durable decisions go to ADRs; `.notebook/MEMORY.md` holds only pointers to them.
