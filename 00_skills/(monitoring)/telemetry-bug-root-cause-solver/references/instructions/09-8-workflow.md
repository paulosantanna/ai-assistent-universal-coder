<!-- Package: 00_skills/(monitoring)/telemetry-bug-root-cause-solver; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Establish scope, time window, evidence sources and allowed paths.
2. Redact sensitive values before storing or summarizing telemetry.
3. Build a chronological failure timeline:
   - first bad signal;
   - first user impact;
   - first alert;
   - first deployment or config change;
   - first recovery or mitigation signal.
4. Normalize telemetry names using OpenTelemetry semantic conventions when possible.
5. Correlate runtime identifiers with code:
   - trace or request ID to handler;
   - pod and container to workload;
   - image tag or commit SHA to source revision;
   - stack frame to file and line;
   - metric or alert to affected component.
6. Form root-cause candidates and actively seek counter-evidence.
7. Reproduce the defect with a failing test or deterministic command when possible.
8. Apply the smallest authorized fix or produce a fix plan when mutation is not authorized.
9. Run focused verification first, then broader suites based on blast radius.
10. Compare baseline and final behavior.
11. Generate rollback and learning records.
12. Apply the honest evaluator before claiming completion.
