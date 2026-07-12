# CONTINUOUS_LEARNING.md
# AEOS Continuous Learning Engine

## 1. Purpose

Continuous learning means improving future engineering decisions through governed accumulation, validation, reuse and invalidation of knowledge.

It does not mean allowing agents to rewrite institutional truth after every execution.

---

## 2. Learning objectives

The system must improve:

- repository understanding;
- planning quality;
- delegation quality;
- implementation accuracy;
- failure prediction;
- verification coverage;
- architecture decisions;
- operational safety;
- context efficiency;
- evidence quality.

---

## 3. Learning loop

```text
Execute
→ Observe
→ Capture Evidence
→ Identify Findings
→ Generate Candidate Lessons
→ Review
→ Promote or Reject
→ Reuse
→ Measure Outcome
→ Revalidate
```

---

## 4. Learning by hierarchy

### Child learning

Scope: execution-local.

Captures:

- exact attempts;
- commands;
- outputs;
- failures;
- successful local patterns;
- unresolved uncertainty.

Persists only in execution memory.

### Parent learning

Scope: domain.

Captures:

- recurring domain failures;
- domain constraints;
- validated implementation patterns;
- effective decomposition strategies;
- domain test strategies.

Writes domain candidates after reviewing Child evidence.

### Root learning

Scope: architecture and organization.

Captures:

- cross-domain dependencies;
- systemic risks;
- architecture trade-offs;
- orchestration failures;
- delegation effectiveness;
- repeated organizational bottlenecks.

Writes Root candidates.

### Institutional learning

Scope: shared.

Contains only promoted knowledge.

---

## 5. Mandatory post-execution reflection

After each material task, answer:

1. What was expected?
2. What actually happened?
3. Which assumptions were correct?
4. Which assumptions failed?
5. What evidence supports the conclusion?
6. What should be repeated?
7. What must be avoided?
8. Where does the lesson apply?
9. Where does it not apply?
10. What would invalidate it?
11. Should it remain local, domain-level, Root-level or shared?
12. Does an existing entry already cover it?

---

## 6. Anti-catastrophic-forgetting policy

Never replace old knowledge merely because newer evidence exists.

Instead:

- retain history;
- link superseding entries;
- compare old and new applicability;
- preserve evidence;
- downgrade confidence when appropriate;
- use representative old cases during revalidation;
- maintain regression tests for critical lessons.

New knowledge must be evaluated against:

- recent cases;
- representative historical cases;
- known edge cases;
- known failures;
- high-risk scenarios.

---

## 7. Learning quality gates

A candidate lesson fails when:

- evidence is absent;
- conclusion exceeds evidence;
- applicability is undefined;
- the lesson duplicates existing knowledge;
- contradictions are ignored;
- confidence is inflated;
- source execution is incomplete;
- secrets or prohibited data are included;
- it cannot be traced to a handoff and execution.

---

## 8. Learning metrics

Track:

- candidate lessons created;
- candidates rejected;
- candidates promoted;
- duplicate rate;
- contradiction rate;
- stale knowledge rate;
- reuse count;
- successful reuse rate;
- regression prevention count;
- false guidance count;
- time to deprecate invalid knowledge;
- percentage of entries with complete provenance.

Metrics must not become vanity scores.

---

## 9. Reuse protocol

Before a material task:

1. Identify relevant scope and domain.
2. Load applicable negative knowledge.
3. Load applicable validated patterns.
4. Check dependency and architecture compatibility.
5. Check last validation date.
6. Exclude deprecated or superseded entries.
7. Record which memory entries influenced the plan.

Memory must inform reasoning, not replace it.

---

## 10. Revalidation cadence

Revalidate when:

- a dependency changes materially;
- architecture changes;
- a new environment is introduced;
- production behavior contradicts memory;
- standards or regulations change;
- review deadline expires;
- critical knowledge has not been used recently.

High-risk knowledge requires shorter review intervals.

---

## 11. Learning stop conditions

Block promotion when:

- evidence integrity fails;
- conflict is unresolved;
- source cannot be reproduced;
- scope is overgeneralized;
- human review is mandatory;
- regulatory or clinical interpretation is uncertain;
- knowledge could enable unsafe behavior;
- memory schema validation fails.

---

## 12. Continuous improvement of agents

Agent behavior itself may generate candidate lessons about:

- poor decomposition;
- excessive context use;
- weak handoffs;
- repeated scope violations;
- inadequate tests;
- missed risks;
- judge disagreement;
- memory pollution.

Changes to agent contracts require Root review and independent validation.

---

## 13. Feedback loop to planning

Validated lessons must influence:

- task decomposition templates;
- handoff templates;
- risk checklists;
- quality gates;
- test selection;
- Parent selection;
- stop conditions;
- architecture review.

A learning system that stores knowledge but does not alter future planning is incomplete.

---

## 14. Final learning statuses

Use:

- `NO_MATERIAL_LESSON`
- `EXECUTION_LOCAL_LESSON`
- `DOMAIN_CANDIDATE`
- `ROOT_CANDIDATE`
- `PROMOTION_REQUESTED`
- `PROMOTED_VALIDATED`
- `PROMOTED_GOLDEN`
- `REJECTED`
- `CONFLICTED`
- `DEPRECATED`
