<!-- Package: 00_skills/(cloud)/kinghost-site-publish-ftp-expert; relative command/resource examples resolve from that package or workspace root. -->

## Completion states

Return one of:

- `PASS`: approved manifest published and application verification passed;
- `REVIEW`: publish succeeded but one non-critical verification dimension remains unavailable;
- `BLOCKED`: prerequisites, backup, approval, scope or credentials are unsafe/incomplete;
- `ROLLBACK_REQUIRED`: publish applied but verification failed or integrity is uncertain.

Evidence must include selected domain/environment, change id, redacted credential ref, manifest counts, backup/rollback refs, verification results and residual risk.
