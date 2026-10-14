# HONEST_EVALUATOR.md

Use this checklist before marking work complete.

## Extremely Honest Review

- What evidence directly supports each material claim?
- What is assumed, guessed or still unverified?
- What would fail in production, CI or a fresh workspace?
- What user-visible risk remains after the proposed result?
- Did any tool, permission, policy or registry boundary get bypassed?
- Are secrets, tokens, credentials and sensitive values redacted?

## Verdict Rules

- Return `PASS` only when evidence and validation support completion.
- Return `REVIEW` when the result is useful but needs human judgment.
- Return `BLOCKED` when required input, evidence, permission, tool access or validation is missing.
