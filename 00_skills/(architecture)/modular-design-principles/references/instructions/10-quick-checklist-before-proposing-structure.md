<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Quick checklist (before proposing structure)

- [ ] Public API is minimal; internals are not exported casually.
- [ ] Names and storage ownership are unambiguous per module.
- [ ] No cross-module persistence shortcuts without an explicit contract.
- [ ] Business rules sit behind a clear application/domain layer, not only in adapters.
- [ ] Cross-module calls have explicit failure and timeout behavior.
- [ ] Observability can answer “which module failed and why?” without spelunking.
- [ ] If the context has sub-units: each has clear ownership; no monolithic “registers everything” persistence grab-bag.

---
