---
name: vss-search-archive
description: "Search an authorized VSS archive or RTSP index. Use for vss search archive. Do NOT use for summarization."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "3.3.0"
  owner_agent: codenavi-agent
---

# VSS Search Archive

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/vss-search-archive`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Search video already registered on a VSS deployment the user administers.

## Workflow

1. Confirm the deployment and the source scope. Do not widen an empty scope into every camera.
2. Run vss search through the CLI with only the filters the user asked for.
3. Keep timestamp bounds explicit when the user gave them.
4. Verify result identity before answering a follow-up.
5. Send summaries to vss-summarize-video and single-clip questions to vss-ask-video.

## Inputs, outputs, and stop

Inputs: authorized VSS deployment, registered sources, and the search text
Outputs: result list with the exact query and scope
Stop when a required tool, permission, or evidence check fails. Do not ingest, delete, or discover sources from this skill. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
