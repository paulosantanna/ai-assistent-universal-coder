# ADR practices

Load this file when writing, reviewing or superseding an ADR. It condenses the sources in section 10; follow the links for the full argument. Evidence checked 2026-10-07.

## Contents

1. What deserves an ADR
2. Definition of Ready (START)
3. Definition of Done (ecADR)
4. Writing good ADRs
5. Anti-patterns
6. Lifecycle and immutability
7. Review mode
8. Templates and provenance
9. TLC baseline versus current guidance
10. Sources

## 1. What deserves an ADR

- Architecturally significant decisions: those that affect structure, non-functional characteristics, dependencies, interfaces or construction techniques (Nygard 2011; AWS, after Richards and Ford 2020).
- An ADR logs the resolution of at least one architecturally significant requirement (ASR). When significance is unclear, triage first with `architecturally-significant-requirement`.
- Choices that are cheap to change and invisible to stakeholders (a class name, a local refactoring) do not get an ADR.
- One ADR records one decision. A staged answer (short term, mid term, long term) is either one staged ADR revisited at each stage or one ADR per stage (Zimmermann; Azure WAF).

## 2. Definition of Ready (START)

Zimmermann's five entry criteria for making an architectural decision:

- [ ] **S**takeholders are known: decision makers, consulted and informed (RACI).
- [ ] **T**ime has come: the most responsible moment (MRM) is now.
- [ ] **A**lternatives exist and are understood: at least two options.
- [ ] **R**equirements, criteria (decision drivers) and context are known.
- [ ] **T**emplate is chosen and the record is created.

When the decision is not ready, say which criterion fails. Record it as `proposed` only if options and drivers exist; otherwise route the decision itself to `the-jury` or `technical-design-doc-creator`.

## 3. Definition of Done (ecADR)

Set status `accepted` only when all five hold; otherwise keep `proposed`:

- **E**vidence that the chosen option will work (spike, proof of concept, trusted experience).
- **C**riteria: at least two options compared against the decision drivers.
- **A**greement among peers, team and stakeholders, at the level the decision's reach requires.
- **D**ocumentation: the ADR is written and shared with every affected party.
- **R**ealization and review plan: implementation scheduled, confirmation defined, revisit date or trigger set.

## 4. Writing good ADRs

- Executive summary: brief, assertive and factual; one to two pages at most (Nygard). Move design detail to a TDD or model and link it.
- Context in value-neutral language that names the forces in tension. The problem statement may be a question; the title never is.
- Root the justification in requirements and experience; cite the ASR ids that drive the decision.
- Balanced verdict: pros and cons of the chosen and of the rejected options, and at least one honest negative consequence.
- Disclose the confidence level; a low-confidence decision is still a useful record (Azure WAF).
- When weighting criteria, prefer meta-qualities such as observability and the ability to react over speculative long-term goals.
- Write as a conversation with a future developer, in full sentences (Nygard).
- State how compliance will be confirmed: design or code review, tests, or a fitness function such as an ArchUnit rule (MADR 4.0.0 Confirmation).

## 5. Anti-patterns

From Zimmermann, "How to create ADRs — and how not to":

| Anti-pattern | Symptom | Remedy |
| --- | --- | --- |
| Fairy Tale | only pros, truisms ("the load balancer balances load") | add cons and evidence |
| Sales Pitch | marketing adjectives without evidence | delete unbacked claims; link the evidence |
| Free Lunch Coupon | no consequences, or only harmless ones | list the difficult and long-term consequences |
| Dummy Alternative | an option that cannot work, added to make the favorite shine | list real alternatives or justify a single viable option |
| Sprint (Rush) | one option, short-term effects only | search for alternatives; add mid- and long-term effects |
| Tunnel Vision | only the local context, e.g. operations ignored | add operator and maintainer criteria |
| Maze | content derails from the title | refactor; move side topics out |
| Blueprint or Policy in Disguise | cookbook or law tone | reword as a journal of the decision |
| Mega-ADR, Novel | a design document stuffed into the ADR | move detail to a TDD or model and link it |
| Magic Tricks | false urgency, problem-solution mismatch, pseudo-accurate weighted scores | remove; justify qualitatively |

## 6. Lifecycle and immutability

- Statuses: `proposed`, then `accepted` or `rejected`; later `deprecated` or `superseded by ADR-NNNN` (MADR, AWS, Nygard).
- Accepted and rejected ADRs are immutable. A changed decision is a new ADR that supersedes the old one, linked in both directions; the log is append-only (AWS, Azure WAF).
- On the superseded record only the status line changes. Never delete records and never reuse numbers (Nygard).
- A rejected ADR keeps the reason for rejection so the topic is not re-litigated (AWS).
- Brownfield systems: decisions already in force may be captured retroactively (Azure WAF). Date the record with the capture date and state the known origin.

