# Decision log conventions

Load this file when locating, creating, indexing or repairing a decision log. Evidence checked 2026-10-07.

## What the log is

The collection of ADRs created and maintained in a project constitutes its decision log (adr.github.io). It provides project context: readers skim the record titles for an overview and open single records for depth (AWS). The log is append-only: accepted records are not edited; a changed decision is a new record that supersedes the old one, and the two are linked (Azure WAF, AWS).

## Where logs live

Detect before creating. Common locations, in search order:

| Location | Filename pattern | Origin |
| --- | --- | --- |
| `docs/decisions/` | `NNNN-title-with-dashes.md` | MADR 4.0.0 |
| `docs/adr/` | `NNN-kebab-case-title.md` | TLC `create-adr` 1.0.0 |
| `doc/arch/` | `adr-NNN.md` | Nygard 2011 |
| `adr/`, `.adr/`, `architecture/decisions/` | varies | community tooling |
| `aeos/docs/adr/` | `ADR-NNNN-UPPER-KEBAB-TITLE.md` | this workspace (template `templates/ADR_TEMPLATE.md`) |

When no log exists, create `docs/decisions/` with MADR naming and four-digit numbers. Store the log with the system's documentation in the repository, so it is versioned with the code and reachable by every stakeholder (Nygard, Azure WAF).

## Numbering

- Numbers are sequential and monotonic, and are never reused, even after a record is deleted or a gap appears (Nygard). `adl_index.mjs` always proposes the highest number plus one.
- Keep one filename pattern and one number width per log; mixing them is reported as a warning.
- Large logs may use category subfolders (for example `decisions/backend/`, `decisions/ui/`); numbers are then unique per category only (MADR). Decide the categorization once, early, following the same structure as the code.

## Index

- The index is a generated table: ADR, title, status, date, superseded by. `adl_index.mjs --write-index <file>` rewrites only the block between `<!-- adl:index:start -->` and `<!-- adl:index:end -->`, creating the file when missing. Text outside the markers is preserved; a second run without changes writes nothing.
- The index file lives inside the log directory (usually its `README.md` or `index.md`); `README.md`, `index.md` and `adr-template*.md` are never treated as records.
- Never hand-edit rows inside the markers; fix the record and regenerate.

## Status transitions

| From | To | Change in the log |
| --- | --- | --- |
| (new) | proposed | new record |
| proposed | accepted | status and date on the same record (done criteria met) |
| proposed | rejected | status plus the reason for rejection on the same record |
| accepted | superseded | new record with `Supersedes ADR-NNNN`; old record status becomes `superseded by ADR-MMMM` |
| accepted | deprecated | status plus reason on the same record; no replacement |

Only the status line of an accepted record may change; its decision text stays as it was.

## Integrity findings

| Code | Severity | Meaning and repair |
| --- | --- | --- |
| `DUPLICATE_NUMBER` | error | two records share a number; renumber the newer, unmerged one |
| `SUPERSEDED_TARGET_MISSING` | error | the replacement named in the status does not exist; fix the reference or write the record |
| `SUPERSEDED_BY_SELF` | error | a record names itself as its replacement |
| `SUPERSESSION_CYCLE` | error | records supersede each other in a loop; one of them must stay current |
| `RECORD_LINT_ERRORS` | error | a record fails `adr_lint.mjs` (missing title, status, context, decision or consequences) |
| `FILE_TOO_LARGE` | error | record above 512 KiB; split detail into linked documents |
| `NUMBER_GAP` | warning | numbers are missing; keep the gap, never reuse it |
| `MIXED_FILENAME_PATTERNS`, `MIXED_NUMBER_WIDTH` | warning | more than one naming convention in one log |
| `SUPERSEDE_BACKLINK_MISSING` | warning | the new record does not link the record it supersedes |
| `SUPERSEDED_BY_INACTIVE` | warning | the replacement is rejected or deprecated |
| `STALE_PROPOSAL` | warning | proposed longer than the stale threshold (default 30 days); decide, reject or re-date it |

The lifecycle summary also lists current decisions (accepted, not superseded), undated records and accepted MADR records without a Confirmation section. `architecture-knowledge-management` uses these lists for knowledge audits.

## Sources

- adr.github.io: https://adr.github.io/
- MADR 4.0.0 (naming, categories): https://adr.github.io/madr/
- M. Nygard, "Documenting Architecture Decisions" (2011): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html
- AWS Prescriptive Guidance, ADR process: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- Microsoft Azure WAF, Maintain an ADR: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- adr.github.io tooling list (adr-log, Log4brains, adr-tools): https://adr.github.io/adr-tooling/
