# How to Add an AEOS Agent

## Steps

1. Create `aeos/agents/<agent>.agent.md`.
2. Register in `aeos/registries/agents.registry.yaml` or the v0.7 registry overlay.
3. Declare role, allowed delegation, forbidden actions and independence.
4. Define required outputs and evidence.
5. Add tests for scope violations and direct tool bypass.

## Required Agent Contract

- mission
- scope
- allowed skills
- allowed capabilities
- forbidden actions
- context requirements
- evidence requirements
- escalation rules

## Judge Checks

Judge must block if the agent:
- executed tools directly;
- judged its own work;
- expanded scope;
- emitted facts without evidence;
- included secrets;
- bypassed delegation policy.
