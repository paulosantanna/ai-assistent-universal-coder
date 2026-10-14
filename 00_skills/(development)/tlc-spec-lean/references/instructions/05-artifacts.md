<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Artifacts

```
.specs/
├── STATE.md                    # Decisions log (AD-NNN) + Handoff snapshot
├── LESSONS.md                  # rendered by scripts/lessons.py - never hand-edit
├── lessons.json                # machine-owned
└── features/<feature>/
    ├── plan.md                 # problem, flow, impact, then the rest of the shape, then criteria; audit last
    ├── checks.md               # claims + proofs, the coverage join, test policy, swept
    └── verification.md         # the Verifier's report
```

Create each file when its phase produces content. For a change under roughly three files with no
one-way door, write only `checks.md` with an `## Intent` paragraph and skip `plan.md` - one
bounded escape, not a sizing matrix.
