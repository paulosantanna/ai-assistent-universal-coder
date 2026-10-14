<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Production gates

Before production write:

- consolidated Beta Map exists;
- target hostname/environment verified;
- current cookie session valid;
- Development Context and acceptance criteria are explicit for code changes;
- change plan and affected surfaces identified;
- generated/edited diff has been reviewed against existing architecture;
- backup/snapshot or deterministic rollback exists;
- staging/dry-run used when risk warrants;
- security/accessibility/performance/maintainability impact considered;
- no secret/cookie/nonces are persisted;
- complete installed plugin inventory is known (not a sampled subset);
- post-change smoke and visual/functional verification defined.

High-risk operations require explicit approval according to Policy Engine.
