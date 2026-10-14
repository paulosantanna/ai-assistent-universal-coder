<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

# Tech Lead's Club - Spec, Lean

Freeze the obligations. Free the plan. Prove it with someone who did not build it. Derived from tlc-spec-driven 3.3.0 (Felipe Rodrigues), tlc-plan, and tlc-implement.

```
┌──────┐   ┌────────┐   ┌───────┐   ┌────────┐
│ PLAN │ → │ CHECKS │ → │ BUILD │ → │ VERIFY │
└──────┘   └────────┘   └───────┘   └────────┘
 read it    obligations   yours       always
```

Four moves, two artifacts before code, one after. A human confirms **what** must be true and
**how** it is being built in one document, and only then does any of it become an obligation with
a proof attached. There is no task breakdown, and the plan carries no component catalogue: what is
hard to reverse gets a one-way door with its literal shape, and everything reversible is decided
while building and reviewed in the diff.
