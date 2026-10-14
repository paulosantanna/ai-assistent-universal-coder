<!-- Package: 00_skills/(development)/specs; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# specs

```yaml
skill:
  name: specs
  slug: specs
  version: 1.0.0
  description: Spec-driven AEOS preflight skill that must run before any AEOS skill creates or alters code, files, architecture, schemas, configuration, documentation, governance, policy, prompts, playbooks, skills, MCPs, LSPs or agent contracts.
  category: GOVERNANCE
  architecture_level: 3
  risk_level: HIGH
  activation:
    - before any AEOS skill is used to create or alter an artifact
    - before implementation, migration, refactor, schema change, configuration change, documentation generation, policy change, skill creation or playbook creation
    - when a request needs requirements, design, task planning, test mapping or approval gates before mutation
  exclusions:
    - read-only inspection with no generated artifact and no modification
    - trivial chat answers that do not create or alter repository, runtime, governance or documentation artifacts
    - emergency containment where a higher-priority human safety boundary explicitly overrides normal sequencing
  inputs:
    - user objective
    - target scope
    - affected artifacts or artifact classes
    - constraints and non-goals
    - evidence refs from repository inspection or external authoritative sources
  outputs:
    - spec package
    - requirements
    - design notes
    - task plan
    - test applicability matrix
    - approval and evidence gates
    - blocking conditions
  tools:
    - filesystem read
    - repository search
    - approved documentation lookup
    - AEOS evidence store
  memory: true
  human_approval: true
  maintainer: AEOS
```
