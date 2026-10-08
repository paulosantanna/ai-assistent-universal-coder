# tests-expert

Entry: `skills/tests-expert/SKILL.md`
Updated: 2026-10-08

- Oracle is the user request. The implementation is only a way to reach the surface.
- `scripts/charter.mjs` freezes that oracle. An unchanged request with edited expectations exits 2.
- A failed run writes `.aeos/tests-expert/RESUME.md` (gitignored) and exits 3. PASS deletes it.
- Cursor loads `.agents/skills/tests-expert/SKILL.md`, which points at the canonical skill.
- Router boost: `scripts/aeos-skill-router.mjs`. Overlay: `aeos/registries/skills.tests-expert.additions.yaml`.
