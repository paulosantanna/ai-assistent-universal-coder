<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Common failures

### A proof that names a suite
Cause: `Proof: npm test` was treated as settling one claim.
Solution: name a specific test. A suite going green says nothing about this claim.

### The author verified their own work
Cause: the builder dispatched a child agent, or re-checked the diff themselves.
Solution: a build agent finishes, reports, and stops. The orchestrator dispatches a fresh Verifier over the whole feature after the last batch.

### A test written from the implementation
Cause: the assertion mirrors what the code happens to do.
Solution: tests assert what the checklist says. If a check is wrong or impossible, stop and renegotiate rather than quietly adjusting it.
