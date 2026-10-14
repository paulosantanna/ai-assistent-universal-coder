<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Understanding and obligations are separate artifacts

`plan.md` exists because a human has to be able to plan and object **before** anything turns into
a claim with a test selector attached. Reading forty checks to reconstruct what is being built is
not planning, and writing the checks in the same pass that decides the shape produces checks that
ratify whatever was already assumed.

**Both halves live in one file because they are one review.** The file boundary is the semantic
one: on this side, what a human confirms; on the other, obligations with proofs. Splitting the
plan into a spec and a design would cut it in a place that matches neither, and would buy two
mandatory stops for one feature. File order is for reading - Problem, Flow, Impact, then the
rest of the shape, then the criteria, then the audit tables. Writing order is not: write the
problem, walk the surfaces, write the criteria, then fill the shape. That is what stops a
criterion from being invented to justify a component. The closure gate still requires every
criterion to land somewhere in `Flow`, `Relations` or `Surface`, or it is out of scope or a
gap in the shape.

The derivation into `checks.md` is the load-bearing part, not paperwork. Every route in `Surface`
owes a `Coverage` set row whose members are its statuses; every door in `Landing` owes a check;
every entity in `Relations` owes one. A shape section with nothing pointing back at it from
`checks.md` is either dead or unproven, and `validate_checks.py` warns on the common case.

**The design half exists; the component catalogue does not.** What made design documents rot was
never the diagram, it was `Purpose` / `Location` / `Interfaces` / `Dependencies` per class -
reversible detail that goes stale within weeks and then misleads the next reader with the
authority of a written document. None of those fields exists here. Five bounded sections:

| Section | Reviews | Kept out |
| --- | --- | --- |
| `Flow` | the path, one line per hop | any module that neither exists nor is created by a door - that is placement |
| `Impact` | what changes underneath: terms, and existing data | risk registers |
| `Relations` | entities, cardinality, one-way constraints | columns and types |
| `Surface` | route, in, out, statuses | request-body specification, and check ids - those do not exist yet |
| `Landing` | the one-way doors, with the literal shape and the rejected alternative | anything a refactor reverses |

**Which folder, how many classes, what the private method is called: the diff.** Reversible,
answered by the repo's conventions, and never worth an artifact. That is the deliberate trade,
and it is the only one.

A bet still open when you get here - two architectures with live alternatives, each needing to be
costed against this repository - does not fit in a `Landing` row, and a row is the only shape this
artifact has for it. Whatever the project uses to settle one (an ADR, an RFC, a spike) comes
first; then the plan records the shape that won and makes it reviewable.
