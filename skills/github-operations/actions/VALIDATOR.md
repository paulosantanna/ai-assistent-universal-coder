# GitHub Actions Validator

A pipeline execution is valid only when:

1. the evaluated SHA equals the current expected head SHA;
2. all repository-required workflow runs/checks have been discovered after the quiet period;
3. every required run/job/check is terminal;
4. every required terminal conclusion is `success`;
5. `neutral`/`skipped` is accepted only for explicitly non-required checks;
6. no required result is inherited from an older SHA;
7. no failure was hidden by weakened tests/coverage/security/branch-protection configuration;
8. secrets were redacted before logs reached reasoning/evidence;
9. recovery stayed within cycle/time/token limits;
10. Judge, Evidence Verify and secret scan pass before merge readiness.

## Recursive validation

After every corrective push, discard previous-SHA success as merge evidence, discover the new run/check graph and assign guardian coverage again.

## Merge validation

Immediately before merge, re-read PR head SHA and required checks. Any head movement or new pending/failing required check invalidates readiness.

## Permanent denial validation

Any repository-deletion path must resolve to `DENY_PERMANENT` before API/CLI/tool invocation.
