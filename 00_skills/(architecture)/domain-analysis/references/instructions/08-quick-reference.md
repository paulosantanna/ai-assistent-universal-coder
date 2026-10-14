<!-- Package: 00_skills/(architecture)/domain-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Quick Reference

### Subdomain Decision Tree

```
Analyze business capability
└─ Is it competitive advantage?
   ├─ YES → Core Domain
   └─ NO → Is it business-specific?
      ├─ YES → Supporting Subdomain
      └─ NO → Generic Subdomain
```

### Cohesion Quick Check

```
Same vocabulary? → High linguistic cohesion
Used together? → High usage cohesion
Direct relationships? → High data cohesion
Change together? → High change cohesion

All high → Strong subdomain candidate
Mix of high/low → Review boundaries
All low → Likely wrong grouping
```

### Bounded Context Signals

```
Clear boundary signs:
✅ Distinct Ubiquitous Language
✅ Concepts have unambiguous meaning
✅ Different meanings across contexts
✅ Clear integration points

Unclear boundary signs:
❌ Same terms with same meanings everywhere
❌ Concepts used identically across system
❌ No clear linguistic differences
❌ Tight coupling everywhere
```
