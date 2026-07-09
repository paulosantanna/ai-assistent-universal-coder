# Playbook: agent-delegated-project-analysis

## Objective

Run project analysis through controlled agent delegation.

## Agents

- Root
- Planner
- Architect
- Security
- Documenter
- Judge

## Subagents

- java-analyzer, when Java indicators exist
- python-rag-analyzer, when Python AI indicators exist
- dependency-risk-analyzer
- security-secret-detector
- docs-adr-writer

## Steps

1. Root receives goal.
2. Planner creates task graph.
3. Context Router creates context packets.
4. Architect delegates stack analysis to subagents.
5. Security delegates secret risk review.
6. Documenter creates evidence-based summary.
7. Agent Trace Store persists trace.
8. Judge validates task graph, context, delegation, evidence and outputs.

## Outputs

- task-graph.json
- context-packets/
- subagent-results/
- agent-trace.jsonl
- delegated-project-analysis.md
- judge-report.md
