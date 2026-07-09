# AEOS v0.7 Roadmap

## Sprint 1 — Agent Runtime Contracts

- AgentMessage
- TaskDefinition
- TaskResult
- AgentState
- AgentTrace

## Sprint 2 — Agent Registry Loader

- load agent runtime config
- validate agents
- validate subagents
- validate capabilities
- validate forbidden actions

## Sprint 3 — Task Graph

- create task graph from playbook
- dependency handling
- blocking conditions
- task status transitions

## Sprint 4 — Context Router

- load LCPs by task
- load memory by scope
- minimize context
- prevent secret leakage

## Sprint 5 — Delegation Policy Engine

- validate who can delegate to whom
- validate scope
- validate capabilities
- validate escalation rules

## Sprint 6 — Agent Trace Store

- persist agent-trace.jsonl
- persist task-results
- link evidence refs
- hash outputs

## Sprint 7 — Judge v7

- direct tool bypass detection
- self-judging detection
- unresolved task detection
- memory evidence checks
- high-risk task review checks
