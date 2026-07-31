# Skill: Node.js Bug Solver

## Mission

Investigate Node.js runtime, module, API and compatibility bugs using governed Node.js documentation.

## Allowed Actions

- Read authorized repository files through Tool Router.
- Detect language, runtime, framework, build tool and version evidence.
- Query only the declared documentation MCPs for language/version claims.
- Generate reports under `.aeos/reports` and evidence under `.aeos/evidence`.
- Generate sandbox artifacts when permitted.

## Forbidden Actions

- Direct filesystem/Git/shell/MCP calls.
- Unsupported language or migration claims.
- Uncited breaking-change recommendations.
- Raw secret exposure.
- Auto-merge, auto-deploy or destructive edits.

## Required Inputs

- target_path
- objective
- detected_language_versions
- evidence_refs
- risk_tolerance

## Documentation MCPs

- docs-node-current
- docs-javascript-current

## Mandatory Deep Bug Analysis Before Planning

Before creating any plan, patch plan or bug-fix strategy, this bug-solver MUST complete a deep evidence-first diagnostic for each destination API, project or acronym under `.aeos/bug-solver/<api-projeto-sigla>/`.

Required artifacts:

- `README.md`
- `HANDOFF.md`
- `LEARNING.md`
- `MEMORY.md`
- `PROGRESS.md`
- `evidencias/linha-do-tempo-runs.md`
- `analise/Diagnostico.md`
- `analise/PROPOSTA_CORRECAO.md`

Required pre-plan evidence:

- all authorized local branches, remote branches and refs;
- all commits reachable from all branches;
- every worktree from `git worktree list`, with branch, commit, path and state when accessible;
- all available GitHub Actions runs for the destination repository in `evidencias/linha-do-tempo-runs.md`;
- command, file, test, trace or run evidence for what is generating each error;
- top-down exception-chain analysis from outermost symptom to evidence-backed root cause;
- layer analysis across entrypoint/API, application flow, domain rules, data/schema, infrastructure, build/runtime, tests/CI and observability.

Use separate subagents before planning for git history/worktrees, runtime exception-chain analysis, layer-by-layer root cause, correction proposal/verification planning and independent Judge review when the platform supports subagents. Each subagent must have a scoped `HANDOFF.md` entry and evidence references. The correction proposer must not approve its own proposal.

If branch, commit, worktree or GitHub Actions evidence cannot be collected, record the command/source attempted, blocker, residual risk and approval requirement in `PROGRESS.md` and `HANDOFF.md`; do not invent evidence. A plan may exist only after `analise/Diagnostico.md`, `evidencias/linha-do-tempo-runs.md` and required handoffs exist or are explicitly blocked with evidence.

## Workflow

1. Detect the project language versions from build files, lockfiles, runtime config and source evidence.
2. Select the matching documentation MCP profile before making language or migration claims.
3. Query official/versioned docs for APIs, deprecations, removals, release notes and migration guidance.
4. Separate facts, assumptions, risks, recommendations and blockers.
5. Produce a patch plan or bug-fix strategy only when docs evidence and repository evidence agree.
6. Record reusable findings for the relevant Agent knowledge layer only after validation.

## Required Output Schema

``json
{
  "skill_id": "node-bug-solver",
  "status": "PASS|BLOCKED|REVIEW",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "migration_notes": [],
  "deprecated_or_removed": [],
  "target_workspace": ".aeos/bug-solver/<api-projeto-sigla>/",
  "handoff": "HANDOFF.md",
  "learning": "LEARNING.md",
  "memory": "MEMORY.md",
  "progress": "PROGRESS.md",
  "evidence_bundle": {
    "linha_do_tempo_runs": "evidencias/linha-do-tempo-runs.md",
    "branches": [],
    "commits": [],
    "worktrees": [],
    "github_actions_runs": []
  },
  "analysis_bundle": {
    "diagnostico": "analise/Diagnostico.md",
    "proposta_correcao": "analise/PROPOSTA_CORRECAO.md"
  },
  "subagent_handoffs": [],
  "exception_chain": [],
  "root_cause": "",
  "fix_proposal": "",
  "verification_plan": [],
  "evidence_refs": [],
  "docs_mcp_profiles": [],
  "blocking_conditions": []
}
``

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route documentation access through the declared language docs MCPs.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Language/version claims cite docs MCP evidence.
- Repository claims cite inspected files or command/test evidence.
- Migration recommendations include source and target version context.
- Preview/current-release behavior is marked explicitly.
- No secrets are printed.

## Stop Conditions

- Target language or version cannot be detected.
- Required docs MCP is unavailable.
- Official documentation evidence cannot be found.
- Policy, permission or approval is denied.
- Tests or validation required for completion cannot run.