## 7. Review mode

From Zimmermann, "How to review ADRs — and how not to". Agree the review mode first: friendly peer or coach, affected stakeholder, or formal design authority. Then ask:

1. Is the problem relevant enough to be solved and recorded in an ADR?
2. Do the options have a chance to solve the problem? Are valid options missing?
3. Are the decision drivers mutually exclusive and collectively exhaustive?
4. If the criteria conflict, are they prioritized?
5. Does the chosen solution solve the problem? Is the rationale sound and convincing?
6. Are the positive and negative consequences reported as objectively as possible?
7. Is the chosen solution actionable and traceable to requirements? Does the ADR define a validity period or review date?

Report findings as finding-recommendation pairs prioritized H, M or L. Avoid the review anti-patterns Pass Through, Copy Edit, Siding (Dead End), Self Promotion, Power Game, Offended Reaction and Groundhog Day. A review never edits an accepted ADR; it proposes a superseding ADR.

## 8. Templates and provenance

| Asset | Source | License |
| --- | --- | --- |
| `assets/madr-template.md` | MADR 4.0.0 `template/adr-template.md` (tag `4.0.0`, released 2024-09-17), verbatim | MIT OR CC0-1.0, used under CC0-1.0 |
| `assets/madr-template-minimal.md` | MADR 4.0.0 `template/adr-template-minimal.md`, verbatim | MIT OR CC0-1.0, used under CC0-1.0 |
| `assets/nygard-template.md` | Nygard 2011 structure (title, status, context, decision, consequences) plus a Date line | Cognitect CC0 waiver |
| `assets/y-statement-template.md` | adr.github.io long-form Y-statement (Zdun et al.) plus Date, Status and Deciders lines | format description |
| `templates/ADR_TEMPLATE.md` | workspace AEOS ADR engine template for `aeos/docs/adr/` | workspace |

Other formats (for example the ISO/IEC/IEEE 42010 information items) are kept when a log already uses them; the lint reports them as `unknown`.

## 9. TLC baseline versus current guidance

`references/ORIGINAL_SKILL.md` is TLC `create-adr` 1.0.0 verbatim. Apply its interactive workflow, language adaptation, quality checklist and anti-patterns with these updates:

| Topic | TLC 1.0.0 baseline | Current guidance applied here |
| --- | --- | --- |
| MADR consequences | Positive and Negative Consequences subsections | one Consequences list with "Good, because" and "Bad, because" items (MADR 3.0.0 and later) |
| Confirmation | absent | Confirmation section (MADR 4.0.0) |
| Metadata | Date, Status and Deciders bullets | YAML front matter `status`, `date`, `decision-makers`, `consulted`, `informed` (MADR 4.0.0); bullets still parse |
| Numbering | `NNN-kebab-case-title.md` in `docs/adr/` | follow the existing log; a new log uses `NNNN-title-with-dashes.md` in `docs/decisions/` (MADR) |
| Status values | accepted, proposed, deprecated, superseded | adds rejected, with the reason recorded (MADR, AWS) |
| Undecided decision | route to `create-rfc` | `create-rfc` is not installed here; `proposed` covers a decision being made; `the-jury` or `technical-design-doc-creator` makes an open decision |
| Verification | manual checklist | plus the deterministic `scripts/adr_lint.mjs --strict` gate |

## 10. Sources

- adr.github.io (definitions, templates, practices): https://adr.github.io/ , https://adr.github.io/adr-templates/ , https://adr.github.io/ad-practices/
- MADR 4.0.0: https://adr.github.io/madr/ and https://github.com/adr/madr/tree/4.0.0/template
- M. Nygard, "Documenting Architecture Decisions" (2011): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html
- O. Zimmermann, "How to create ADRs — and how not to" (2023): https://www.ozimmer.ch/practices/2023/04/03/ADRCreation.html
- O. Zimmermann, "How to review ADRs — and how not to" (2023): https://www.ozimmer.ch/practices/2023/04/05/ADRReview.html
- O. Zimmermann, "A Definition of Ready for Architectural Decisions" (2023): https://ozimmer.ch/practices/2023/12/01/ADDefinitionOfReady.html
- O. Zimmermann, "A Definition of Done for Architectural Decision Making" (2020): https://www.ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html
- AWS Prescriptive Guidance, "Architectural decision record process": https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- Microsoft Azure Well-Architected Framework, "Maintain an architecture decision record": https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- Tech Leads Club, `create-adr` 1.0.0: https://github.com/tech-leads-club/agent-skills
