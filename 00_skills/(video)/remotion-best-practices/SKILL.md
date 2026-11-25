---
name: remotion-best-practices
description: "Write frame-driven Remotion videos and open Studio. Use for remotion studio or a composition. Do NOT use for unrelated React apps."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Remotion best practices

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: TLC rewrite of public Remotion skills `4.0.547` at `a3f4098a`. Not a Remotion-maintained copy. Read [provenance](references/provenance.md).

## Outcome

Create or change a Remotion video with frame-driven markup, a Studio preview when the project runs, and a render only when the user asks for one.

## Workflow

1. Inspect the folder, including hidden files, and the installed `remotion` version. Keep surprising user edits.
2. Route the task: scaffold, markup, elements, maps, captions, Studio, render, SaaS, upgrade, or license.
3. Read the matching procedure section, then the current official `.md` page, before calling an API.
4. Open Studio once the project can run and the user is editing a video. Pass a composition id when rendering.
5. Report commands, the composition id, and any step that did not run.

## Inputs, outputs, and stop

Inputs: the user goal, the project folder, and permission to install, scaffold, or render.
Outputs: the composition change, the Studio URL when started, and render evidence only if a render ran.
Stop when a required tool, permission, or evidence check fails. Do not scaffold over meaningful files, echo a license key, or start Lambda, Vercel, or Cloudflare rendering without confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before writing markup or running a Remotion command.
- Read [topics](references/topics.md) to choose the official doc page for the current mode.
- Read [effects](references/effects.md) before applying a visual effect.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream claim or copying a nested skill.
- Read [provenance](references/provenance.md) when citing version, license, or what was not copied.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
