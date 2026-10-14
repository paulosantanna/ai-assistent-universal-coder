<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

## Common failures

### Converging on turn two
Cause: a solution was proposed before the verdict, the user said "sure", and that was treated as a decision.
Solution: stop. Recover the problem. If the decision was already committed, record it and skip the gate — do not manufacture a second one.

### Empty case for a new capability
Cause: pain questions ("what breaks if we do nothing") were run on an absence or construction problem.
Solution: switch kinds. Absence: what they do instead. Construction: what stalls, and why now rather than after the next piece. A missing number is not evidence the problem is small.

### Description or template placeholders leaking into the artifact
Cause: the Format template was copied with the angle-bracket hints still in it.
Solution: replace every placeholder with a concrete value, or omit the section. A heading with "N/A" under it does not appear.

### A spec wearing a design's clothes
Cause: one Decisions table grew to thirty rows of error copy, trimming and sort order, and the transaction that actually decides the design is one cell among them. No flow, no state machine, the schema in one line.
Solution: pull the hard-to-reverse decisions into Key decisions as prose, draw the critical path inside the slice that owns it, write the schema as a column table. Drop the derivable literals - a planner gets them from the convention the repository already holds, and cite that convention once under the index.

### Organised by view instead of by slice
Cause: every flow under Flows, every table under Schema, every endpoint under Contract, every choice in one Decisions table, every open question at the end. Each section is tidy and the reader who wants to understand one piece of the work visits five of them.
Solution: cut the slices first. Each one carries its own state table, flow, schema, contract and open questions. The only things above the slices are the bet, the key decisions, and an index with one status per slice.

### Ten decisions said eighty times
Cause: the transaction appears in Situation, Prior art, Shape twice, two Key decisions, the slice's Delivers, its state table, its diagram, a paragraph after the diagram, a cross-cutting line, a decisions row and a schema note. Every section was "earned by having content", and the transaction has content everywhere.
Solution: each decision once, at the highest level that owns it. Key decisions holds it; the slice says "Key decision 2"; the diagram shows it; nothing else mentions it. Then remove the per-slice decisions table, the cross-cutting line and the Adds/Changes list - they were the repetition's vehicles.

### The plan written inside the design
Cause: each slice lists files to touch, container tokens, method names, the order of `DELETE FROM` in the test suite, the union type on the screen.
Solution: identifier ceiling - route, table, column, class, glossary term. Below that is the plan's. The design says what will exist; the plan says what will be done.

### A diagram nobody checked
Cause: the entity diagram says every ledger entry has an Invoice; the code says Refund and Adjustment entries have none.
Solution: every diagram is read back against the repository before it lands. A picture is believed faster than prose, which is exactly why a wrong one costs more.
