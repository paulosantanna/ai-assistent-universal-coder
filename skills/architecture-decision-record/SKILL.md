---
name: architecture-decision-record
description: 'Writes, supersedes and reviews one Architecture Decision Record (ADR), the record of a single architectural decision with its context, options, outcome and consequences, in MADR 4.0.0, Nygard or Y-statement format, then lints it. Use when the user says "write an ADR", "document this decision", "record why we chose X", "supersede ADR-0007", "review this ADR", "escreva um ADR", "registre a decisão arquitetural" or "crie um registro de decisão de arquitetura". Do NOT use for indexing or auditing the whole decision log (use architecture-decision-log), for judging whether a requirement is architecturally significant (use architecturally-significant-requirement), for an organization-wide decision practice (use architecture-knowledge-management), for making a still-open choice (use the-jury or technical-design-doc-creator), or for general documentation (use docs-writer).'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# Architecture Decision Record (ADR)

Governance: CodENavi v1. A skill of the single canonical `codenavi-agent`; it creates no other agent identity.

An Architectural Decision (AD) is a justified design choice that addresses an architecturally significant requirement. An ADR captures one AD and its rationale so a future reader knows what was chosen, why, and at what price (adr.github.io). This skill derives from TLC `create-adr` 1.0.0, preserved verbatim in `references/ORIGINAL_SKILL.md`, updated to MADR 4.0.0 and backed by a deterministic lint.

## Critical rules

1. One ADR records one decision. Its title is a noun phrase that states the decision, never a question.
2. Accepted and rejected ADRs are immutable. A changed decision is a new ADR that supersedes the old one; on the old record only the status line changes.
3. Never invent context, options, deciders or evidence. Ask, in the user's language, only for missing mandatory fields; state every assumption you make.
4. Follow the target log's existing directory, filename pattern, template and heading language. Defaults apply only when no log exists.
5. Write prose in the user's language; keep technical terms such as ADR, API and SLA in English.
6. Before delivering an authored ADR, `node skills/architecture-decision-record/scripts/adr_lint.mjs <file> --strict` must exit 0.
7. Never put secrets, credentials or personal data in an ADR.

## Workflow

### Step 1: Confirm the decision deserves an ADR

Record decisions that affect structure, non-functional characteristics, dependencies, interfaces or construction techniques. If significance is unclear, run `architecturally-significant-requirement` first and cite the ASR it returns. Cheap-to-change, stakeholder-invisible choices get no ADR.

### Step 2: Check readiness and mandatory fields

Apply the START checklist from `references/adr-practices.md`: stakeholders, time (most responsible moment), alternatives, requirements, template. Mandatory fields: title, date (YYYY-MM-DD), status, context, decision, consequences with at least one negative. Recommended: decision drivers, considered options with pros and cons, decision makers, consulted, informed, confirmation, links.

If options and drivers exist but agreement does not, write the ADR as `proposed`. If no options or criteria exist, stop and route the decision to `the-jury` or `technical-design-doc-creator`.

### Step 3: Locate the log and the next number

Use `architecture-decision-log` (or the MCP tool `architecture_knowledge.adl_index` with `next_title`) to find the log, its convention and the next free number. Look in `docs/decisions/`, `docs/adr/`, `doc/arch/`, `adr/`, `.adr/` and, in this workspace, `aeos/docs/adr/`. With no log, start `docs/decisions/0001-title-with-dashes.md` (MADR). Never reuse a number.

### Step 4: Choose the format

| Format | Use when | Template |
| --- | --- | --- |
| MADR 4.0.0 (default) | options are compared; most decisions | `assets/madr-template.md`, or `assets/madr-template-minimal.md` for small decisions |
| Nygard | the log already uses it, or the decision is small and obvious | `assets/nygard-template.md` |
| Y-statement | one compact paragraph, e.g. inline design notes | `assets/y-statement-template.md` |
| AEOS workspace template | the target log is `aeos/docs/adr/` | `templates/ADR_TEMPLATE.md` |

### Step 5: Write the record

- Context: two to four value-neutral sentences that name the forces in tension and link the ASRs.
- Options: real alternatives only, including "do nothing" when it is viable. Justify a single viable option instead of inventing a dummy one.
- Outcome: `Chosen option: "X", because <justification tied to the drivers>`.
- Consequences: `Good, because ...` and `Bad, because ...`; at least one honest Bad.
- Confirmation: how compliance will be checked (review, test, fitness function) and when the decision is revisited.
- Disclose confidence. Keep the ADR within one to two pages and link design detail instead of embedding it.

