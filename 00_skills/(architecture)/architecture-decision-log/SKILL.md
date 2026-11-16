---
name: architecture-decision-log
description: "Maintain the ADR log: next number, index, statuses, integrity. Use for ADR index work. Do NOT use to write one ADR (architecture-decision-record)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Architecture Decision Log (ADL)

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

The collection of ADRs created and maintained in a project constitutes its decision log (adr.github.io). The log is append-only: decisions change through superseding records, never through edits. This skill keeps the log navigable and consistent. `scripts/adl_index.mjs` does the deterministic work and imports the ADR parser of the sibling skill `architecture-decision-record`, so both skills always agree on what a record contains.

## Critical rules

1. Detect the existing log and its convention before creating anything. Never introduce a second naming pattern into an existing log.
2. Numbers are never reused. The next number is the highest existing number plus one, even when gaps exist.
3. Never change an accepted record's decision text. Status transitions follow the table in `references/log-conventions.md`.
4. Regenerate the index with the script; never hand-edit the rows between the index markers.
5. Writes are limited to the index block inside the log directory and to record status lines. Commits require explicit approval.
6. Report integrity findings with file evidence. Never repair a log by deleting records.

## Workflow

### Step 1: Locate the log

Search `docs/decisions/`, `docs/adr/`, `doc/arch/`, `adr/`, `.adr/`, `architecture/decisions/` and, in this workspace, `aeos/docs/adr/`. If several exist, ask which one is authoritative before writing. With no log, propose `docs/decisions/` with MADR naming; create it only together with the first record.

### Step 2: Scan

Run `node "00_skills/(architecture)/architecture-decision-log/scripts/adl_index.mjs" <log-dir> --today <YYYY-MM-DD>`, or the read-only MCP tool `architecture_knowledge.adl_index` with `directory`. The JSON result holds `records` (id, title, status, date, superseded_by, format, lint codes), `integrity` findings, the `lifecycle` summary, `index_markdown` and, when `--next` or `next_title` is given, the `next` record. Exit code 1 means at least one error-level finding.

### Step 3: Act on the request

- What is decided: report `lifecycle.current_decisions` with titles, then supersession chains and pending proposals.
- Next number: add `--next "<decision title>"`; hand the id and file name to `architecture-decision-record`.
- Status transition: apply the table in `references/log-conventions.md`. Acceptance requires the ecADR done criteria checked by `architecture-decision-record`.
- Repair: follow the repair column of the integrity table in `references/log-conventions.md`.

### Step 4: Regenerate the index

Run the scan again with `--write-index <log-dir>/README.md` (or the log's existing index file). The script replaces only the block between `<!-- adl:index:start -->` and `<!-- adl:index:end -->` and writes nothing when the index is already current.

### Step 5: Verify and report

Rescan. Report counts by status, current decisions, every remaining finding with its file and why it remains, and the index path.

## Examples

### Example 1: What is currently decided

User says: "Quais decisões de arquitetura estão vigentes?"
Actions: locate `docs/decisions/`; scan with today's date; read `lifecycle`.
Result: ADR-0003 and ADR-0005 are accepted; ADR-0001 is superseded by ADR-0003; ADR-0002 has been proposed since 2026-08-01 (`STALE_PROPOSAL`) and needs a decision.

### Example 2: Next number

User says: "Next ADR number for adopting OpenTelemetry tracing."
Actions: scan with `--next "Adopt OpenTelemetry tracing"`.
Result: `ADR-0006`, file `0006-adopt-opentelemetry-tracing.md`; in `aeos/docs/adr/` the same request yields `ADR-0002-ADOPT-OPENTELEMETRY-TRACING.md`.

### Example 3: Accept a proposal

User says: "Accept ADR-0002."
Actions: confirm the ecADR criteria with `architecture-decision-record`; change the status to accepted and set the date; rescan; regenerate the index.
Result: the index row shows `accepted`; `STALE_PROPOSAL` disappears.

## Troubleshooting

- Exit code 2 with `SCAN_FAILED`: the path is not a directory or holds more than 2000 records; point at the log directory, not the repository root.
- No records found: file names match no supported pattern; check the `ignored` list and ask before renaming anything.
- `DUPLICATE_NUMBER` after merging two branches: renumber the record that is not yet accepted and update its links.
- `SUPERSEDED_TARGET_MISSING`: the status names a record that does not exist; correct the reference or write the superseding record first.
- `RECORD_LINT_ERRORS`: lint the record with `architecture-decision-record` and fix it there.
- Category subfolders: numbers are unique per folder; scan the subfolder itself to get its next number, or pass `next_category` to the MCP tool.

## Relationship to other skills

- `architecture-decision-record` writes single records and owns the ADR parser this skill reuses.
- `architecturally-significant-requirement` explains why a record exists; cite ASR ids from records, not from the index.
- `architecture-knowledge-management` turns the `lifecycle` summary into a knowledge audit and an improvement plan.

## Continuity

The log is the source of truth for decisions. `.notebook/MEMORY.md` points to the log and to individual ADR ids; it never duplicates their content.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
