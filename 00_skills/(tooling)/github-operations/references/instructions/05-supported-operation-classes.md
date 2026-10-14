<!-- Package: 00_skills/(tooling)/github-operations; relative command/resource examples resolve from that package or workspace root. -->

## Supported operation classes

### Read-only

- repository metadata, refs, diff/log/status;
- pull requests/issues/releases metadata;
- workflow/runs/jobs/checks and redacted logs;
- branch protection/rulesets when permissions allow;
- artifact metadata and rate-limit state.

### Governed mutation

- create/switch/rename branches;
- selective stage and atomic commit;
- fetch/pull/push authorized branches;
- create/update pull requests (Why/Porquê section required);
- rerun failed workflow runs/jobs;
- create draft releases and authorized releases;
- create/verify Git bundles;
- approved merge after latest-SHA revalidation and a verified Why/Porquê section.

High-risk mutation requires Policy/Permission/Judge/approval as defined by the calling playbook.