Read `references/adr-practices.md` sections 4 and 5 for good practices and anti-patterns before finalizing.

### Step 6: Apply lifecycle transitions

- `proposed` to `accepted`: all ecADR done criteria hold; add the date and the decision makers.
- `proposed` to `rejected`: keep the record and add the reason for rejection.
- Superseding: write the new ADR with a `Supersedes ADR-NNNN` link, then change only the old record's status to `superseded by ADR-MMMM` with a link.
- `deprecated`: the decision no longer applies and has no replacement; state why.

### Step 7: Lint and self-review

Run `node skills/architecture-decision-record/scripts/adr_lint.mjs <file> --strict`, or the MCP tool `architecture_knowledge.adr_lint` with `strict: true`. Fix every error, then answer the seven review questions in `references/adr-practices.md` section 7.

### Step 8: Deliver

Save the file at the path from Step 3, refresh the index with `architecture-decision-log`, and report the path, number, status and what remains to confirm. Do not commit unless the user asked for it.

## Review mode

When asked to review an ADR, lint it without `--strict` for template conformance, then review content with the seven questions and the ecADR criteria. Report prioritized finding-recommendation pairs. Never rewrite an accepted ADR; propose a superseding one.

## Examples

### Example 1: New decision in Portuguese

User says: "Escreva um ADR: decidimos usar PostgreSQL em vez de MongoDB no serviço de pedidos."
Actions: confirm significance (transactions, external dependency); check START; find `docs/decisions/` with next number 0004; fill the MADR template in Portuguese; lint with `--strict`; refresh the index.
Result: `docs/decisions/0004-usar-postgresql-no-servico-de-pedidos.md`, status `accepted`, lint PASS.

### Example 2: Supersede a decision

User says: "We are moving sessions from PostgreSQL to Redis, supersede ADR-0002."
Actions: write ADR-0007 with `Supersedes ADR-0002`; change only ADR-0002's status to `superseded by ADR-0007`; lint both; the log index shows the chain.
Result: two consistent records; ADR-0002's decision text is unchanged.

### Example 3: Review

User says: "Review ADR-0012 before the architecture board."
Actions: non-strict lint; seven review questions; ecADR check.
Result: findings table with H/M/L priority and one recommendation per finding.

## Troubleshooting

- `TITLE_IS_QUESTION`: rewrite the title as the decision, e.g. "Use Redis for session storage".
- `CONSEQUENCES_MISSING` or `NO_NEGATIVE_CONSEQUENCE`: add the real trade-offs (Free Lunch Coupon anti-pattern).
- `PLACEHOLDER_LEFT`: replace or delete the remaining template guidance in braces.
- `UNRECOGNIZED_FORMAT`: restructure the record with one of the templates in Step 4.
- `DATE_MISSING` on a retroactive record: use the capture date and state the known origin of the decision.
- The user wants to edit an accepted ADR: explain immutability and offer a superseding ADR or a status-only change.
- The log index reports a duplicate number: renumber the newer, unmerged ADR; never renumber accepted ones.

## Relationship to other skills

- `architecturally-significant-requirement` decides whether an ADR is warranted; cite its ASR ids in the drivers and links.
- `architecture-decision-log` owns numbering, the index, integrity checks and supersession chains.
- `architecture-knowledge-management` owns the practice: where knowledge lives, review cadence and adoption.
- `adr-decision-writer` emits evidence-only ADR candidates for enterprise reports; this skill authors the record itself.
- `technical-design-doc-creator` holds design detail that an ADR links to; `the-jury` settles a contested decision before it is recorded.

## Continuity

ADRs are the durable decision record. `.notebook/MEMORY.md` may point to an ADR but never copies it, and no memory entry may contradict an accepted ADR without an explicit superseding or deprecating record (`project-memory` LCP).

## Provenance and licenses

- Workflow baseline: TLC `create-adr` 1.0.0 by Tech Leads Club (github.com/tech-leads-club), CC-BY-4.0, kept in `references/ORIGINAL_SKILL.md`. Changes: MADR 4.0.0 structure, rejected status, START and ecADR gates, deterministic lint and AEOS governance; see `references/adr-practices.md` section 9.
- MADR 4.0.0 templates in `assets/`: MIT OR CC0-1.0, used under CC0-1.0. Nygard structure: Cognitect CC0 waiver.
