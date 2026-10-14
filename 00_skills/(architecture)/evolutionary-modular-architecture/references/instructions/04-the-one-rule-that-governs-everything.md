<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## The one rule that governs everything

**Separate the logical boundary (always strong) from the physical boundary (evolutionary).** Modules, contracts, state ownership, and the Anti-Corruption Layer are non-negotiable from day one. Whether a module is its own deploy or its own database is an **operational** decision made later — never a structural prerequisite. This is what lets the system start as one deploy and grow without a rewrite.

A useful mental image: the house has well-divided rooms (modules). Inside each room things sit out in the open, grouped by what they are for (flat-by-aggregate) — not buried in nested drawers (technical-layer folders). The floor plan (boundaries) is what matters most.

---
