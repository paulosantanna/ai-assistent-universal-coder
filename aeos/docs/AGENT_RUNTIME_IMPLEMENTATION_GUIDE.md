# CodENavi Agent Runtime Implementation Guide

Status: CURRENT

## Runtime invariant

AEOS executes with exactly one registered agent identity: `codenavi-agent`.

Specialization is resolved as skills, playbooks, MCPs, LCPs, tools, adapters and critical-thinking lenses. Judge remains an independent deterministic runtime gate/service.

## Minimum vertical slice

```text
aeos run agent-runtime-smoke-test --target <path>
```

Expected evidence includes:

- canonical agent resolution;
- task graph;
- selected skill contexts;
- permission decisions;
- tool/MCP routing decisions;
- evidence references;
- Judge verdict when required;
- final status.

## Initialization order

1. Load `AGENT.md` and workspace governance.
2. Load `aeos/config/agent.runtime.yaml`.
3. Load `aeos/registries/agents.registry.yaml` and fail unless it contains exactly `codenavi-agent`.
4. Load and merge skill/playbook/MCP/LCP registries.
5. Apply CodENavi governance to resolved entries.
6. Load permission, policy, token-budget and Tool Router configuration.
7. Initialize evidence, approval and Judge services.
8. Expose the runtime only after all fail-closed checks pass.

## Mission execution

`BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`

For each mission:

1. resolve the requested playbook or bounded task;
2. build a task graph;
3. route only the necessary context;
4. resolve required skills and allowed MCP/LCP capabilities;
5. check policy and permissions before tool execution;
6. persist evidence and redacted audit data;
7. require approval/rollback for governed high-impact actions;
8. run deterministic verification;
9. obtain Judge verdict when the runtime policy requires it;
10. emit a factual debrief.

## Specialization model

The canonical agent does not create additional identities. Different technical responsibilities are expressed through capability contracts and context slices. Parallel work means parallel bounded steps or tool calls, not parallel personas.

## Failure behavior

The runtime must fail closed when:

- the canonical registry is missing or contains another identity;
- a requested capability is unregistered;
- policy or permission denies an operation;
- mandatory evidence is missing;
- a secret would be exposed;
- required approval or rollback is absent;
- deterministic verification or Judge blocks completion.

## Verification

Before accepting runtime changes:

```text
npm run aeos:guard:single-agent
npm run aeos:verify
```

Use `npm run aeos:verify:full` when integration/tooling changes require the complete Node verification matrix.
