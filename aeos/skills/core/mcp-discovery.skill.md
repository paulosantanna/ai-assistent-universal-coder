# Skill: mcp-discovery

## Mission

Discover and validate MCP tools and capabilities against AEOS policies.

## Output

- tools discovered
- capabilities discovered
- allowlist comparison
- blocked tools
- risk classification

## Blocking Conditions

- unknown high-risk tool
- forbidden capability
- critical MCP enabled
- missing evidence

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.
