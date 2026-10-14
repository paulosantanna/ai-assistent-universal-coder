<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

### Error: a validator exits non-zero

Cause: A structural gate failed — a criterion without SHALL, a check without a proof, a coverage row whose size exceeds its members, a verification report written by the author, or a profile that does not match the approved checks.
Solution: Read the script stderr, fix the artifact it named, and re-run the same command. Never skip the script or weaken an assertion to proceed.

### Error: no code-execution tool

Cause: The harness cannot run Python.
Solution: Perform the same checks by reading the artifact and say once that you are on the degraded path.
