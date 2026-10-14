<!-- Package: 00_skills/(mapping)/documentation-11-layer-mapper; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# documentation-11-layer-mapper

```yaml
skill:
  name: documentation-11-layer-mapper
  slug: documentation-11-layer-mapper
  version: 1.0.0
  description: Generate 11-layer project documentation with client, developer, director and product-owner views, data dictionary, Mermaid diagrams on white background, endpoint integration maps and end-to-end functional documentation.
  category: DOCUMENTATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests 11-layer documentation, complete project documentation, client dev director PO views, data dictionary, Mermaid diagrams, endpoint integration diagrams, relational diagrams, concept diagrams, database diagrams or end-to-end documentation
    - the ai-production-autopilot playbook reaches documentation and release-readiness waves
  exclusions:
    - one-off notes that do not require complete project documentation
    - documentation that would expose secrets or protected data
    - production readiness claims without implementation and verification evidence
  inputs:
    - architecture handoff
    - implementation handback
    - repository path
    - evidence index
    - stakeholder audience requirements
  outputs:
    - 11-layer documentation package
    - stakeholder views for client, developer, director and product owner
    - Mermaid diagrams with white background
    - data dictionary and endpoint integration map
    - documentation evidence and honest evaluator verdict
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
