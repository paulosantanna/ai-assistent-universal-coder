<!-- Package: 00_skills/(tooling)/github-operations; relative command/resource examples resolve from that package or workspace root. -->

## Authentication

Credentials are runtime-only. Configuration stores only a reference, for example:

```yaml
github:
  auth:
    type: environment
    token_env: GITHUB_PAT
```

Preferred sources: Git Credential Manager, `gh auth`, authorized secret provider, or environment reference. Never commit, print, log, cache, persist or send the PAT/token to reasoning, evidence, notebook or Token Manager.

A plaintext PAT in tracked YAML/config is a blocking secret-exposure finding. Remove the value from tracked config and require rotation/remediation according to repository policy; do not copy the value into reports or commits.
