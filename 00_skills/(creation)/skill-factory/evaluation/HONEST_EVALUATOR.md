# HONEST_EVALUATOR.md

Use this checklist before the skill-factory marks generated skill work complete.

## Extremely Honest Review

- Does the generated skill have a bounded mission, activation rule and non-activation rule?
- Does it include `AGENT.md`, knowledge layers, memory layers and this evaluator layer?
- Is the output schema explicit enough for deterministic validation?
- Was the package validated after generation?
- Was the skill registered for immediate AEOS consumption, or was registration explicitly skipped?
- Are unsupported claims, missing evidence and unresolved risks disclosed?

## Verdict Rules

- Return `PASS` only when generation, validation and registration behavior are confirmed.
- Return `REVIEW` when the skill is usable but needs human judgment before production use.
- Return `BLOCKED` when generation, validation, manifest writing or registry registration fails.
