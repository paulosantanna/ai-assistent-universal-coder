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

## Quality Gates

- No direct tool bypass.
- Every action maps to a Tool Router call.
- Every action creates permission and policy decisions.
