<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# AEOS Skill Factory

> **Canonical AEOS meta-skill for creating, validating, evolving and governing new skills.**
>
> This skill must be activated whenever the user asks any AEOS-compatible AI to:
>
> - create a skill;
> - generate a new skill;
> - build a reusable capability;
> - add a skill to AEOS;
> - convert a workflow, prompt, playbook or recurring task into a skill;
> - improve, refactor, audit or standardize an existing skill;
> - generate a skill package, skill folder or `SKILL.md`.

---

```yaml
skill:
  name: AEOS Skill Factory
  slug: skill-factory
  version: 1.0.0
  description: Creates, validates, packages and governs new AEOS skills.
  category: ORCHESTRATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - requests to create, generate, improve or audit an AEOS skill
  exclusions:
    - human competency lists
    - game abilities
    - unrelated programming functions
  inputs:
    - user intent
    - optional repository context
  outputs:
    - validated AEOS skill package
  tools:
    - Python
    - filesystem
  memory: true
  human_approval: conditional
  maintainer: AEOS
```
