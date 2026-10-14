# Execution

Read this when choosing a surface or writing the outcome file.

## Surface

| User asked about | Surface | What runs |
| --- | --- | --- |
| a screen, click, form, or page | `browser` | the real UI: open, type, submit |
| an endpoint or status | `http` | the running server, not a function call |
| a command | `cli` | that command |
| a job or worker | `job` | the real entrypoint |

Use the repository's documented start command. Do not mock the system under test. Do not point the run at production data. If the application cannot be started, say so and leave the charter pending. Do not replace the check with a unit test.

## Evidence

Save raw tool output at `.aeos/tests-expert/evidence/<check-id>.txt`. Include the check id, the command or URL you issued, and the response. The observed quote in the outcome must be copied from that file. The file cannot be the charter or the state file, and it cannot be only the expectation sentence.

## Outcome

```json
{
  "status": "fail",
  "evidence_refs": [".aeos/tests-expert/evidence/login-empty-password.txt"],
  "checks": [
    {
      "id": "login-empty-password",
      "result": "fail",
      "observed": "HTTP/1.1 200"
    }
  ]
}
```

`status` is `pass` only when every frozen check was observed to match the user request. `result` marks each check. `observed` is a quote from the evidence, not a paraphrase invented to match `expect`.
