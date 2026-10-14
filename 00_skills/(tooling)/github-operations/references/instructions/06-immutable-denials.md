<!-- Package: 00_skills/(tooling)/github-operations; relative command/resource examples resolve from that package or workspace root. -->

## Immutable denials

Always deny:

- repository deletion by API, CLI, script, workflow or delegation;
- reading/exporting existing secret values;
- PAT/token disclosure or scope escalation;
- branch-protection bypass;
- audit/evidence deletion;
- finalized evidence rewrite;
- force-push unless a future stricter policy explicitly introduces a separately approved exception; current default is deny.

Repository deletion response:

```json
{
  "decision": "DENY_PERMANENT",
  "operation": "repository.delete",
  "reason_code": "REPOSITORY_DELETION_MANUAL_ONLY",
  "overridable": false,
  "approval_allowed": false,
  "delegation_allowed": false
}
```

AEOS may state that repository deletion must be performed manually by the user in GitHub, but must not generate or execute a deletion command/API call.
