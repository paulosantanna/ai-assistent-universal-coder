<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

## Decide

Now open the repository, and open it **before** proposing anything and before reading anything outside. An option is not a design, it is a design plus what it costs *here*, and the same choice is obvious in one codebase and absurd in another. Proposing first and checking later means defending a position instead of forming one; reading a benchmark first means reading your own codebase through somebody else's lens.

### What the repository tells you

**Churn does not say which option is right. It says how much it costs to be wrong.** That is the calibrator for the robustness axis, and the most useful signal available because git is always there. A one-way door in a file touched twice a year is cheap to get wrong; the same door in a file touched every week is a bill arriving weekly. Where the answer is already "very little", read it in one command and move on - and a project three months old has no history to read.

Churn is ambiguous in both directions, so never read it alone. Low churn is stable, abandoned, or so painful everyone routes around it; high churn is the hot path of the business, or a part never factored properly. Two cheap signals disambiguate: **how many distinct authors** touch it, because many authors make changing it a coordination cost rather than an edit, and **how recent** it is, because an area still moving six months in has not found its shape and does not deserve an abstraction today.

Read the conventions too, and read them as **precedence rather than as a cost to weigh**. Where this codebase has already answered the question in front of you, its answer stands unless you can name what is wrong with it - not what is nicer about the alternative. An outside idea that merely ties with an established one loses, because a tie gets decided by which is more interesting to write about, and that is how a product line drifts one reasonable improvement at a time.

### Prior art

Somebody has solved a version of this before, and reading how is cheap next to discovering it in production. The discipline the numbers get applies here too: **name what a benchmark would change before you go and look**, or "how do others do this" returns three paragraphs about a company you are not.

Three things are worth carrying back. **The shape that repeats** across independent teams, because convergence is evidence - the same seam everywhere is usually load-bearing rather than fashionable. **The failure everybody reports**, the cheapest item in this skill: an edge case avoided by reading instead of by shipping. And **what turned out to be unnecessary**, which you only get from teams describing what they removed.

**What never transfers is scale, and that is how this section does harm.** A design published by a company with a thousand times your traffic describes *their* constraints faithfully, and adopting it imports a bill for a problem you do not have. Where a benchmark argues for something heavier, say which of their conditions you share; sharing none, it is interesting and irrelevant, and saying so is the finding. Read the constraint behind the design, never the design.

Where nothing comparable exists, that is a result too: the problem is unusual, or the framing is off and nobody names it that way. The second is worth going back for.

**Skip the whole section wherever little rides on being wrong.** A shape everyone in the room can already picture does not get a literature review, and running one anyway turns this into the padding it exists to prevent. Web access is guaranteed nowhere either; where it is missing, say so rather than reasoning from memory about what some product does today, which is exactly the fabricated constraint the knowledge chain forbids. Cite what you did read in Sources - and Sources holds only the documents the research stood on: the roadmap, the decision records, earlier design documents, the external references. Code paths are cited inline, next to the fact they settle, and are not repeated there.

### Two shapes

Propose the overall shape, not each decision separately. Eight decisions with two options each is sixteen options and an exhausted reader; the shape is the thing with a real fork, and the smaller decisions fall out of it, a line apiece.

**The first shape is the obvious one**: what the context already suggests, the best ratio of value to effort, what a sensible team ships. **The second is the one that survives**: more robust over time, more expensive now. The axis is always the same - pay now or pay later - and naming it is what makes the comparison honest, stopping the second option from being a flavour and forcing it to be a different bet.

Give each one the condition under which it wins. That is what lets someone disagree productively: not "I prefer the other one" but "your condition is wrong, we do change that area monthly".

**The lighter shape holds the recommendation and the heavier one has to take it from it** - and taking it is an ordinary outcome, not an upset. The default exists because the condition justifying the heavier shape is a claim about the future, and an unchecked claim about the future is how a team pays today for a scale that never arrives. So put the condition in the present tense and check it: not "we might need a second region" but "we run in one and nothing on the roadmap adds another".

**Where the condition holds, say so and flip.** Situation already collected the evidence for this - a roadmap commitment, a block in flight that needs this, a second consumer that exists today - so "credibly close" means a fact in that list and never a feeling. Where the list holds one, shipping the lighter shape now means building the thing twice.

**Building too little argues for itself as well, and it costs differently.** Overbuilding wastes money you can see; underbuilding buys a rewrite plus whatever broke on the way to it, and neither lands in the estimate. So when you recommend the lighter shape, name **what it will not survive** and what would force the rewrite. Unable to name either, you have not compared two shapes - you have described one and defaulted to it.

