<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Automated checks

Make the principles executable instead of relying on review. Run these in CI and before merge (both are zero-dependency Node ESM scripts; pass the libs/packages root, or let them autodetect):

- `node scripts/validate-structure.mjs [root]` — enforces flat-by-aggregate (P11–P17): no technical-layer folders, no single-file folders (except `__test__/`), depth ≤ 3, no README inside aggregates.
- `node scripts/validate-boundaries.mjs [root]` — enforces modular boundaries (P1, P3, P8): no deep cross-module imports (only via barrel/facade), no duplicate or unprefixed entity names, no cross-context relations.

Both exit non-zero on violation and print the offending paths. Treat structural failures as blocking; treat boundary findings as blocking once the team adopts the convention.

---
