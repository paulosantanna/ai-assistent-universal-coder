<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Profile

The project declares how much runs, in `AGENTS.md` or equivalent. Absent a declaration:
`light`. Same three levels as `tlc-implement`, gated the same way, so moving between the two
skills needs no second vocabulary.

```markdown
## tlc-spec-lean

profile: light
budget: 150k
```

| Profile | Adds | Cannot catch |
| --- | --- | --- |
| `light` (default) | proofs run at `HEAD` with each named test shown to exist and run, one located assertion per check, level and sampling gaps, `Swept existing` re-read | a set member with no proof; a test that would pass under a wrong implementation |
| `standard` | the `Coverage` join recomputed, `Test policy` rows with a verdict each, one fault per assertion surface | a check that contradicts a binding source; a screen nobody built |
| `ui` | binding sources opened and compared, per-screen enumeration of copy **and** arrangement | only spacing, colour and type weight, enumerated per screen |

Each step adds a **class of failure detected**, so a cheap profile is not a discount on the
same product - read the right column before choosing it. Two things about `light` are worth
saying out loud, because its own row says them and they are easy to skim past: it will not
notice an enumerated set member that nobody proved, and it will not notice a test that passes
under a wrong implementation. `standard` exists for exactly those two.

`ui` costs nothing on work with no interface: every screen step is conditional on a screen
existing. A step whose input is empty costs a line, not a pass ("no set rows", "no binding
source").

The `Coverage` join is **written** into `checks.md` at every profile - the join is what makes an
omission structural, and that costs nothing at authoring time. What `standard` buys is the
Verifier **recomputing** it from the authority over each set instead of reading the author's
table back.

The profile is a pin, not a preference, and unlike `tlc-implement` that is enforced rather than
asked for: `validate_verification.py` fails a report whose profile differs from the one
`checks.md` was approved under, and fails a `standard` report with no fault rows or no
recomputed coverage, and a `ui` report with no binding-sources section. So a step that did not
run stays distinguishable from a step that was forgotten, which is the whole reason to declare
a floor.

Where the profile looks too thin for the feature in hand, say so in one line and let the user
raise it. Doing more than the profile in silence costs the predictability that made declaring
it worthwhile.
