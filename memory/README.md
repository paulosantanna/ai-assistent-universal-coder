# AEOS Memory

Memory stores execution history, candidate lessons, decisions, failures and open risks. It is not a dumping ground for raw output.

Use the role scopes required by the AEOS constitution:

- `root/` for root-level candidate memory.
- `parents/<domain>/` for domain candidate memory.
- `children/executions/<execution-id>/` for execution records.
- `shared/` only for reviewed and promoted institutional knowledge.

API and integration memory must be separated by organization, project and API acronym:

```text
memory/shared/apis/<ORG>/<PROJECT>/<API_ACRONYM>/
```

Each API memory folder should contain reviewed references, constraints, failure patterns, integration decisions and revalidation notes. Do not store credentials or raw sensitive output.
