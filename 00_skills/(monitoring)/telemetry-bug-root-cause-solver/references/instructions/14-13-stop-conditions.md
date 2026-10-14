<!-- Package: 00_skills/(monitoring)/telemetry-bug-root-cause-solver; relative command/resource examples resolve from that package or workspace root. -->

## 13. Stop conditions

Stop when:

- required failure evidence is missing and no reproduction can be created;
- the incident time window is unknown for runtime evidence;
- evidence cannot be redacted safely;
- the required fix would exceed authorized scope;
- approval is required;
- tests show a blocking regression;
- a critical blocker remains;
- the honest evaluator returns `BLOCKED`.
