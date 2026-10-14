<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Extract

Read the source completely first - ticket, PRD, RFC, thread. Then walk the codebase around what it touches, so the checks land on real paths and reuse what exists.

**Refuse rather than guess.** Three things must be true before you write the checklist:

- every claim has a **nameable proof** - if you cannot say which test would settle it, it is too vague to write down
- every claim has a **concrete value** - a status code, a field, a bound; never "gracefully", "properly" or "fast"
- the boundary is stated - you can say what is explicitly out

Under `profile: ui` a screen carries a fourth requirement - the design is a **binding** source and its concrete values belong in the checks - and the whole of it lives in [screens.md](../tlc/references/screens.md). Under `light` or `standard` skip that file entirely.

Missing one is normal and asking is cheap. Proceeding on a guess is not: if it is still unclear after asking, name what is missing and stop there. A vague check becomes a vague assertion that passes, which is the one failure this whole thing exists to prevent.

**Sweep for what the source does not mention.** These are the requirements nobody writes down, so go through them explicitly and say where each one landed: validation, failure modes, idempotency and retry, authorization, concurrency and ordering, data lifecycle, external-dependency failure, state transitions, observability.

Raising one is always free. Growing scope is the user's call - most resolve to something that already exists, or to "not in scope because X", and both are complete answers. What is not allowed is passing over one in silence.

### Format

Read `references/checklist-format.md` when you write the `.checks/<feature>.md` artifact — after the source is read, the refuse gate is passed, and the sweep is walked. Do not load it during the first pass of Extract.
