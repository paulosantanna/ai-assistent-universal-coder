<!-- Package: 00_skills/(architecture)/architecture-decision-record; relative command/resource examples resolve from that package or workspace root. -->

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

Run `node "00_skills/(architecture)/architecture-decision-record/scripts/adr_lint.mjs" <file> --strict`, or the MCP tool `architecture_knowledge.adr_lint` with `strict: true`. Fix every error, then answer the seven review questions in `references/adr-practices.md` section 7.

### Step 8: Deliver

Save the file at the path from Step 3, refresh the index with `architecture-decision-log`, and report the path, number, status and what remains to confirm. Do not commit unless the user asked for it.
