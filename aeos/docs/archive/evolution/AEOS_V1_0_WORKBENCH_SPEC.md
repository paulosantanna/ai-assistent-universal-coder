# AEOS v1.0 — Stable Workbench Specification

## Mission

AEOS v1.0 is a governed AI-first engineering workbench capable of:

- analyzing repositories;
- generating evidence-based documentation;
- recommending playbooks;
- generating skills;
- proposing code/test/dependency changes;
- applying patches under approval;
- running tests through allowlists;
- producing rollback;
- creating controlled commits and PRs;
- packaging review bundles;
- orchestrating agents/subagents;
- integrating MCPs under Tool Router;
- tracking observability;
- validating everything through Judge.

## Stable Command Surface

```powershell
aeos run project-analysis --target <path>
aeos run documentation-generation --target <path> --mode sandbox
aeos run security-secrets-audit --target <path>
aeos run devcontainer-generation --target <path> --mode sandbox
aeos run test-recovery --target <path> --mode sandbox
aeos run code-change-proposal --target <path> --issue "<description>"
aeos run dependency-analysis --target <path>
aeos run agent-delegated-project-analysis --target <path>

aeos patch apply --execution-id <id> --target <path>
aeos rollback <id> --target <path>
aeos test run --execution-id <id> --target <path>

aeos approvals list --target <path>
aeos approve <id> --target <path> --action <action> --scope <scope> --reason "<reason>"
aeos deny <id> --target <path> --reason "<reason>"

aeos evidence verify --execution-id <id> --target <path>
aeos package create --execution-id <id> --target <path> --type full-review
aeos package verify --package <zip>
aeos package inspect --package <zip>
aeos package extract --package <zip> --to <safe_path>

aeos pack import --package <zip>
aeos pack verify --package <zip>
aeos pack promote --pack-id <id>
aeos pack activate --pack-id <id>

aeos doctor --target <path>
aeos status --target <path>
```

## v1.0 Release Gates

AEOS cannot be tagged v1.0 until:

- all critical policies have tests;
- all dangerous actions fail closed;
- evidence verify works;
- package verify works;
- Judge blocks deterministic failures;
- Tool Router cannot be bypassed;
- MCP critical connectors disabled by default;
- approvals are granular and expiring;
- rollback works for patch apply;
- no secret values are persisted;
- docs and runbooks are generated;
- bootstrap + evolution packs validate.
