# Defects and adaptation

## Findings

- Upstream `SKILL.md` is 120 physical lines and only a router. The TLC cap is 100, so the rules live in this procedure.
- The description was "Router for all Remotion skills" with no negative boundary and no `metadata.author`.
- `remotion-dev/skills` reports no GitHub license. The nested essays, Mapbox examples, Cesium assets, and duplicated `remotion-markup/remotion-maps` tree were not copied.
- `agents/openai.yaml` is an agent-client profile. It was not copied. This package stays a skill of `codenavi-agent`.
- The docs module embeds an Algolia search key. This rewrite fetches official `.md` pages and does not store that key.
- `npx skills update remotion-best-practices ...` would replace this package with upstream files. The upgrade section forbids that in this workspace.
- Video-layout text opened with "You are designing a video". The rule remains; the persona does not.
- Map technique files repeat the same render-stability note and one static-map file differed between the two copies. Choosing one technique is the rule; the essays are not vendored.
- Version label `4.0.547` is the upstream snapshot, not proof that the user's install matches it.

## Grade

Rubric from `00_skills/(creation)/skill-architect/references/quality-checklist.md`. Not measured routing accuracy.

| Dimension | Weight | Before | After |
| --- | --- | --- | --- |
| routing | 20 | 3 | 4 |
| procedure | 25 | 4 | 4 |
| examples | 15 | 2 | 4 |
| errors | 15 | 3 | 4 |
| disclosure | 15 | 2 | 4 |
| verification | 10 | 2 | 3 |

Before 56.0. After 78.0. Verification stays at 3 because Studio and render were not executed in this workspace.
