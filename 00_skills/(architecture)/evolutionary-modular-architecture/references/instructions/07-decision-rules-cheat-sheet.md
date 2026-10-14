<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Decision rules (cheat sheet)

- **Subdomain class:** competitive advantage → Core; business-specific but not differentiating → Supporting; solved problem you consume → Generic.
- **Tactical intensity:** full (rich aggregates, VOs, invariants, events) in **Core**; moderate in **Supporting**; minimal in **Generic** (forcing richness where there is no invariant is over-engineering). Details in `references/ddd.md`.
- **Flat vs subdomain:** flat by default (depth 2). Go subdomain-based (depth 3) only when 4+ of 6 criteria hold: different personas, authorization, execution model, scaling, deployment, failure isolation. Details in `references/flat-by-aggregate.md`.
- **Sync vs event:** sync inside one aggregate (atomicity matters); event via outbox across modules (tolerates eventual consistency).
- **Durable execution:** add it only for long-running, multi-step, must-resume processes — not for ordinary requests.
