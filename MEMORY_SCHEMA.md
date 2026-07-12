# MEMORY_SCHEMA.md
# AEOS Governed Memory Schema

## 1. Purpose

This document defines the mandatory structure, lifecycle, authority and integrity rules for AEOS memory.

Markdown is a storage format, not a trust mechanism.

A memory entry becomes trustworthy only through evidence, provenance, validation and controlled promotion.

---

## 2. Memory classes

### 2.1 Execution memory

Produced by Children.

Purpose:

- preserve factual task history;
- record commands, outputs, diffs and failures;
- support reproduction and review.

Trust level: `RAW_EVIDENCE`.

### 2.2 Domain candidate memory

Produced by Parents.

Purpose:

- capture reviewed domain lessons;
- consolidate recurring patterns;
- preserve domain constraints.

Trust level: `CANDIDATE`.

### 2.3 Root candidate memory

Produced by Root.

Purpose:

- capture architecture, strategy and systemic lessons.

Trust level: `CANDIDATE`.

### 2.4 Shared institutional memory

Produced through governed promotion.

Purpose:

- provide reusable validated knowledge.

Trust level:

- `VALIDATED`
- `GOLDEN`
- `DEPRECATED`
- `SUPERSEDED`

---

## 3. Canonical memory entry

```yaml
memory_entry:
  id:
  schema_version:
  title:

  classification:
    memory_class:
    knowledge_type:
    scope:
    domain:
    criticality:

  lifecycle:
    status:
    created_at:
    updated_at:
    last_validated_at:
    review_due_at:
    deprecated_at:

  authorship:
    author_role:
    author_agent_id:
    reviewer_roles:
    curator_id:

  provenance:
    source_execution_ids:
    source_handoff_ids:
    source_files:
    source_commits:
    source_urls:
    source_standards:
    evidence_ids:

  content:
    observation:
    problem:
    context:
    finding:
    conclusion:
    recommended_action:
    prohibited_action:
    rationale:

  validity:
    applicability:
    preconditions:
    limitations:
    invalidation_conditions:
    confidence:
    confidence_basis:

  relationships:
    related_entries:
    duplicates:
    conflicts_with:
    supersedes:
    superseded_by:
    derived_from:

  verification:
    validation_method:
    tests:
    reproduction_steps:
    independent_reviews:
    contradiction_checks:
    validation_result:

  integrity:
    content_hash:
    previous_hash:
    signature:
```

---

## 4. Required fields

Every persistent entry must include:

- unique ID;
- schema version;
- title;
- memory class;
- knowledge type;
- scope;
- lifecycle status;
- timestamps;
- author role;
- source execution or source evidence;
- observation or finding;
- evidence references;
- applicability;
- limitations;
- confidence;
- validation status;
- integrity hash when runtime supports it.

Missing provenance makes an entry invalid.

---

## 5. Knowledge types

Allowed values:

- `OBSERVATION`
- `FINDING`
- `FAILURE_PATTERN`
- `SUCCESS_PATTERN`
- `ARCHITECTURAL_DECISION`
- `TECHNICAL_CONSTRAINT`
- `SECURITY_RULE`
- `TESTING_RULE`
- `OPERATIONAL_RULE`
- `DOMAIN_LESSON`
- `ANTI_PATTERN`
- `OPEN_QUESTION`
- `RISK`
- `BENCHMARK`
- `REGULATORY_CONSTRAINT`

---

## 6. Lifecycle statuses

Allowed values:

- `RAW`
- `CANDIDATE`
- `UNDER_REVIEW`
- `VALIDATED`
- `GOLDEN`
- `REJECTED`
- `CONFLICTED`
- `DEPRECATED`
- `SUPERSEDED`
- `EXPIRED`

No entry may jump from `RAW` directly to `GOLDEN`.

---

## 7. Confidence model

Confidence must be evidence-based.

Recommended scale:

- `0.00–0.24`: speculative;
- `0.25–0.49`: weak;
- `0.50–0.69`: moderate;
- `0.70–0.84`: strong;
- `0.85–0.94`: very strong;
- `0.95–1.00`: independently reproduced and highly reliable.

Confidence must not exceed the quality of the underlying evidence.

---

## 8. Scope values

Examples:

- `EXECUTION_LOCAL`
- `DOMAIN_LOCAL`
- `REPOSITORY`
- `ECOSYSTEM`
- `ORGANIZATION`
- `CROSS_PROJECT`
- `REGULATORY`
- `CLINICAL`

Broader scope requires stronger validation.

---

## 9. Memory file structure

```text
memory/
├── root/
│   ├── ROOT_LESSONS.md
│   ├── ROOT_DECISIONS.md
│   ├── ROOT_FAILURES.md
│   ├── ROOT_PATTERNS.md
│   └── ROOT_OPEN_RISKS.md
├── parents/
│   └── <domain>/
│       ├── DOMAIN_CONTEXT.md
│       ├── LESSONS.md
│       ├── FAILURES.md
│       ├── PATTERNS.md
│       └── OPEN_QUESTIONS.md
├── children/
│   └── executions/
│       └── <execution-id>/
│           ├── HANDOFF.md
│           ├── EXECUTION_LOG.md
│           ├── EVIDENCE_INDEX.md
│           ├── RESULT.md
│           └── CANDIDATE_LESSONS.md
└── shared/
    ├── GOLDEN_KNOWLEDGE.md
    ├── VERIFIED_PATTERNS.md
    ├── REJECTED_PATTERNS.md
    ├── VERIFIED_FIXES.md
    ├── ARCHITECTURAL_PRINCIPLES.md
    └── OPEN_UNCERTAINTIES.md
```

---

## 10. Append-only history

Where practical:

- do not delete historical entries;
- mark them deprecated or superseded;
- preserve prior hashes;
- record why status changed;
- record reviewer and timestamp.

Knowledge history must remain auditable.

---

## 11. Secret and privacy restrictions

Never persist:

- API keys;
- passwords;
- access tokens;
- private keys;
- session cookies;
- raw medical identifiers;
- confidential personal data;
- unredacted production secrets.

Persist references to approved secure locations instead.

---

## 12. Duplicate and conflict handling

Before adding an entry:

1. Search for semantic duplicates.
2. Search related IDs.
3. Search conflicting conclusions.
4. Compare applicability and evidence.
5. Merge only when provenance remains intact.
6. Mark unresolved disagreement as `CONFLICTED`.

Never overwrite a conflicting entry silently.

---

## 13. Invalidation

An entry must be re-reviewed when:

- dependency versions materially change;
- architecture changes;
- tests begin failing;
- new evidence contradicts it;
- standards or regulations change;
- operating context changes;
- review deadline expires.

---

## 14. Integrity controls

Recommended:

- SHA-256 per entry;
- previous-entry hash;
- append-only audit log;
- immutable execution IDs;
- reviewer identity;
- schema validation;
- registry of active memory files.

An integrity failure blocks promotion.