**Options beyond the two are perspective and are labelled as that** (rule 7). Where three approaches exist in the wild and two are out, naming all three with the line that removes each beats arriving quietly with the survivor: it turns "here is my answer" into "here is the field, and here is where it narrows". A line each, never in Decisions, never padded to make the recommendation look inevitable - that padding is the straw man rule 3 stops.

When the second shape is not genuinely live, do not build it a section. One sentence - "the heavier version only pays off if we expect N, and we do not" - carries the whole comparison and hands the planner the rejected alternative with the property that killed it.

**Shape is four sentences at most**: what the record is, what the operation does, what the door is and what it costs to change, and the heavier alternative with its condition. It does not say which layers it follows - the repository's rules already do, and restating them is the harness leaking into the document; it earns a sentence only where the design *departs* from them. It does not name precedents - Situation › In flight already did. If Shape names a method it is implementation; if it restates a Key decision it is repetition.

### What the document holds

The document holds the **fundamental decisions - product, API, schema, direction - and nothing the plan can derive from them.** Three rules keep it that size, and they are checked before the document is written, not after:

1. **Each decision is stated once, at the highest level that owns it.** Key decisions is the home of everything hard to reverse; a slice says "Key decision 2" and moves on. The same fact in Shape, in Key decisions, in a slice's table and in its diagram is not four views - it is one decision the reader meets four times and the maintainer updates in three. A design that enunciates ten decisions eighty times reads as bloated even when every section, alone, looks justified.
2. **Identifier ceiling: route, table, column, class, glossary term.** Nothing below - method, container token, file path, CSS selector - appears in the design. If the plan cannot name the method from the route and the class, that is the plan's problem, and a design that names it has started planning and will drift from the plan the moment the plan does its job.
3. **The document says what will exist, not what will be done.** State tables, contracts and schemas define a slice. A list of files to add and methods to change is the plan's output, and a design that carries one is a task list wearing a design's headings.

### Slices

The design is organised by **vertical slice**, never by kind of view. A slice is a staffable vertical - the record, the operation that moves it, the parents that name the new child, the screen - and it carries what a reader needs to understand it in one place: what it delivers, its status, its state table, and only the other views it has content for. A reader who wants to understand one operation reads one section. A document that puts every flow under Flows, every table under Schema and every decision in one table has organised itself for the writer; the reader visits five sections to assemble one slice and gives up.

**Cut the slices first, then fill them.** Five to eight is typical. One is one section and no index. "Pay Invoice" is a slice; "write the service" is a task, and tasks are planning. The index is a table - slice, what exists when it is done, status - followed by an order line. Every fog in the document is visible in that one status column: `clear`, `open` with defaults taken, `rfc`, `spike`, `design`.

**A slice is named by a domain term or a code identifier, never by a prose verb.** "Invoice" and "Pay Invoice" name things a reader can search for - the table, the route. "Bill" and "Settle" name nothing in the repository or the glossary, and the first question a reader who was not in the room asks is what they mean. The same discipline holds in the prose: the record is called what the glossary calls it, every time. A second noun for the same thing - however natural the sentence reads - is the synonym the glossary forbids, and a design document is where it leaks in first.

**A slice is its state table plus what only it can say.** The state table - each journey state this slice answers, what should happen, what the caller sees - is the slice's acceptance criteria, and distributing the journey this way is also the check: every state the user confirmed needs a row in some slice, or one line under the index saying what already handles it. A state confirmed in the interview and missing from every slice is the concrete form of building too little, and the only form of it you can catch by reading instead of by shipping. There is no Adds/Changes list: the plan derives files and methods from the contract, the schema and the flow. There is no per-slice decisions table: what is costly is in Key decisions, and what is reversible and worth a reader's objection is one "Alternatives considered" line - option, and the condition under which it wins.

**Derivable conventions are named once, under the index, not per slice.** Copy text, trimming, sort order, the exact sentence of a `400`, which codes body refs and path ids get - "all as Invoice does them" with the record that holds the convention. Putting them in the slices buries the seven decisions that matter under twenty-three that do not.

**Draw where relationship or order is the content; write where it is not.** Each view appears only in the slice that has the content for it:

