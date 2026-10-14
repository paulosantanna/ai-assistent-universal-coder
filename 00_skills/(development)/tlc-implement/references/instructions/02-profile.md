<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Profile

The project chooses how much of this runs, in its `AGENTS.md` or equivalent:

```markdown
## tlc-implement

profile: standard
handoff: on
```

`profile` is one of `light`, `standard`, `ui`; `handoff` is `on` or `off`, and absent it is `on`. A batch packs whole slices up to **150k tokens** of estimated reading; a project on a smaller window overrides that with `handoff: on, budget 90k`. Which slices land in which batch is not configured - that is decided per feature, from the slices in front of you, and written down before any code.

| Profile | Adds | Cannot catch |
|---|---|---|
| `light` (default) | proofs batched at `HEAD`, each named test shown to exist and run, one located assertion per check, level and sampling gaps, `Swept existing` re-read | a set member with no proof; a test that would pass under a wrong implementation |
| `standard` | the `Coverage` join, `Test policy` rows with a verdict each, one fault per assertion surface | a check that contradicts the design; a screen nobody built |
| `ui` | binding sources opened and compared, per-screen enumeration of copy **and arrangement**, the designed-screens row - [screens.md](../tlc/references/screens.md) | **only** spacing, colour and type weight, enumerated per screen - never layout, which a selector reaches and which is checked like anything else |

Each step adds a **class of failure detected**, so read the right column before choosing: the cheap profile is not a discount on the same product. Absent a declaration, `light` - a review nobody runs because it outlasts the build protects nothing, so the default is the one that gets run rather than the one that catches most.

Under `standard` or `ui`, read `references/test-policy.md` when writing Coverage and Test policy rows. Under `light` skip that file.

**A step whose input is empty costs a line, not a pass.** The `Coverage` join has nothing to recompute where the checklist declares no set; the `Test policy` verdicts need that section to exist; step 1 needs a source marked binding. Say "no set rows" and move on - working through an empty step is how a small feature ends up paying a large feature's review.

`ui` costs nothing on work with no interface, because every screen step is conditional on a source marked binding; a product repo can set it once and stop thinking about it.

**The profile is a floor and it is not a secret.** The verification report names it, or "no faults injected" reads the same as forgetting. Where the profile looks too thin for the feature in hand, say so in one line and let the user raise it - doing more than the profile in silence costs the predictability that made it worth declaring.

`handoff: on` is the default and governs the build alone: `off` keeps the whole build in one agent, and what that changes is in *When one agent is not enough*. It does not reach the Verifier, which is a separate agent because the author cannot check their own work rather than because the build ran long.
