# Playbook: chromatic-decision

## Objective

Use `chromatic-mega-brain` to prepare high-impact AEOS decisions before implementation.

## Required Skills

- chromatic-mega-brain
- risk-classifier
- anti-hallucination-evaluator

## Required Agents

- architect
- security, when risk or security tradeoffs exist
- judge

## Required LCPs

- global-rules
- security-governance
- project-memory

## Required Evidence

- objective
- decision type
- constraints
- inspected files or prior evidence refs
- known risks
- candidate options, when comparing alternatives

## Steps

1. Classify whether the decision is high-impact.
2. If a deterministic specialized skill is sufficient, stop and route to that skill.
3. Execute `chromatic-mega-brain` with objective, decision type, constraints and evidence refs.
4. Review selected colors and remove any color without a material role.
5. Collect color handoffs and contradiction list.
6. Build a decision matrix with evidence-backed criteria.
7. Route synthesis through Judge for high-impact decisions.
8. Record only candidate lessons; promote knowledge only after validation.

## Blocking Conditions

- Objective missing.
- Evidence refs missing for architecture, migration, security or cloud readiness decisions.
- Requested use would bypass a specialized deterministic skill.
- Any color requires claims unsupported by inspected evidence.
- Judge review missing for high-impact decisions.

## Outputs

- chromatic run record
- selected color set
- color handoffs
- decision matrix
- contradictions and blockers
- Judge-ready recommendation package
