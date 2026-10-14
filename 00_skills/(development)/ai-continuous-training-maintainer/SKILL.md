---
name: ai-continuous-training-maintainer
description: 'Manter o pipeline de treino contínuo de IA em `E:/GitHub/aidiabetic-research/src/` sempre: 1. Atualizado com **melhores práticas** de engenharia de ML (SOLID, OWASP, OWASP AI) 2. **Livre de CVEs conhecidas** (rastreamento de múltiplas fontes: NVD, GitHub Advisories, OSV, PyPA, etc.) 3. **Auditado por SAST/Trivy** com correção de achados críticos e altos 4. Com **dependências atualizadas** sem quebrar compatibilidade 5. **Sem regressões** — alterações graduais, testadas e com rollback 6. Com **co Use when the user requests ai continuous training maintainer or invokes ai-continuous-training-maintainer. Do NOT use for unrelated languages, domains or production deployment.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Continuous Training Maintainer

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Manter o pipeline de treino contínuo de IA em `E:/GitHub/aidiabetic-research/src/` sempre: 1. Atualizado com **melhores práticas** de engenharia de ML (SOLID, OWASP, OWASP AI) 2. **Livre de CVEs conhecidas** (rastreamento de múltiplas fontes: NVD, GitHub Advisories, OSV, PyPA, etc.) 3. **Auditado por SAST/Trivy** com correção de achados críticos e altos 4. Com **dependências atualizadas** sem quebrar compatibilidade 5. **Sem regressões** — alterações graduais, testadas e com rollback 6. Com **co

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [1. Identity](references/instructions/02-1-identity.md) — before acting on this contract.
- 3. [2. Mission](references/instructions/03-2-mission.md) — before acting on this contract.
- 4. [3. Activation](references/instructions/04-3-activation.md) — when this domain or mode is in scope.
- 5. [4. Non-activation](references/instructions/05-4-non-activation.md) — when this domain or mode is in scope.
- 6. [5. Scope](references/instructions/06-5-scope.md) — before acting on this contract.
- 7. [6. Authority](references/instructions/07-6-authority.md) — before acting on this contract.
- 8. [7. Inputs](references/instructions/08-7-inputs.md) — before acting on this contract.
- 9. [8. Outputs](references/instructions/09-8-outputs.md) — before acting on this contract.
- 10. [9. Preconditions](references/instructions/10-9-preconditions.md) — before acting on this contract.
- 11. [10. Workflow — Mandatory Execution Sequence](references/instructions/11-10-workflow-mandatory-execution-sequence.md) — at this step of execution.
- 12. [11. Tool Policy](references/instructions/12-11-tool-policy.md) — before acting on this contract.
- 13. [12. Evidence Policy](references/instructions/13-12-evidence-policy.md) — before acting on this contract.
- 14. [13. Subagent Policy](references/instructions/14-13-subagent-policy.md) — before acting on this contract.
- 15. [14. Validation](references/instructions/15-14-validation.md) — before claiming completion.
- 16. [15. Stop Conditions](references/instructions/16-15-stop-conditions.md) — when an input, tool or check fails.
- 17. [16. Failure Behavior](references/instructions/17-16-failure-behavior.md) — when an input, tool or check fails.
- 18. [17. Completion Criteria](references/instructions/18-17-completion-criteria.md) — before claiming completion.
- 19. [18. Memory Behavior](references/instructions/19-18-memory-behavior.md) — when reading or promoting continuity knowledge.
- 20. [19. Security Restrictions](references/instructions/20-19-security-restrictions.md) — before acting on this contract.
- 21. [20. CVE Sources (Multi-Source)](references/instructions/21-20-cve-sources-multi-source.md) — when this domain or mode is in scope.
- 22. [21. Examples](references/instructions/22-21-examples.md) — when choosing an output or matching a use case.
- 23. [22. Version](references/instructions/23-22-version.md) — when this domain or mode is in scope.
- 24. [23. MCP Integration](references/instructions/24-23-mcp-integration.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
