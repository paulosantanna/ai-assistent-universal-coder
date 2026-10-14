<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Sub-agents and handoff

**One builder unless the estimate does not fit.** Pack whole slices - never split a slice -
accumulating while the running estimate stays under the declared `budget` (default 150k
tokens, from `wc -c` on the files each slice touches, divided by four). Prefer a cut where
the surface changes. Write the intended split into `checks.md` under `## Handoff` with the
arithmetic, after the checks exist and before any code: a number with its reason can be
argued with, a bare number can only be trusted.

Then the gate, and only then:

- The estimate fits → one builder. Do not ask. Do not offer a spawn.
- The estimate exceeds the budget → **stop**. Do not start the implementation. Ask which
  mechanism to use, with both exits named:
  - **handoff** — cut at the surface boundary already written, batches sequential and only
    on green
  - **one builder** — stay, and accept compaction / context loss
- A slice that alone exceeds the budget was cut too coarsely - say so rather than splitting
  mid-outcome. That is not this ask.

Do not ask where to cut. The cut is logistics; the user's answer cannot be better informed
than the arithmetic. Do not ask when it fits. Do not offer spawn at the start of a feature.
Record the chosen mechanism on the same `## Handoff` line before the first line of code.

Batches run sequentially and only hand off on green. The next builder reads `checks.md` and
the **diff** of what landed, never a narrative summary.

When the last batch returns green, the parent dispatches the Verifier in that same turn.
Do not ask. A builder never launches it.

What else needs a decision is the profile, a live alternative in `Landing`, and anything
the refuse-rather-than-guess gate caught.

**Model tier**, only if the harness assigns a model per sub-agent: high reasoning for a
core-domain slice and for writing the checks, faster for mechanical slices, mid-to-high for
the Verifier - it designs mutations and reasons adversarially, so it is never the cheapest
tier. Advisory only; no gate depends on it.
