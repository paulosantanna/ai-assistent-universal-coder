---
name: vss-query-analytics
description: "Query read-only VSS analytics. Use for vss query analytics or incidents. Do NOT use for video summarization."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "3.3.0"
  owner_agent: codenavi-agent
---

# VSS Query Analytics

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/vss-query-analytics`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Read incidents, occupancy, speed, places, or sensors from an authorized VSS analytics service.

## Workflow

1. Confirm the analytics service is already configured and the user may read it.
2. Pick the command family from the procedure: incidents, sensors, metrics, or deterministic analysis.
3. Run the read-only CLI. Do not create or edit sensors.
4. Treat a non-zero exit as a failed query and use the troubleshooting notes.
5. Report the command, time window, and rows returned.

## Inputs, outputs, and stop

Inputs: authorized analytics endpoint and the metric or incident question
Outputs: query result and exit status
Stop when a required tool, permission, or evidence check fails. Do not mutate analytics configuration or query a deployment the user does not operate. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
