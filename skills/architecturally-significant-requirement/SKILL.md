---
name: architecturally-significant-requirement
description: 'Decides whether a requirement, change request or design issue is an Architecturally Significant Requirement (ASR), a requirement with a measurable effect on the architecture and quality of a system, using the seven-criteria ASR Test, then makes it specific and measurable as a quality attribute scenario and hands the decisions it drives to an ADR. Use when the user asks "is this architecturally significant", "ASR", "requisito arquiteturalmente significativo", "does this need an ADR", "architectural drivers", "quality attribute scenario" or "priorize os requisitos que impactam a arquitetura". Do NOT use for writing the ADR itself (use architecture-decision-record), for full feature specification (use spec-driven), or for threat modeling (use security-threat-model).'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# Architecturally Significant Requirement (ASR)

Governance: CodENavi v1. A skill of the single canonical `codenavi-agent`; it creates no other agent identity.

An ASR (Requisito Arquiteturalmente Significativo) is a requirement that has a measurable effect on the architecture and quality of a software and/or hardware system (adr.github.io). ASRs drive architectural decisions. This skill triages requirements with Olaf Zimmermann's seven-criteria ASR Test, makes significant ones measurable and routes their decisions to `architecture-decision-record`. `scripts/asr_test.mjs` makes the triage repeatable.

## Critical rules

1. Assess the requirement as its source states it; quote it and name the source. Never rewrite it into something easier to satisfy.
2. Give a rationale with evidence for every criterion you mark as met. Mark a criterion `?` when evidence is missing instead of guessing.
3. The test is qualitative triage, not a weight calculator. Never present weighted scores or decimals as precision.
4. A significant ASR needs a measurable formulation: a six-part quality attribute scenario for quality requirements, SMART criteria otherwise.
5. ASRs justify decisions; they are not decisions. Every design issue an ASR raises becomes its own ADR.
6. Ask only for facts that change the outcome; spend less time on relevance than on solving the issue.

## Workflow

### Step 1: Capture the requirement

Record the requirement text, its source (stakeholder, ticket, document) and the date. Split compound requirements first; assess each part separately.

### Step 2: Run the ASR Test

Answer the seven criteria with Y, N or ?, or H, M, L and n/a, and pass a count when a criterion applies several times. See `references/asr-test.md` for the criteria, value rules and examples.

| Id | Criterion |
| --- | --- |
| C1 | high business value or business risk |
| C2 | concern of a particularly important stakeholder |
| C3 | quality of service substantially beyond what the architecture already satisfies |
| C4 | unpredictable, unreliable or uncontrollable external dependency |
| C5 | cross-cutting, system-wide impact |
| C6 | first of a kind for this team |
| C7 | caused trouble on a similar past project |

Run `node skills/architecturally-significant-requirement/scripts/asr_test.mjs <input.json>` (or `-` for stdin), or the MCP tool `architecture_knowledge.asr_test`. Input: `requirement`, `criteria` keyed by id (`C1`) or key (`value_risk`), optional `rationale` and `scenario`.

### Step 3: Interpret

- `significant` (two or more criteria met): it is an ASR.
- `open` (unknowns could make it significant): resolve unknowns by asking, prototyping or a spike; keep it in the decision backlog.
- `borderline` (one criterion): team-level concern; an ADR is optional unless a hard-to-reverse decision follows.
- `not-significant`: handle in normal design and code review.

A `high` band also means the decisions it drives probably have an early most responsible moment.

### Step 4: Make it measurable

For quality requirements, write the six-part quality attribute scenario: source of stimulus, stimulus, environment, artifact, response, response measure. The script reports missing parts and whether the response measure is measurable. For other ASRs, state SMART acceptance criteria.

### Step 5: Record and hand off

Record the ASR with `assets/asr-record-template.md` where the project keeps requirements, or in `docs/architecture/asr-register.md` when no place exists. For each design issue it raises, hand off to `architecture-decision-record` with the ASR id as a decision driver.

### Step 6: Report

Return the significance, the criteria met with their rationale, the unknowns, the scenario status and the next steps.

## Examples

### Example 1: Regulatory retention

User says: "É arquiteturalmente significativo reter dados de clientes por 10 anos por exigência regulatória?"
Actions: C1 (fines), C2 (compliance auditor), C4 (archive storage provider), C5 (every data store) are met; run the script.
Result: band `high`, `significant`; next step is an ADR on the archival storage and hosting model, citing ASR-007.

### Example 2: Pipeline automation

User says: "Do we need an ADR for automating the deployment pipeline?"
Actions: only C5 is met (team-internal, cross-cutting).
Result: band `low-medium`, `borderline`; discuss with the team, no ADR unless a hard-to-reverse tool choice follows.

### Example 3: Unknown partner SLA

User says: "Partners will call our pricing API at 10,000 requests per minute; we do not know their retry behavior."
Actions: C1 met; C3 and C4 are `?`; write the scenario with response measure "p95 under 300 ms at peak".
Result: `open`; spike the partner retry behavior, then rerun the test.

## Troubleshooting

- `BLOCKED` with `UNKNOWN_CRITERION`: use ids C1 to C7 or the keys listed in `references/asr-test.md`.
- `BLOCKED` with `INVALID_CRITERION_VALUE`: use Y, N, ?, H, M, L, n/a, true, false or a non-negative count.
- Stakeholders disagree on a criterion: mark it `?`, record both positions in the rationale, and keep the ASR open.
- Everything looks significant: compare against the examples in `references/asr-test.md`; criteria C6 and C7 are context-specific and should not alone justify an ADR.
- `measurable_response: false`: replace adjectives such as "fast" with a threshold, unit and condition.

## Relationship to other skills

- `architecture-decision-record` records the decisions an ASR drives.
- `architecture-decision-log` keeps those decisions consistent over time.
- `architecture-knowledge-management` decides where ASRs live and how often they are revisited.
- `spec-driven` writes full feature requirements; this skill only triages their architectural significance.

## Continuity

The ASR register and the ADRs are the durable record. Promote to `.notebook/MEMORY.md` only a pointer to a verified, accepted ASR or decision, never the raw assessment.
