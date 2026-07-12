# KNOWLEDGE_PROMOTION.md
# AEOS Knowledge Promotion Protocol

## 1. Purpose

This protocol governs how raw observations become reusable institutional knowledge.

Its purpose is to prevent:

- memory contamination;
- duplication;
- overgeneralization;
- promotion of unverified conclusions;
- catastrophic forgetting;
- obsolete knowledge remaining active;
- confidence inflation.

---

## 2. Promotion chain

```text
RAW OBSERVATION
→ EVIDENCE-BACKED FINDING
→ CANDIDATE LESSON
→ DOMAIN VALIDATION
→ CROSS-CHECK
→ CURATOR REVIEW
→ VALIDATED KNOWLEDGE
→ GOLDEN KNOWLEDGE
```

No stage may be skipped.

---

## 3. Promotion authority

### Child

May create:

- observations;
- evidence;
- execution-local candidate lessons.

May not promote.

### Parent

May:

- validate Child evidence;
- consolidate domain candidates;
- reject weak candidates;
- submit promotion requests.

May not independently create golden knowledge.

### Root

May:

- validate system-wide relevance;
- resolve cross-domain applicability;
- submit architecture or organization-level promotion requests.

### Judge

May:

- independently validate evidence;
- identify contradiction;
- approve or reject quality criteria.

### Knowledge Curator

May:

- deduplicate;
- merge;
- classify;
- calibrate confidence;
- promote;
- deprecate;
- supersede;
- reject.

---

## 4. Promotion eligibility

A candidate is eligible only when:

- provenance is complete;
- evidence exists;
- evidence is reproducible or independently reviewable;
- applicability is bounded;
- limitations are declared;
- invalidation conditions exist;
- duplicate search was performed;
- conflict search was performed;
- confidence is justified;
- schema is valid;
- no secret or prohibited data is included.

---

## 5. Promotion request schema

```yaml
promotion_request:
  request_id:
  candidate_memory_id:
  submitted_by:
  submitted_at:
  target_memory_class:
  proposed_scope:
  proposed_status:
  rationale:
  evidence_summary:
  reproduction_status:
  reviewers:
  duplicate_check:
  conflict_check:
  applicability:
  limitations:
  invalidation_conditions:
  confidence:
  risk_if_wrong:
```

---

## 6. Validation levels

### Level 0 — Raw

Single observation, no validation.

### Level 1 — Evidence-backed

Direct evidence exists.

### Level 2 — Reproduced

The result was reproduced in the same environment.

### Level 3 — Independently reviewed

A separate agent or reviewer validated the result.

### Level 4 — Cross-context validated

The knowledge worked across relevant environments or cases.

### Level 5 — Golden

Highly reliable, broadly applicable within defined boundaries, independently validated and actively maintained.

Critical knowledge requires at least Level 3.

Organization-wide principles normally require Level 4 or Level 5.

---

## 7. Promotion decision

Allowed decisions:

- `PROMOTED_VALIDATED`
- `PROMOTED_GOLDEN`
- `RETAIN_CANDIDATE`
- `REJECTED_INSUFFICIENT_EVIDENCE`
- `REJECTED_DUPLICATE`
- `REJECTED_OVERGENERALIZED`
- `CONFLICT_REQUIRES_RESOLUTION`
- `DEFERRED_PENDING_REPRODUCTION`
- `DEPRECATED`
- `SUPERSEDED`

---

## 8. Duplicate handling

When duplicate candidates exist:

1. Compare evidence.
2. Preserve all provenance.
3. Select the most precise applicability.
4. Merge only compatible conclusions.
5. Link superseded candidates.
6. Recalculate confidence.

Do not delete evidence history.

---

## 9. Conflict handling

When candidates conflict:

1. Mark all affected entries `CONFLICTED`.
2. Identify environmental differences.
3. Compare evidence strength.
4. Run targeted reproduction.
5. Narrow applicability if both are conditionally valid.
6. Escalate critical unresolved conflict.
7. Block golden promotion until resolved.

---

## 10. Confidence calibration

Confidence depends on:

- evidence quality;
- reproduction;
- independent review;
- environment coverage;
- contradiction absence;
- time since validation;
- dependency stability.

Confidence must decrease when:

- evidence becomes stale;
- dependencies change;
- contradictory evidence appears;
- reproduction fails;
- applicability expands without new validation.

---

## 11. Golden knowledge criteria

An entry may become `GOLDEN` only when:

- independently reviewed;
- no unresolved contradiction exists;
- applicability is explicit;
- invalidation conditions are testable;
- evidence is durable;
- maintenance owner exists;
- review cadence exists;
- risk if wrong is understood;
- schema and integrity checks pass.

Golden does not mean immutable.

---

## 12. Deprecation and supersession

Deprecate when:

- obsolete;
- unsafe;
- no longer reproducible;
- replaced by a better method;
- invalid under current architecture;
- contradicted by stronger evidence.

Use `SUPERSEDED` when a replacement exists.

The replacement must reference the prior entry.

---

## 13. Promotion audit record

Every promotion decision must record:

- candidate ID;
- reviewer identities;
- decision;
- rationale;
- evidence;
- conflicts considered;
- confidence before and after;
- target memory location;
- timestamp;
- resulting content hash.
