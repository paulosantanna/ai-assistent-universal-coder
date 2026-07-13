# Skill: tool-router-audit

## Mission

Audit whether AEOS code and playbooks enforce Tool Router for every external action.

## Checks

- direct filesystem access
- direct Git mutation
- direct subprocess calls
- direct HTTP calls to tools
- direct secret access
- missing tool-call evidence

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- No direct tool bypass.
- Every action maps to a Tool Router call.
- Every action creates permission and policy decisions.
