# How to Add an AEOS Skill

1. Prefer `skills/skill-factory/scripts/skill_factory.py create` or `generate`.
2. Generate into `aeos/skills/generated` when the skill belongs to the AEOS runtime.
3. Keep registration enabled unless intentionally creating an isolated package.
4. Follow `aeos/docs/specs/AEOS_SKILL_CONTRACT.md`.
5. Follow `aeos/docs/PROMPT_CONTRACT.md`.
6. Keep the generated `AGENT.md`, `knowledge/`, `memory/` and `evaluation/HONEST_EVALUATOR.md` layers.
7. Declare activation and non-activation boundaries.
8. Declare capabilities and forbidden actions.
9. Declare required evidence, output schema, quality gates and stop conditions.
10. Ensure Judge can validate outputs.

Generated skills are registered in `aeos/registries/skills.registry.yaml` by default when the factory can locate an AEOS workspace. Use `--no-register` only for temporary packages that should not be consumed by AEOS immediately.
