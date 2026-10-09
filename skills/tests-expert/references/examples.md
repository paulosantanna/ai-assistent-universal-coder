# Examples

## Bug fix

User says: "o login aceita senha vazia; corrija."

Actions: freeze one `http` or `browser` check whose expectation is "an empty password is rejected and no session starts". Submit an empty password to the running application.

Result: HTTP 200 plus a session cookie is FAIL. `record` exits 3 and writes `RESUME.md`. Fix login in this window, or in a later window that reads `RESUME.md` first, and record again against the same charter. PASS is exit 0 only after a rejection is in the evidence.

## New behavior

User says: "ao salvar o perfil sem nome, mostre a mensagem Nome obrigatório."

Actions: one `browser` check that submits the profile with an empty name.

Result: the page shows that message. Do not add checks for fields the user did not mention, and do not read the component to decide the message text.

## Tamper

The empty-password check failed because the app still opened a session. Rewriting `expect` to "a session starts" exits 2 with `ORACLE_TAMPERED`. Restore the frozen expectation and fix login.

## Not this skill

User says: "gere testes unitários da classe UserService."

Result: do not run this skill. That request is a unit test of a class, which `test-writer` may handle. This skill does not turn the class into the oracle.
