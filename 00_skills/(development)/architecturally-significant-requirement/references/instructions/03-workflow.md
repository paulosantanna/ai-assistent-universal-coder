<!-- Package: 00_skills/(development)/architecturally-significant-requirement; relative command/resource examples resolve from that package or workspace root. -->

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

Run `node "00_skills/(development)/architecturally-significant-requirement/scripts/asr_test.mjs" <input.json>` (or `-` for stdin), or the MCP tool `architecture_knowledge.asr_test`. Input: `requirement`, `criteria` keyed by id (`C1`) or key (`value_risk`), optional `rationale` and `scenario`.

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
