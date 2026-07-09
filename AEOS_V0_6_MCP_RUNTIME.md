# AEOS v0.6 — MCP Runtime Expansion Layer

## Mission

AEOS v0.6 introduces a controlled MCP Runtime layer that allows AEOS to connect to external capabilities through governed connectors.

MCPs are not permissions. MCPs are integration adapters.

Every MCP call must pass through:

```text
Agent
  -> Skill Executor
  -> Playbook Engine
  -> Kernel Runtime
  -> Permission Engine
  -> Policy Engine
  -> Tool Router
  -> MCP Registry
  -> MCP Runtime
  -> MCP Server / Adapter
  -> Evidence Store
  -> Judge
```

## Core Rule

No agent may invoke an MCP server directly.

## Scope v0.6

Allowed:

- filesystem read-only;
- filesystem write only inside `.aeos/sandbox/**`, `.aeos/reports/**`, `.aeos/evidence/**`, `.aeos/patches/**`, `.aeos/packages/**`;
- git read-only;
- test runner through allowlist;
- package local verify/inspect/create/extract-to-staging;
- MCP health check;
- MCP tool discovery;
- MCP call evidence logging.

Not allowed:

- unrestricted shell;
- browser login;
- secrets value reading;
- database mutation;
- cloud mutation;
- deploy;
- git push;
- git merge;
- force push;
- filesystem delete outside sandbox.

## Required Runtime Features

1. MCP process lifecycle management.
2. stdio transport support.
3. tool discovery with allowlist.
4. input validation.
5. output validation.
6. timeout and retry policy.
7. redaction.
8. evidence logging.
9. health check.
10. Judge verification of tool calls.

## MCP Risk Levels

```text
low      -> read-only, non-sensitive
medium   -> writes to sandbox or local generated artifacts
high     -> branch/commit/test runner with controlled side effects
critical -> secrets, deploy, database write, production mutation
```

v0.6 must not enable critical MCPs by default.
