<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

# TLC Discover

Find out where this project actually is. Understand the problem. Decide whether to solve it. Then, and only then, decide how.

```
SITUATION ────→ PROBLEM ───────→ VERDICT ───────→ DECIDE
(where this     (no solution     (a stop, or a    (two shapes, costed
 project is)     proposed yet)    record)          against this repo)
```

**These are not a script, they are the prerequisite order.** What you run is an interview: ask whatever is answerable given what is settled, and stop when nothing answerable is left. The order falls out on its own, because *how* has *whether* as a prerequisite and *whether* has *where we are*. Marching them as four acts is how a discovery asks a project that never shipped what its problem costs today.

The failure that matters here is not inventing a fact, it is **converging early**: proposing a solution on turn two, hearing "sure", and manufacturing a decision that has all the authority of one and none of the examination. Everything below exists to make that harder.

The artifact is a design document that anyone - a person, a team, a planning tool - can plan from without having been in the conversation that produced it. It has to show the design, not only record that one was made: the decisions that are hard to reverse, the flow of the critical path, the states and who moves them, the schema as it will exist, the contracts callers will hold. Where relationship or order is the content, that is a diagram; a table of thirty literals is a spec wearing a design's clothes. And it is organised by vertical slice, so a reader who wants one piece of the work reads one section and finds its diff, its flow, its schema, its contract, its decisions and its open questions there. If Shape cannot tell a reader what the bet is, a slice cannot show them how its piece moves, or the Work index which slices are clear, it failed even with every decision recorded.
