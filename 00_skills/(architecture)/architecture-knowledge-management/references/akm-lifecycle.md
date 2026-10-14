# Architecture knowledge lifecycle

Load this file when auditing, setting up or improving how a team manages architectural knowledge. Evidence checked 2026-10-07.

## Contents

1. Scope of AKM
2. Decision management lifecycle
3. Knowledge placement
4. Knowledge audit checklist
5. Adoption model
6. Retroactive recovery (brownfield)
7. Review, revisit and reuse
8. AEOS integration
9. Sources

## 1. Scope of AKM

ADs, ASRs, ADRs and decision logs are all within Architectural Knowledge Management; ADR usage can extend to design and other decisions ("any decision record") (adr.github.io). Useful working definitions of an AD (OST AKM page): a decision you wish you could get right early (Fowler); a design decision that is costly to change (Booch); a decision that directly or indirectly determines the non-functional characteristics of a system, with several possible options and a rationale for the one chosen.

## 2. Decision management lifecycle

Five logical steps of architectural decision management and modeling (Zimmermann, Definition of Ready), mapped to the skills and artifacts that own them. The steps are logical, not strictly sequential; teams loop back when no favorite or no consensus emerges.

| Step | Activity | Gate | Owner skill | Artifact |
| --- | --- | --- | --- | --- |
| 1 | identify the design issue and its options | ASR Test | `architecturally-significant-requirement` | ASR register, decision backlog |
| 2 | collect criteria and analyze options | START (Definition of Ready) | `architecture-decision-record` | ADR draft, `proposed` |
| 3 | make the decision and reach agreement | ecADR E, C, A | `architecture-decision-record`, `the-jury` when contested | ADR `accepted` or `rejected` |
| 4 | capture the decision | ecADR D | `architecture-decision-record`, `architecture-decision-log` | ADR plus log index |
| 5 | enforce: implement, confirm, review | ecADR R | this skill | Confirmation, review trigger, code review referencing ADRs |

During code review, a change that violates an accepted ADR is sent back with a link to that ADR (AWS).

## 3. Knowledge placement

One home per knowledge item; every other place links to it.

| Knowledge | Home | Owner |
| --- | --- | --- |
| Architecturally significant requirements | the project's requirement tool, else `docs/architecture/asr-register.md` | `architecturally-significant-requirement` |
| Decisions and their rationale | ADRs in the decision log | `architecture-decision-record` |
| Overview of all decisions | the log index | `architecture-decision-log` |
| Pending decisions | decision backlog: open ASRs and `proposed` ADRs | this skill |
| Design detail behind a decision | TDD or architecture model linked from the ADR | `technical-design-doc-creator` |
| Durable project facts in AEOS | `.notebook/MEMORY.md`, holding pointers to ADR ids | `memory-curator` |
| Generalized lessons in AEOS | `.notebook/LEARNING.md` | `learning-curator` |

Store the log with the workload's documentation as a single source of truth for reference, audits and incident response (Azure WAF).

## 4. Knowledge audit checklist

Every finding cites its evidence. Deterministic items come from `architecture_knowledge.adl_index` (or `adl_index.mjs`) and `architecture_knowledge.asr_test`.

| Check | Evidence source | Typical finding |
| --- | --- | --- |
| A decision log exists and is discoverable | log locations in `architecture-decision-log` | no log, several competing logs |
| Log integrity | `integrity` findings | duplicate numbers, broken or circular supersession |
| Pending decisions are moving | `lifecycle.stale_proposals` | proposals older than the threshold |
| Decisions are dated | `lifecycle.undated` | records without a date |
| Accepted decisions are enforceable | `lifecycle.without_confirmation` | no Confirmation or validation plan |
| Decisions trace to ASRs | ADR decision drivers and links | rationale with no requirement behind it |
| Decisions exist that were never recorded | PR Why sections, commit messages, TDDs, `.notebook/MEMORY.md`, code structure | candidates for retroactive ADRs |
| Knowledge does not contradict itself | notes versus accepted ADRs | a memory note contradicts an accepted ADR |
| Revisit dates have not passed | review triggers and dates in ADRs | expired decisions never reviewed |

Prioritize findings H, M or L by the significance of the decisions involved.

