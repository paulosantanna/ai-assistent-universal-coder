<!-- Package: 00_skills/(development)/solve-problems; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# solve-problems

```yaml
skill:
  name: solve-problems
  slug: solve-problems
  version: 1.0.0
  description: Universal Staff-level problem solver that receives an error report, detects the affected language and repository context, reads the failing code, produces the simplest clean fix in the same language, verifies it, and records governed Memory, Handoff, progress, Learning, evidencias and analise artifacts without changing project architecture.
  category: REPAIR
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests solve-problems, language-independent bug fixing, error report repair, stack trace repair, failing test repair, CI log repair, pod log repair, telemetry bug repair, or code correction without architecture changes
    - an error report must be fixed in the language of the affected files
    - a repository bug must be corrected with Memory, Handoff, progress, Learning, evidencias and analise artifacts
  exclusions:
    - feature work unrelated to an error report or verified defect
    - architecture redesign, directory restructuring or framework replacement
    - direct production mutation, deployment, credential handling or destructive action without approval
  inputs:
    - error report, stack trace, failing command, CI log, pod log, telemetry log or user-described defect
    - repository path
    - optional project, repo, org and API acronym memory scope
  outputs:
    - corrected code in the same language as the affected file or a blocked report
    - execution bundle with Memory, Handoff, progress, Learning, evidencias and analise
    - tests, logs and evidence index
    - honest evaluator decision and selected correction proposal
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
