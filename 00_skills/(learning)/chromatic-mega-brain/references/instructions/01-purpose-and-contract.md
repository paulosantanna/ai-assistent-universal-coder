<!-- Package: 00_skills/(learning)/chromatic-mega-brain; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# AEOS Chromatic Mega Brain

```yaml
skill:
  name: AEOS Chromatic Mega Brain
  slug: chromatic-mega-brain
  version: 1.0.0
  description: Orchestrates multiple bounded cognitive perspectives to analyze complex problems, challenge assumptions, compare alternatives, synthesize evidence and produce governed decisions.
  category: ORCHESTRATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests deep multi-perspective reasoning
    - the user requests architectural or strategic analysis
    - the user requests a Mega Brain or Chromatic analysis
    - the user requests comparison of competing solutions
    - the user requests adversarial review before implementation
  exclusions:
    - trivial factual questions
    - deterministic one-step tasks
    - requests that do not benefit from multiple perspectives
  inputs:
    - user objective
    - optional repository context
    - optional constraints and evidence
  outputs:
    - chromatic analysis
    - decision matrix
    - evidence map
    - synthesized recommendation
    - unresolved risks
  tools:
    - AEOS agents
    - repository tools
    - validators
  memory: true
  human_approval: conditional
  maintainer: AEOS
```
