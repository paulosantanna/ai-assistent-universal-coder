<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Critical rules

1. Every check names its **proof**: the test or command whose exit code settles it. No proof, no check.
2. Tests assert what the checklist says, never what the code happens to do. Never write a test by reading the implementation.
3. Never weaken an assertion, delete a test, or skip one to make a suite pass. If a test is genuinely wrong, stop and ask.
4. The checks and the test-policy rows do not change while you build: once written they are the bar you build under, not a position to argue against, and lowering either is renegotiation with the user, visible in the diff. `Landing` is the exception, and it is additive - a door you discover while building gets a row, never a deletion.
5. The **Verifier is a fresh sub-agent**, never the author, never optional, never waiting to be asked. It is dispatched by whoever holds the whole feature, after the **last batch** has landed - never by a build agent, and never as a child of one. A build agent never spawns another agent at all. This is what keeps "done" from being a self-report.
6. **Blast radius:** an approved checklist authorises local edits and local commits. `git push`, deploy and production data changes need an explicit go-ahead.
