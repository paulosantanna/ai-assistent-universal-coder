<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Build

You decide how. Write the tests from the checklist, implement, run each proof, commit in coherent pieces with Conventional Commits.

Two boundaries, and they are about scope rather than care. New capability nobody asked for and unrelated refactors are not yours to add - surface them and move on. Everything else inside the work at hand is the work: a guard clause, a log line, a clear error message, a test beyond the proofs when you can say what *should* happen at an edge the checklist did not name. Extra tests are welcome and there is no quota.

Doors get discovered while building, and deciding them is yours - stopping to ask on every one defeats the point of getting out of your way. Decide, then record: append the row to `Landing` with its literal shape and the alternative you rejected, **before the code that closes it is written**, and in that code's commit where the project tracks the artifact. The timing is the mechanism, not the commit. An alternative is only knowable while you are still choosing between them; written at the end of the build it becomes a justification of what you already wrote, which is the stale design document `Landing` exists to avoid. Stating what the other option would have done is also the one thing that can expose a bad decision with nobody else in the loop.

A red proof is a stop, not a note. If a check turns out to be wrong or impossible, stop and renegotiate with the user rather than quietly adjusting it. The same goes for a `Landing` row the user approved that the build proves unbuildable - they approved that shape specifically. A new door that contradicts nothing already approved never stops: it gets its row and you keep going.

### When one agent is not enough

A long build runs out of context, and the two ways through it are not equivalent. Automatic compaction summarises the **conversation** and chooses for you what to drop, at whatever token boundary it happens to hit. A handoff to a fresh agent carries the **artifact**, at a boundary you chose. This skill is built for the second: the checklist plus the diff is a better briefing than a machine summary of a chat, which is the whole reason `Landing` rows are appended before the code that closes them rather than at the end.

**The batch is whole slices, and you decide how many while writing the checklist.** Slices come from the upstream task, one observable outcome each, and their checks are countable before any code exists - so the split is knowable in advance, which is the only reason it can be declared and argued with. Never split a slice: mid-slice is green but incomplete, and the next agent inherits half an outcome, which is the horizontal cut the whole pipeline exists to avoid.

**Weigh the slices, do not count them.** Slice size varies by a factor of three or more inside one task - the one holding all the doors is rarely the one with three trivial criteria - so a fixed number of slices per batch inherits all of that variance. Pack by the size on each slice heading: **accumulate whole slices while the running total stays under 150k tokens**, and hand off at the last slice that fits. Where two packings both fit, prefer the boundary at which the **surface changes** - where the next slice reads different code - because there the next agent had to read it anyway and nothing is paid twice.

A slice that alone exceeds the budget is a slice the upstream task cut too coarsely. Say so rather than splitting it here: cutting mid-outcome is the horizontal cut this whole pipeline exists to avoid, and the task is the place that can re-cut it vertically.

**Why a token budget works where a check budget did not.** What a check costs is a property of the repo - fourteen checks inside one service share their reading, fourteen across fourteen modules pay it in full - so a count travels badly between projects. A token does not: it means the same thing everywhere, and it is measurable from the files themselves. 150k is the default because it leaves the rest of a large window for the part no arithmetic reaches - failing tests, retries, a runner dumping two thousand lines. Where a project runs a different window, it says so: `handoff: on, budget 90k`. Do not fix the number of agents up front, though; that is still a boundary you would honour after it stopped making sense.

Write the intended split into the checklist while you are still writing it, under a `## Handoff` heading, with the arithmetic that produced it - "S1-S3 = 118k, all in Warehouse; S4 enters Quantities at 140k, so hand off after S3". It costs a line, it is contestable before any code exists, and it is the only moment when anyone can say the batching is wrong cheaply. A number with its reason beside it can be argued with; a bare "hand off after slice 3" can only be trusted.

**Handing off.** Only on green, with every proof in the batch passing. The next agent reads the checklist and the **diff of what has already landed** - never a narrative summary of it. The diff is the state, and it carries the hundred reversible choices that sit below the `Landing` bar: naming, error shape, where the helper went. Those are exactly what drifts between agents, and they are exactly what no document records.

Then append three lines to `## Handoff`. They go in the checklist rather than in the next agent's prompt: a briefing written into a prompt survives exactly one boundary, and the third agent needs the first one's.

- **Where the boundary fell** - the checks now closed and the commit that closed them. Scope then comes from the artifact instead of being reconstructed from a diff, which is the one inference the next agent would otherwise have to make before writing a line.
- **What the user settled mid-build** - every clarification and renegotiation that did not already become a `Landing` row or an edited check. This is the class that hurts most, because it exists only in a conversation the next agent cannot read, and re-deriving it means asking the user the same question twice or guessing, which every other part of this skill forbids.
- **What was abandoned** - tried, discarded, and why. The one thing neither the code nor the checklist preserves.

**When compaction happens anyway**, re-read the checklist and the diff before continuing. You cannot see the limit approaching - no reliable measure of your own context exists - but you can see that a compaction occurred, so build the recovery on the signal that exists rather than on predicting the one that does not.

That paragraph is the whole strategy under `handoff: off`, which a project sets when its harness has no sub-agent mechanism, or when one continuous session is simply easier to review. Off means one agent, compaction, and re-reading - so the checklist earns its keep more rather than less. Say at the start of a long build that handoff is off, and where the work is plainly too large for one context say that too, then let the user turn it back on for this feature.

Where the source is a ticket or a thread rather than a task with slices, there are no inherited boundaries, so cut on the surface you found yourself - the module the next checks move into. Say when that happens: a boundary you drew is weaker than one the upstream task drew, and the next agent should know that is what it inherited.
