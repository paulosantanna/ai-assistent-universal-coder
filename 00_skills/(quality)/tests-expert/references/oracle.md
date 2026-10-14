# Oracle

Read this before writing or editing a charter.

## Source

The oracle is the user request that asked for the fix or the new behavior, kept verbatim in `user_request`. The diff, the current function, and a passing suite are observations. They do not decide the expected result.

You may read the implementation only to find how to reach the behavior: the URL, command, selector, or job name. If the request does not say what should happen, stop and ask. Do not open the code to invent the expected value.

## One check per requested outcome

1. Quote the request.
2. List the observable outcomes the user asked for, in their words.
3. Turn each outcome into one check. Do not add a check they did not ask for.
4. A bug fix checks the broken behavior they named, in the direction they asked to correct.
5. New behavior checks the behavior they asked to exist.

`oracle_source` is `user_request`. `surface` is `browser`, `http`, `cli`, or `job`.

```json
{
  "oracle_source": "user_request",
  "user_request": "o login aceita senha vazia; corrija.",
  "checks": [
    {
      "id": "login-empty-password",
      "surface": "http",
      "requested_behavior": "A login attempt with an empty password is rejected.",
      "steps": ["Start the application the way the repository documents", "Submit login with an empty password"],
      "expect": "The attempt is rejected and no authenticated session starts."
    }
  ]
}
```

## Rejected charters

The freeze script rejects these. Do not rephrase them until they pass.

- `oracle_source` of `implementation` or `code`
- a unit or class surface, or prose such as "unit test" or "teste de classe"
- an expectation "based on the code", "espelhar o código", or "match the current implementation"
- an expectation written "para o teste passar" or "so the test passes"
- a credential assignment inside the charter

Freeze writes `.aeos/tests-expert/state.json`. After that, editing `expect`, `requested_behavior`, or `steps` while `user_request` is unchanged exits 2 with `ORACLE_TAMPERED`.
