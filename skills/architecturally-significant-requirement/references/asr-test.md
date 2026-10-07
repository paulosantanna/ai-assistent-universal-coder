# ASR Test and quality attribute scenarios

Load this file when triaging requirements for architectural significance or when making an ASR measurable. Evidence checked 2026-10-07.

## Definitions

- An Architecturally Significant Requirement (ASR), in Portuguese a Requisito Arquiteturalmente Significativo, is a requirement that has a measurable effect on the architecture and quality of a software and/or hardware system (adr.github.io).
- An architectural decision is a justified design choice that addresses an architecturally significant requirement; ASRs therefore drive and justify ADRs. Unsatisfied ASRs accumulate technical debt (Wikipedia, citing Chen, Ali Babar and Nuseibeh 2013).
- Not every non-functional requirement is architecturally significant, and functional requirements can be (empirical studies summarized by Wikipedia: Chen et al. 2013; Eckhardt, Vogelsang and Fernández 2016).
- The test applies to requirements and change requests, and also to pending design decisions and structural elements such as components and connectors (Zimmermann).

## The seven criteria

From Zimmermann, "Architectural Significance Criteria and Some Core Decisions Required" (ECSA 2020 working sessions). A requirement is likely an ASR when it:

| Id | Key | Criterion |
| --- | --- | --- |
| C1 | `value_risk` | is directly associated with high business value (benefit versus cost) or business risk |
| C2 | `key_concern` | is a concern of a particularly important stakeholder, such as the project sponsor or an external compliance auditor |
| C3 | `new_qos` | includes runtime quality-of-service characteristics, such as performance, that deviate substantially from those the evolving architecture already satisfies |
| C4 | `external_dependency` | causes new, or deals with existing, external dependencies with unpredictable, unreliable or uncontrollable behavior; dependencies may be compile time, runtime or organizational |
| C5 | `cross_cutting` | has a cross-cutting nature and affects several parts of the system and their interactions, possibly system-wide (for example security, monitoring) |
| C6 | `first_of_a_kind` | has a first-of-a-kind character: the team has never built a component that satisfies it |
| C7 | `past_problems` | has been troublesome and caused critical situations, budget overruns or client dissatisfaction on a previous project in a similar context |

C1 to C5 are more objective and easier to agree upon; C6 and C7 are highly context-specific. The order is outside-in and does not imply weight.

## Values and counting

- Cell values: Y (yes), N (no), ? (unknown), or the more elaborate H, M, L and n/a. `asr_test.mjs` counts Y, H and M as met; N, L and n/a as not met; ? and unassessed criteria as unknown.
- One criterion may apply several times; pass a count (for example `"external_dependency": 2` when two new public APIs must be consumed). The count is reported as `instances`; the band counts distinct criteria.
- When significance cannot be agreed immediately, mark it open and track it as a backlog item or in a parking lot reviewed periodically.

## Interpreting the result

The ASR Test is not a quantitative tool or weight calculator; relevance assessments are qualitative, subjective and context-dependent, and the test makes tacit knowledge explicit ("worst first"). Do not spend more time assessing relevance than solving issues.

Zimmermann's published examples, which the band mapping of `asr_test.mjs` reproduces:

| Requirement | Criteria met | Band |
| --- | --- | --- |
| Data retention policy of 10 years for regulatory compliance | C1, C2, C4, C5 | high |
| Technical constraint to prefer a particular messaging middleware and backend API | C2, C3 | medium-high |
| Deployment pipeline automation | C5 | low-medium |
| Name of a Java class wrapping access to a backend | none | low |

Mapping: 0 criteria met is `low`, 1 is `low-medium`, 2 or 3 is `medium-high`, 4 or more is `high`. Significance: two or more criteria met is `significant`; fewer, but enough unknowns to reach two, is `open`; exactly one is `borderline`; none is `not-significant`. A `high` band also signals an early most responsible moment for the decisions the ASR drives (Zimmermann, Definition of Ready).

## Characteristics and heuristics

From Chen, Ali Babar and Nuseibeh (2013), as summarized by Wikipedia:

- Descriptive characteristics: ASRs are often hard to define and articulate, expressed vaguely, initially neglected, hidden within other requirements, and subjective, variable and situational.
- Indicators: a broad effect, targeting trade-off points, strictness (constraining, limiting, non-negotiable), assumption-breaking, or being difficult to achieve.
- Heuristics: requirements that specify quality attributes, refer to core features, impose constraints or define the runtime environment are likely architecturally significant.

## Making an ASR specific and measurable

ASRs should be SMART. Quality attribute scenarios achieve the specific and measurable parts. A scenario has six parts (Bass, Clements and Kazman; Ozkaya, Bass, Nord and Sangwan 2008):

| Part | Meaning |
| --- | --- |
| Source of stimulus | the entity (human, system, actuator) that generates the stimulus |
| Stimulus | the condition that arrives at the system |
| Environment | the conditions under which it occurs (normal load, overload, degraded mode) |
| Artifact | the part of the system that is stimulated, often the whole system |
| Response | the activity undertaken after the stimulus arrives |
| Response measure | how the response is measured so that the requirement can be tested |

`asr_test.mjs` checks that all six parts are present and that the response measure is measurable (contains a number or an explicit zero). The SEI recommends Quality Attribute Workshops to elicit scenarios; utility trees prioritize them by business value and technical difficulty, for example (H, H) first.

## From ASR to decision

1. Record the ASR with an id (template `assets/asr-record-template.md`) where requirements already live, or in `docs/architecture/asr-register.md` when no place exists.
2. For each design issue the ASR raises, check readiness and write the decision with `architecture-decision-record`; cite the ASR id in the decision drivers.
3. Keep open ASRs in the decision backlog and revisit them when the unknowns are resolved.

## Sources

- adr.github.io definitions: https://adr.github.io/
- O. Zimmermann, "Architectural Significance Criteria and Some Core Decisions Required" (2020): https://www.ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html
- O. Zimmermann, "A Definition of Ready for Architectural Decisions" (2023): https://ozimmer.ch/practices/2023/12/01/ADDefinitionOfReady.html
- L. Chen, M. Ali Babar, B. Nuseibeh, "Characterizing Architecturally Significant Requirements", IEEE Software 30(2):38-45, 2013, doi:10.1109/MS.2012.174
- Wikipedia, "Architecturally significant requirements": https://en.wikipedia.org/wiki/Architecturally_significant_requirements
- L. Bass, P. Clements, R. Kazman, Software Architecture in Practice, Addison-Wesley, chapter "Understanding Quality Attributes"
- I. Ozkaya, L. Bass, R. Nord, R. Sangwan, "Making Practical Use of Quality Attribute Information", IEEE Software, March/April 2008
- SEI, "Reasoning About Software Quality Attributes": https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/