## 5. Adoption model

Zimmermann and Anvaari (2023) define seven dimensions and five levels of architectural decision making and capturing.

Dimensions: usage scenario; scope and scale; structure and location; process and engagement (including timing and significance criteria); tool support and automation; review culture; learning.

| Level | Name | Signature |
| --- | --- | --- |
| 1 | Undefined and unconscious | decisions made intuitively; no ADRs or only free-form personal notes; no review |
| 2 | Ad-hoc and unstructured | some teams write ADRs after the fact; optional reviews; plain Markdown or wiki |
| 3 | Encouraged and supported | decisions on hard-to-reverse issues driven by significant concerns; minimal templates and light tools; reviews encouraged |
| 4 | Systematic, selective and diligent | decision identification is explicit; elaborate templates in a central repository linked to the issue tracker; mandatory reviews |
| 5 | Optimized and rigorous | proactive identification organization-wide from curated recurring concerns; global searchable repository; ADRs reused; enforced, type-aware reviews; part of training |

Assess the as-is level per dimension, then agree a to-be level. Not every team should aim for level 5: a single small agile team may be best served by levels 2 to 3, while a large regulated architect community may need level 5.

## 6. Retroactive recovery (brownfield)

Azure WAF recommends starting the record for brownfield workloads and generating it retroactively from known past decisions when the data is available.

1. Collect candidate decisions from evidence: PR descriptions and Why sections, commit messages, TDDs, runbooks, `.notebook/MEMORY.md` decisions and the code structure itself.
2. Triage each candidate with `architecturally-significant-requirement`; only significant ones become ADRs.
3. Write each with `architecture-decision-record`: date it with the capture date, state "retroactively captured from <evidence>", and write "rationale unknown" where no evidence exists. Never reconstruct motives.
4. Keep the record `proposed` until the decision owners confirm it, then accept it.

## 7. Review, revisit and reuse

- Every accepted decision states how compliance is confirmed and when it is revisited (ecADR R; MADR Confirmation). Revisit when the review date passes or when its context changes.
- Elaborate decision reviews include ATAM and DCAR (Zimmermann, Definition of Done).
- Reuse recurring decisions instead of re-deciding them: decision guidance models such as ADMentor and the Cloud Guidance Model (OST AKM), or the 29 recurring API design decisions in "Patterns for API Design" (adr.github.io).
- Core decisions with an early most responsible moment include the architectural style, supported technology stacks, integration options and the product governance structure (ECSA 2020 working session, reported by Zimmermann).

## 8. AEOS integration

- The continuity quartet keeps transient audit status in `PROGRESS.md`, transfer state in `HANDOFF.md`, durable facts in `MEMORY.md` and verified lessons in `LEARNING.md`. Decisions live in ADRs; `MEMORY.md` entries point to ADR ids instead of copying them.
- LCP `project-memory` rule: never contradict an existing ADR without an explicit deprecation or superseding record.
- This workspace's own log is `aeos/docs/adr/` (template `templates/ADR_TEMPLATE.md`, engine notes `knowledge/ADR_ENGINE.md`).
- `adr-decision-writer` produces evidence-only ADR candidates for enterprise reports under `.aeos/reports`; this skill decides which of them become records.

## 9. Sources

- adr.github.io: https://adr.github.io/
- OST Institute for Software, Architectural Knowledge Management (AKM): https://www.ost.ch/en/research-and-consulting-services/computer-science/ifs-institute-for-software-new/cloud-application-lab/architectural-knowledge-management-akm
- O. Zimmermann, M. Anvaari, "An Adoption Model for Architectural Decision Making and Capturing" (2023): https://ozimmer.ch/practices/2023/04/21/ADAdoptionModel.html
- O. Zimmermann, "A Definition of Ready for Architectural Decisions" (2023): https://ozimmer.ch/practices/2023/12/01/ADDefinitionOfReady.html
- O. Zimmermann, "A Definition of Done for Architectural Decision Making" (2020): https://www.ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html
- O. Zimmermann, "Architectural Significance Criteria and Some Core Decisions Required" (2020): https://www.ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html
- AWS Prescriptive Guidance, ADR process: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- Microsoft Azure WAF, Maintain an ADR: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
