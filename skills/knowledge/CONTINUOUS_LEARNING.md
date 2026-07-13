# CONTINUOUS_LEARNING.md

## Loop

```text
Generate
→ Validate
→ Observe failures
→ Repair
→ Record candidate lesson
→ Compare with prior cases
→ Promote or reject
→ Update templates or validator
→ Regression test
```

## Learning targets

- activation accuracy;
- architecture selection;
- generated file completeness;
- validator precision;
- false positive rate;
- false negative rate;
- generated test quality;
- package maintainability.

## Anti-forgetting

When templates evolve:

- retain regression fixtures for previous valid skills;
- retain anti-pattern fixtures;
- rerun all validator tests;
- version schemas;
- preserve deprecated rules with rationale.
