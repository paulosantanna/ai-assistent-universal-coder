# Tool Adapter Governor

## Mission

Govern every MCP and LSP adapter as a skill-consumed capability. MCPs and LSPs are not decision makers; they are IO, documentation, diagnostics, package, repository, observability or editor adapters invoked only from an active AEOS skill context.

## Mandatory Contract

- Every MCP registry entry must declare `governing_skill`.
- Every MCP call must include an active skill context from the runtime or `__aeosSkillId`.
- Every LSP language profile must declare `governing_skill`.
- Direct MCP/LSP usage without a skill context is a policy bypass and must be blocked.
- Tool calls must be persisted as evidence with the active skill id and governing skill.
- High-impact or broad-context tasks must route through `chromatic-mega-brain` before implementation.

## Execution Rules

1. Route the user request through the skill router.
2. Select the smallest useful skill set.
3. Let selected skills call MCP/LSP adapters through the Tool Router only.
4. Persist evidence, memory updates and any generated artifacts.
5. Block execution when the requested adapter lacks a governing skill or when no active skill is present.

## Quality Gates

- No direct adapter bypass.
- No unregistered MCP/LSP surface.
- No adapter without governing skill.
- No silent fallback to legacy Python or ungoverned scripts.
- No generated skill outside the standard skill builder/factory path.
