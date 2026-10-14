<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## When to split or merge

**Default:** **fewer boundaries** until real pain appears — “flat is often better” than premature fragmentation. Splitting adds coordination, versioning, and operational cost.

### Six-criteria test (favor split when several are true)

| # | Criterion | Question |
|---|-----------|----------|
| 1 | **Language** | Do the sub-areas use **different vocabulary** or conflicting definitions of the same word? |
| 2 | **Rate of change** | Do parts **change on different cadences** or for unrelated reasons (most edits touch one side)? |
| 3 | **Scale / SLO** | Do parts need **different** throughput, latency, or availability targets? |
| 4 | **Consistency** | Do they need **different transaction boundaries** (cannot share one atomic write model cleanly)? |
| 5 | **Ownership** | Would **different teams** or clear ownership lines reduce conflict and review churn? |
| 6 | **Pain signal** | Is there **observable** integration pain: ripple effects, fear of change, unclear who owns a bug? |

**Cohesion / coupling (qualitative).** Favor **high cohesion** inside a module and **low, explicit coupling** between modules. If the only motivation is “files got big” or “folder aesthetics,” **merge or wait**.

### When to merge or not split yet

- Boundaries are **artificial** (same language, same lifecycle, constant cross-calls).
- Splitting would **duplicate** logic or data without a clear **single writer** rule.
- Team is not ready to **own** contracts, versioning, and ops for extra units.

### Decision prompts (short)

- Would separation **reduce** accidental coupling more than it **increases** coordination cost?
- Is there a natural **ubiquitous language** boundary, or only a technical seam?

---
