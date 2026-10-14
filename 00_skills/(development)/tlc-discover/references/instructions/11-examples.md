<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: Open decision

User says: "Should we add a cache for the dashboard?"
Actions:
1. Look up situation (shipped product, what is in flight). Ask only what the repo cannot settle.
2. Recover the problem from "we need a cache" — who hurts, what it costs today, what happens if nothing changes.
3. Name the number that would change the decision, then fetch that one.
4. Walk the journey states that matter. Present cheaper-than-building paths.
5. Stop at a verdict and wait.
6. After confirmation, read the repository, then two shapes, then cut the slices and fill each with its diff, flow, schema, contract and decisions. Write `.design/<name>.md` from `references/document-format.md`.
Result: a design document with Status in the header, Situation, Problem, Success, Boundary, Shape, Key decisions, and Work — an index of slices with status, then one section per slice, each with its state table — or a `declined` document that stops after Boundary.

### Example 2: Already committed

User says: "We already decided to build billing. Help me figure out the shape."
Actions:
1. Record the committed decision in Situation. Do not restage the verdict.
2. Interview journey states and evidence that still affect shape.
3. Open the repository before proposing. Two shapes, costed here. Design with the critical-path flow, the state machine and the schema. Write `.design/<name>.md`.
Result: Verdict line is "already committed — see Situation". Shape, Key decisions and every slice are filled. Anyone can plan from it without the conversation.

### Example 3: Wrong skill

User says: "Cut this design doc into tasks."
Actions: Do not run this skill. Planning starts from the document; this skill produces the document.
Result: hand off; no `.design/` file from this skill.
