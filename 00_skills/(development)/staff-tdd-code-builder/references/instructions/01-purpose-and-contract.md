<!-- Package: 00_skills/(development)/staff-tdd-code-builder; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# staff-tdd-code-builder

```yaml
skill:
  name: staff-tdd-code-builder
  slug: staff-tdd-code-builder
  version: 1.0.0
  description: Staff-level TDD code creation super skill that implements architecture plans with clean code, SOLID, design patterns, security, multi-source CVE screening, aggressive tests, evidence, learning and no source-code comments.
  category: GENERATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests code creation from an architecture plan, TDD implementation, clean code generation, SOLID implementation, design-pattern-driven implementation, secure code generation, or production-grade coding with tests first
    - a project must be implemented after an Architect Staff III plan
    - code must be created or changed with aggressive tests and no source-code comments
  exclusions:
    - architecture planning without an accepted architecture handoff
    - code generation that intentionally bypasses tests without explicit user instruction
    - production deployment without approval
  inputs:
    - architecture plan or approved handoff
    - user objective and acceptance criteria
    - repository path
    - optional instruction to code first then tests
  outputs:
    - implementation diff or generated project
    - test suite and verification report
    - CVE and supply-chain evidence
    - execution artifacts with Memory, Handoff, progress, Learning, evidencias and analise
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
