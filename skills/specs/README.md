# specs

`specs` is the AEOS spec-driven preflight skill. It must run before any downstream AEOS skill creates or alters artifacts.

## Purpose

The skill turns creation or modification intent into a traceable spec package:

- requirements;
- acceptance criteria;
- design notes;
- task plan;
- test applicability matrix;
- evidence and approval gates.

## Runtime Gate

The skill executor treats mutating skills as blocked unless the request carries a valid `specs` evidence reference, such as:

```json
{
  "specs": {
    "status": "PASS",
    "evidence_ref": "evidence/specs/<spec-id>.json"
  }
}
```

Read-only inspection does not require this gate.

## Related feature workflows

Assimilated feature skills `spec-driven` and `spec-driven-lean` produce `.specs/` artifacts. They do not replace this preflight. A current approved feature spec, or lean plan plus checks, may be cited as `specs` evidence when it includes testable requirements, acceptance/proofs and approval.

## Validation

```powershell
py -3 skills\specs\scripts\validate.py skills\specs
py -3 -m pytest skills\specs\tests -q
```