- **Schema** - where the slice creates or alters a table: a column table - name, type, nullability, reference, note - plus indexes and what changes on tables that already exist. Not code: the builder knows how to turn a column table into the ORM call. An entity diagram when it relates more than one record, checked against the code. The table one slice alters but another created lives where it was created.
- **Flow** - where the slice holds a one-way door: a sequence diagram whose participants are layers, not files, and whose steps are the refusal before any read, the read that can fail, the transaction, and the race that must lose cleanly. Not the trim, not the existence check - those are the plan's. One per door, not one per status code.
- **States** - only past two states or one writer. Two states and one transition are a sentence in Key decisions, and a diagram of them is a picture of a sentence.
- **Contract** - one line per endpoint the slice adds: method, path, request shape, success response shape. Failure codes are already in the state table next to the outcome they encode.
- **Open, RFC, spike, design** - in the slice they block, and the slice's status says which. There are no global handoff sections.

**Key decisions** sit above the index, in prose, five to eight: what is hard to reverse, wherever it lives. A reader who stops there knows the design. If it needs more than eight, the shape has not been found. Each is an invariant or a placement, never a mechanism - "recording the Payment and marking the Invoice paid are atomic; a lost race leaves no orphan" is a decision; the SQL that achieves it is not.

**Migration and rollout** appears only where Situation said the product is in use: existing rows, backfill, deploy order, what an old client sees before it updates. In construction it is a line or nothing; in steady use it is where the technical risk lives, and a design that skips it has costed the code and not the change.

Every diagram is checked against the repository before it lands. A sequence that calls a method that does not exist, an entity diagram with the wrong cardinality, a state the code cannot reach - each is a fabricated constraint wearing a picture, and pictures are believed faster than prose. Mermaid is the default because it diffs and renders where the document lives; a drawn screen from a design handoff is linked, never redrawn.

**Invariant, not mechanism.** "One Payment per Invoice, and a lost race leaves no orphan Payment" is a decision - it is a product consequence, and a planner reading only the unique index would not arrive at the atomicity it needs. "Conditional `UPDATE ... WHERE status = 'open'`, zero rows means roll back" is a mechanism - one of several that satisfy the invariant, and naming it forecloses the others while putting SQL in a document that forbids method names. The design states the invariant and, where the obvious precedent would violate it, says so - "Refund writes its status and its ledger entry separately; do not copy it here" is the sentence a planner cannot derive and would otherwise get wrong. The test: would a competent planner, reading only the invariant, arrive here on their own - and at the same place? If yes, it is theirs. If the precedent points the wrong way, the warning is yours.

**Code appears almost nowhere.** A full ORM table, a service method, a route handler, a SQL predicate are all what the builder writes from the column table, the flow and the contract; putting them in the design makes the document the thing that drifts from the code instead of the thing the code is checked against. The rare exception is a literal that *is* the product decision - an enum value, a path, a response shape - and those already live in the state table, the contract and the schema.

### When to stop deciding

Two axes settle every remaining question, and the grid is the stopping rule - you are done when every question sits in one of the four, not when you run out of energy.

| | Clear | Unclear |
|---|---|---|
| **High impact** | Decide it. Record the shape, the alternative, and what would flip it. | **Do not decide.** It needs an RFC, or a spike when only building answers it. |
| **Low impact** | One line. | Take a sensible default, note it, and decide while building. |

The top-right cell is the one that gets violated, because deciding feels like progress. A consequential choice nobody can see clearly is exactly the one not to settle in a conversation, and sending it to an RFC is the discovery working rather than failing.

**Spike over RFC** when the missing thing is knowledge only building produces: whether the provider behaves that way, whether the approach performs at this size. Write the question it answers, what each answer changes, and when it stops - a spike with no stopping condition becomes the implementation.

**Needs design** is the third handoff and the one that otherwise gets lost. Behind an API, discovery decides and planning follows directly; on a screen, somebody has to draw it in between, and the plan assumes that happened - it links the visual rather than inventing it. So where a screen cannot be planned until it is designed, say so and say what the design must resolve: which screens, and which journey states it answers for. The drawings then land in **this** document - a link or path in Sources, cited from the slice's state table - never a sidecar brief or a PDF nobody planning from this will open.

Then every cell of the grid lands in a slice: the decided ones in its Decisions table, the RFC, spike and design ones as its status and its open question. The Work index shows the grid as one status column. If a reader cannot see the work and what is still fog from that column alone, the index failed.

Record each decision as it is made, not at the end. Decisions written up afterwards get re-derived, and re-derivation is where the reason quietly turns into a rationalisation.
