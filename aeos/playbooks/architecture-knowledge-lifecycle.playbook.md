# Playbook: architecture-knowledge-lifecycle

## Required agent

- `codenavi-agent` only.

## Required skills

Select the matching skill; `architecture-knowledge-management` composes the other three.

- `architecturally-significant-requirement` — triage a requirement with the ASR Test; make it measurable
- `architecture-decision-record` — write, supersede or review one ADR; lint with `--strict`
- `architecture-decision-log` — index, next number, status transitions, integrity
- `architecture-knowledge-management` — knowledge placement, audits, adoption level, retroactive recovery

## Required LCPs

- `global-rules`
- `project-memory`
- `documentation-standards`

## Allowed MCPs

- `architecture-knowledge` — TLC progressive disclosure (`search_skills` → `read_skill` → `fetch_skill_files`) plus `adr_lint`, `adl_index`, `asr_test`, `concepts`, `sources`
- `filesystem-readonly`, `filesystem-write-sandbox`

## Flow

1. Identify: triage the requirement or issue with `architecturally-significant-requirement`.
2. Prepare: check START readiness; locate the log and the next number with `architecture-decision-log`.
3. Capture: write the ADR with `architecture-decision-record`; `adr_lint.mjs --strict` must exit 0.
4. Log: regenerate the index and rescan; no new error findings.
5. Enforce and revisit: record confirmation and a revisit trigger; audits and adoption plans go through `architecture-knowledge-management`.
6. Promote only pointers to accepted ADRs into `.notebook/MEMORY.md`.

## Failure policy

Rewriting or deleting an accepted ADR, reusing a number, inventing decision rationale, or creating another agent identity blocks completion.
