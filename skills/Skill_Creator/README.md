# AEOS Skill Factory

A governed meta-skill that creates, validates and packages new AEOS skills.

## Package location

```text
skills/skill-factory/
```

## Generate a new skill

```bash
python skills/skill-factory/scripts/skill_factory.py generate \
  --name "Security Audit" \
  --description "Audit repository security controls and produce evidence-based findings." \
  --activation "the user requests a repository security audit" \
  --category SECURITY \
  --level 3 \
  --risk HIGH \
  --output skills
```

## Validate an existing skill

```bash
python skills/skill-factory/scripts/skill_factory.py validate skills/security-audit
```

## AEOS routing rule

Register the skill with highest priority for semantic intents involving:

- creating new skills;
- generating `SKILL.md`;
- converting repeatable workflows into skills;
- auditing or restructuring existing skills.

Suggested registry entry:

```yaml
- id: skill-factory
  path: skills/skill-factory/SKILL.md
  priority: 1000
  activation:
    semantic:
      - create a new skill
      - generate a skill
      - add a skill to AEOS
      - convert workflow into skill
      - improve an existing skill
  exclusions:
    - human résumé skills
    - game skills
    - programming functions named skill
```
