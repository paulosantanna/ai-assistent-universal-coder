---
name: "subagent-creator"
description: "Design bounded sequential lenses of codenavi-agent with a single deliverable, explicit evidence packet, minimal tools and verifiable verdict. Use for create verifier, parity auditor, isolated review procedure or specialized work unit. Do NOT use for creating, register or spawn agent identities; use skill-architect for a reusable skill and cursor-subagent-creator for Cursor work-unit guidance."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# subagent-creator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Discover the work before choosing a role: one deliverable; judging or producing; which information must be excluded to make the judgment meaningful.
2. Classify the work as audit, research or execution. Audit reads supplied evidence only; research may use approved read/search tools; execution may write or run tools only in authorized scope. Shell execution can write even without an edit tool.
3. Read [lens contract](references/lens-contract.md) and choose the smallest tool set. A Markdown tool list is an instruction boundary, not proof of runtime enforcement.
4. Write one lens under `00_skills/(category)/host-skill/lenses/name.md`. State owner codenavi-agent, inputs and excluded information, numbered observable criteria, exact output and stop rule.
5. Use [parity lens](../../(architecture)/legacy-migration-planner/lenses/parity-auditor.md) for migration result comparison. Keep diff, author, commit history and intent out of its evidence packet.
6. Verify the file/link and perform the bounded lens pass in this thread. Report context contamination, missing evidence and remaining limitations; never claim true independent context from a sequential self-review.

## Boundaries

Never create .devin/agents, AGENT.md profiles, agent: bindings or agents registries. Existing AGENTS.md stays authoritative and unchanged. Source runtime claims about background tools, default models and builtin names are host-specific, not guarantees here.
For audit: missing evidence means INCONCLUSIVO, not approval. List what could not be checked; do not fix or suggest fixes in a parity verdict. For a repository scan, return only requested repo/path:line matches unless synthesis was requested.
Source: IMG_2700–IMG_2704. Output: a linked lens procedure and truthful verdict, not a new assistant identity.

## Examples and failure handling

Example: “create a parity verifier” → a local lens with antes/depois evidence and enumerated criteria; “scan this fleet for library X” → bounded repo/path:line matches. Failure: missing runtime enforcement or contaminated context → disclose the limitation, never add another identity.

## Retained resources

- Read [retained ORIGINAL_SKILL](references/ORIGINAL_SKILL.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained package-notes](references/package-notes.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained tlc](references/tlc) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
