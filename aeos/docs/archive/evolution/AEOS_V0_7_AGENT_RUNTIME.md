# AEOS v0.7 — Agent Runtime & Delegation Layer

## Mission

AEOS v0.7 introduces a controlled Agent Runtime capable of orchestrating agents and subagents through explicit contracts, task graphs, context routing, memory governance, evidence, and Judge validation.

## Core Rule

Agents do not execute tools directly. Agents produce intentions, plans, task requests, tool requests, and evidence requirements. Execution remains governed by Kernel, Permission Engine, Policy Engine, Tool Router, MCP Runtime, Evidence Store, and Judge.

## Agent Runtime Scope

Allowed:

- create task graph;
- assign tasks to agents;
- create subagent task requests;
- route context by LCP and memory rules;
- collect agent outputs;
- detect conflicts between agents;
- escalate to human approval;
- call Tool Router indirectly through Skill Executor;
- register agent traces.

Not allowed:

- direct filesystem/Git/shell/MCP calls;
- self-approval;
- bypassing Judge;
- persisting secrets in memory;
- delegating forbidden capabilities;
- modifying protected branches;
- auto-merge or auto-deploy.

## Agent Runtime Pipeline

```text
User Goal
  -> Kernel Runtime
  -> Playbook Engine
  -> Agent Runtime
  -> Root Agent
  -> Planner
  -> Task Graph
  -> Agent Assignment
  -> Skill Executor
  -> Tool Router
  -> Evidence Store
  -> Judge
```

## Key Components

```text
AgentRuntime
AgentRegistry
AgentSupervisor
TaskGraph
TaskScheduler
DelegationPolicyEngine
AgentMessageBus
ContextRouter
MemoryGateway
EscalationGateway
AgentTraceStore
JudgeGateway
```
