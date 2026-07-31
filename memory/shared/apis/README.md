# API Memory

Use one folder per organization, project and API acronym:

```text
memory/shared/apis/<ORG>/<PROJECT>/<API_ACRONYM>/
```

Minimum reviewed files for each API:

- `PROFILE.md` for purpose, owners, environments and source refs.
- `CONSTRAINTS.md` for auth, rate limits, schemas, privacy and safety boundaries.
- `FAILURES.md` for validated negative knowledge.
- `PATTERNS.md` for validated positive integration patterns.
- `REVALIDATION.md` for review schedule and deprecation notes.

Secrets and raw sensitive payloads are forbidden.
