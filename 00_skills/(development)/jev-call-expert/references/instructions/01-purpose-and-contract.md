<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

# Jev Call Expert

Governance: CodENavi Full Workspace v2

```yaml
skill:
  name: Jev Call Expert
  slug: jev-call-expert
  version: 2.0.0
  description: Builds confidence-aware natural-language dispatch into ordinary typed functions with TypeSafe Jev while code retains validation, authorization, and execution control. Supports all three primitive types (Choice, Score, Noul), speculative fan-out, confidence-gated routing, and composite scoring.
  category: AI_ML
  architecture_level: 1
  risk_level: HIGH
  activation:
    - Jev or TypeSafe function calling
    - tool routing
    - typed dispatch
    - implementation
    - review
    - confidence-gated routing
    - composite scoring
    - speculative fan-out
  exclusions:
    - generic non-TypeSafe LLM tool calling
    - open-ended text generation
    - unapproved destructive or production execution
  inputs:
    - user objective and representative utterances
    - allowlisted function signatures and side-effect classification
    - target language, runtime, and repository conventions
  outputs:
    - dispatcher implementation or review
    - typed question and execution policy
    - tests, confidence behavior, and evidence
  tools:
    - repository tools
    - live TypeSafe documentation
    - project test runner
    - SDK client (Python or JavaScript)
  memory: false
  human_approval: conditional
  maintainer: AEOS
  owner_agent: codenavi-agent
```
