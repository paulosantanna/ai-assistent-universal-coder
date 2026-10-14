<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

Use this whether you are **designing** a new system or **reviewing** an existing one. Move through phases in order; each has an exit criterion. State assumptions explicitly; if the domain is unclear, ask before guessing.

### Phase 0 — Frame the scope

Confirm: is this a new platform, a new module in an existing one, or a review? Confirm the runtime/stack constraints (default target is the 2026 TypeScript stack — see `references/stack-2026.md`). Default to **one deploy** (modular monolith) unless a hard constraint says otherwise.

Exit: scope and constraints written down.

### Phase 1 — Domain discovery (DDD strategic)

Read `references/ddd.md`. Identify subdomains from the business language, classify each as **Core**, **Supporting**, or **Generic**, and find the ubiquitous language of each. Do not group by technical layer. If multiple bounded-context interpretations exist, present them — do not pick silently.

Exit: a list of candidate bounded contexts, each classified, with one-line responsibility and key aggregates.

### Phase 2 — Boundaries & context map

Draw the context map: which contexts exist, how they relate (Customer/Supplier, Conformist, Open Host Service, Published Language, Shared Kernel, Anti-Corruption Layer), and which are Core. Decide **state ownership**: one database is fine, but each module is the **sole writer of its own tables** — no foreign keys across module boundaries; reference other contexts by id. Keep aggregates cohesive (do not over-split a transactional Core).

Exit: context map + table-ownership map (one module = its tables).

### Phase 3 — Module internals (flat-by-aggregate)

Read `references/flat-by-aggregate.md`. Inside each module, organize by **aggregate**, not by technical layer: 1 business concept = 1 folder; technical layers become file **suffixes** (`.entity.ts`, `.service.ts`, `.controller.ts`). Keep depth ≤ 2 (flat) or ≤ 3 (subdomain-based). The Clean Architecture **dependency rule still holds** (presentation → application → domain ← infrastructure) — it is just expressed by suffixes and co-location, not by layer folders. Use the 6-criteria test to decide flat vs subdomain-based; default to flat.

Exit: a folder layout per module and a flat-vs-subdomain decision with rationale.

### Phase 4 — Communication & Anti-Corruption Layer

Read `references/acl-and-communication.md`. Every external system goes **behind a Port + Adapter (ACL)** — including internal services owned by other teams. The domain defines ports in its own language; adapters translate the external model in and out. Between internal modules: **synchronous only inside an aggregate** (one ACID transaction); **events via the transactional outbox** across modules, with idempotent consumers. Add SSE for server-to-client real-time when the UX needs push.

Exit: list of ports + adapters; list of domain events with the `module.aggregate.action` naming; sync-vs-async decisions.

### Phase 5 — Resilience

Read `references/resilience.md`. Wrap every external/inter-service call: **timeout → circuit breaker → retry (capped exponential backoff + full jitter)**. Only retry idempotent operations (require an idempotency key for writes). Cap retries with a budget (~10% of traffic), trip the breaker on a sliding-window error rate, and give every breaker a named fallback. Add durable execution only when a long-running, multi-step process must survive restarts.

Exit: a resilience policy applied to each adapter, plus idempotency keys for writes.

### Phase 6 — Stack & evolution

Read `references/stack-2026.md`. Choose the concrete stack and call out the trade-offs (runtime, API style, cache, real-time transport). Then state the **evolution path**: stage 1 (modular monolith + clear boundaries, with events/outbox already in place) is the current state; promote a module to its own app/database only when its own metrics justify it.

Exit: stack table + evolution note.

### Phase 7 — Document the architecture (HTML)

Produce a polished, self-contained HTML architecture document with elegant hand-drawn-style SVG diagrams. Read `references/architecture-doc.md` and start from `assets/architecture-template.html`: copy the template, keep its CSS and visual system intact, and replace the placeholder content. Build the standard sections (overview, domains, principles, monolith map, bounded contexts, ACL, communication, front-to-back, modules, resilience, real-time, evolution, stack) and number diagrams sequentially ("Diagram N — ..."). Preserve the visual identity: palette, Lato + JetBrains Mono fonts, rounded rectangles, arrow markers, soft gradients, and italic captions. The output is one HTML file that opens directly in a browser — no build step.

Exit: a single self-contained HTML file with consistent diagrams and working in-page navigation.

---
