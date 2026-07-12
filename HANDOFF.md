# HANDOFF.md
# AEOS Responsibility Transfer Protocol

## 1. Purpose

A handoff is the formal transfer of bounded responsibility, context, authority and evidence between agents.

A message, summary or informal instruction is not a valid handoff unless it satisfies this protocol.

---

## 2. Handoff principles

1. Responsibility must be explicit.
2. Scope must be bounded.
3. Authority must be limited.
4. Context must be sufficient but minimal.
5. Evidence must travel with claims.
6. Assumptions must be visible.
7. Risks must not be hidden.
8. Acceptance must be acknowledged.
9. Scope changes require amendment.
10. Completion requires handback acceptance.

---

## 3. Handoff directions

Supported directions:

- Human → ROOT
- ROOT → PARENT
- PARENT → CHILD
- CHILD → PARENT
- PARENT → ROOT
- ROOT → JUDGE
- JUDGE → ROOT
- Agent → Knowledge Curator
- Knowledge Curator → Memory Store

---

## 4. Handoff lifecycle

```text
DRAFT
→ ISSUED
→ RECEIVED
→ VALIDATED
→ ACCEPTED | ACCEPTED_WITH_CONDITIONS | REJECTED | BLOCKED
→ IN_PROGRESS
→ HANDBACK_SUBMITTED
→ HANDBACK_ACCEPTED | REWORK_REQUESTED | ESCALATED
→ CLOSED
```

---

## 5. Canonical handoff envelope

```yaml
handoff:
  handoff_id:
  version:
  created_at:
  updated_at:

  source:
    role:
    agent_id:
    domain:

  target:
    role:
    agent_id:
    domain:

  relationship:
    parent_task_id:
    task_id:
    execution_id:
    previous_handoff_id:

  objective:
    statement:
    expected_outcome:
    business_value:

  scope:
    included:
    excluded:
    allowed_paths:
    forbidden_paths:
    allowed_operations:
    forbidden_operations:

  context:
    summary:
    repository_state:
    relevant_files:
    relevant_memory:
    prior_decisions:
    known_failures:

  constraints:
    technical:
    architectural:
    security:
    regulatory:
    operational:
    time_or_budget:
    context_budget:

  assumptions:
    - id:
      statement:
      validation_status:
      evidence:

  dependencies:
    - id:
      description:
      status:
      owner:

  risks:
    - id:
      description:
      severity:
      mitigation:
      escalation_condition:

  evidence:
    available:
    required:
    evidence_format:

  verification:
    required_tests:
    quality_gates:
    acceptance_criteria:
    stop_conditions:

  memory:
    execution_memory_path:
    candidate_memory_scope:
    promotion_eligible:

  expected_handback:
    format:
    required_sections:
    status_values:

  acknowledgment:
    receiver_status:
    receiver_conditions:
    acknowledged_at:
```

---

## 6. Minimum validity rules

A handoff is invalid when any of these are missing:

- handoff identifier;
- source role;
- target role;
- objective;
- scope;
- authority limits;
- acceptance criteria;
- stop conditions;
- evidence expectations;
- expected handback;
- acknowledgment status.

An invalid handoff must be rejected.

---

## 7. Context packaging

Context must be:

- relevant;
- concise;
- traceable;
- current;
- free of secrets unless explicitly authorized;
- separated into fact, inference and assumption.

Do not include entire repositories or memory stores when a minimal subset is sufficient.

---

## 8. Scope amendment

When scope changes:

1. Stop affected execution.
2. Record the triggering evidence.
3. Create a handoff amendment.
4. Increment handoff version.
5. Describe added and removed scope.
6. Reassess risks and tests.
7. Require new acknowledgment.

No silent amendment is allowed.

---

## 9. Rejection reasons

Use explicit reasons:

- `REJECTED_INVALID_SCOPE`
- `REJECTED_MISSING_CONTEXT`
- `REJECTED_AUTHORITY_CONFLICT`
- `REJECTED_UNSAFE_OPERATION`
- `REJECTED_UNVERIFIABLE_ACCEPTANCE`
- `REJECTED_MEMORY_SCOPE_CONFLICT`
- `BLOCKED_DEPENDENCY`
- `WAITING_APPROVAL`

---

## 10. Handback requirements

Every handback must include:

- original handoff identifier;
- status;
- work completed;
- scope deviations;
- files read and changed;
- commands and tests;
- evidence index;
- failures;
- unresolved findings;
- risks;
- candidate lessons;
- recommended next action;
- confidence and limitations.

---

## 11. Acceptance of handback

The receiving agent must:

1. Verify the handoff identifier.
2. Confirm scope compliance.
3. Inspect evidence.
4. Validate required tests.
5. Review deviations.
6. Review memory candidates.
7. Return:

- `HANDBACK_ACCEPTED`
- `HANDBACK_ACCEPTED_WITH_LIMITATIONS`
- `REWORK_REQUESTED`
- `ESCALATED`
- `REJECTED_UNVERIFIED`

---

## 12. Handoff integrity

Recommended controls:

- immutable identifier;
- versioning;
- SHA-256 hash;
- append-only status history;
- author and timestamp;
- linked execution identifier;
- linked evidence index.

When runtime support exists, handoff integrity must be verified before acceptance.
