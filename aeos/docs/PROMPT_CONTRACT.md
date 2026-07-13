# AEOS Prompt Contract

This contract is the canonical instruction standard for AEOS prompts, skills, MCP definitions, LSP commands and CLI commands.

## Objective

Every prompt must state the concrete task outcome in one bounded objective. Avoid broad assistant identities when a narrower operational role is enough.

## Scope And Boundaries

- Declare what is in scope and what is out of scope.
- Prefer file references, registry IDs and evidence IDs over pasted context.
- Keep work bounded by the current target, profile, policy and permission set.
- Treat missing context as a blocker or an assumption, never as silent permission.

## Required Inputs

Prompts that drive execution must name required inputs. At minimum:

- objective;
- target path, entity ID or artifact reference;
- constraints;
- available evidence refs;
- policy, permission or risk profile when applicable.

## Evidence Rules

- Material factual claims require evidence refs.
- Assumptions must be marked explicitly.
- Test results, command output, generated files and hashes should be captured as evidence when available.
- Do not cite evidence that was not inspected.

## Tool And Permission Boundaries

- Route tool access through the approved Tool Router, MCP runtime or command layer.
- Do not bypass policy, permission, approval, sandbox or registry gates.
- Mutating actions need explicit scope, rollback or approval rules.
- Network, filesystem, shell, package, git and secret access must remain inside the declared MCP or command contract.

## Output Schema

Execution-facing prompts should return:

```json
{
  "status": "PASS|BLOCKED|REVIEW",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "performance": {},
  "blocking_conditions": []
}
```

## Quality Gates

- Facts cite evidence.
- Risks have severity or impact.
- Recommendations include action and rationale.
- Outputs satisfy the requested schema.
- Secrets, tokens, credentials and sensitive values are redacted.
- The result is small enough to be reviewed without hidden context.

## Stop Conditions

Stop and return `BLOCKED` when:

- required input or evidence is missing;
- permission, policy or approval is denied;
- required tool access is unavailable;
- output would expose a secret or sensitive value;
- the requested action exceeds scope;
- validation cannot be completed.

## Surface-Specific Rules

| Surface | Additional rule |
| --- | --- |
| Skill | Define activation, non-activation, scope, evidence, quality gates and completion criteria. |
| MCP | Define capabilities, risk, approval rules, redaction, path/network boundaries and stop conditions. |
| LSP | Prefer previews and diagnostics; never mutate workspace state from an explanation command. |
| CLI command | Make dry-run and evidence behavior visible; return clear exit status and actionable errors. |
| Prompt pack | Keep reusable prompts schema-bound and avoid project-specific claims without inputs. |
