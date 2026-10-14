<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Elicitation `E` — how well the framework *extracts* requirements (reported beside; never folded into Final)

`E` grades the SDD-derived `spec.md`/`tasks.md` against the PRD: did the framework surface the implicit requirements a senior engineer would insist on, **and** did it do so cleanly (no hallucinated or contradictory additions)? This is the "value beyond transcription" of an SDD framework. It evaluates the **spec artifacts, not the code**. Like `R`/`S`/`D`, it is reported beside `Final` so the fidelity grade stays comparable.

Three binary-checklist sub-metrics:

### `E_recall` — did it find what it should have?

Run the **frozen implicit-requirement category rubric** below. For each category, mark **Addressed** (cite `spec.md:line`), **Missed**, or **N/A** (the PRD/domain makes it irrelevant). The rubric is PRD-agnostic and reusable, so recall is reproducible without per-PRD gold labeling.

```
E_recall = Addressed / (Addressed + Missed)        # N/A excluded
```

| # | Category | A requirement is expected if the feature… |
| --- | --- | --- |
| 1 | Input validation & bounds | accepts user/external input (ranges, formats, required fields) |
| 2 | Error taxonomy & messaging | can fail in ways the caller must distinguish (typed errors, codes) |
| 3 | AuthN / AuthZ | exposes an endpoint or touches user-owned data |
| 4 | Idempotency & dedup | can be retried or replayed (payments, create-once resources) |
| 5 | Concurrency & race conditions | has interleaving writes / check-then-act on shared state |
| 6 | Data lifecycle & consistency | persists state (transactions, partial-failure rollback, retention) |
| 7 | Observability | runs in production (logs, metrics, traceability of failures) |
| 8 | Limits, pagination & rate | returns lists or is callable at volume |
| 9 | External-dependency failure | calls a third party (timeouts, retries, circuit-breaking, fallback) |
| 10 | State-transition integrity | has a lifecycle/status machine (illegal-transition guards) |

> Extend the rubric per domain, but freeze it per benchmark and apply the identical list to every framework. For head-to-head benchmarks, **also** report **pooled recall**: union the valid additions across all frameworks into one adjudicated master list, then score each framework's recall against that pool.

### `E_precision` — is the signal clean, or gold-plating?

Build the **added-requirement ledger**: every requirement in `spec.md`/`tasks.md` *not traceable to a PRD line*. Adjudicate each, binary, with a one-line warrant + `spec.md:line`:

| Verdict | Meaning |
| --- | --- |
| **Valid-necessary** | a real gap the PRD implied (e.g. "reject `trialDays > 30`") |
| **Valid-defensive** | reasonable hardening (observability, retries, typed errors) |
| **Invalid** | hallucinated, contradicts the PRD, or scope-creep into the explicit out-of-scope list |

```
E_precision = (Valid-necessary + Valid-defensive) / total additions
```

The valid additions become the **`valid E-additions`** set referenced everywhere else (the harness denominator, and `S` traceability). Mark each valid addition **built** or **deferred** (deferred-valid = good discipline, see `S`).

### `E_justified` — are additions warranted?

```
E_justified = additions carrying an explicit rationale/traceability / total additions
```

Unjustified additions are a smell even when individually plausible. Report all three: `E_recall / E_precision / E_justified`. A strong framework reads high on all three — *found the implicit requirements, added little noise, justified what it added*.

---
