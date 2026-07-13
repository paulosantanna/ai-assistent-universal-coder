# Diff Reviewer Skill

**ID:** diff-reviewer
**Version:** 1.0.0
**Owner Agent:** architect
**Risk Level:** low

## Mission
Review generated diffs/patches for correctness, safety, and alignment with evidence.

## Scope
- Read proposed.patch files
- Validate diff syntax and structure
- Check that changes align with issue description
- Identify potential issues in proposed changes

## Allowed Actions
- `filesystem.read` — read patch files and source files
- `generate_evidence` — register review findings

## Forbidden Actions
- Modify patch files
- Apply patches
- Change patch content

## Required Capabilities
- READ_REPOSITORY
- REVIEW_DIFF
- GENERATE_REPORT

## Required Evidence
- Patch file reviewed (SHA-256)
- Source files referenced (SHA-256)
- Review report

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- Every review claim must reference specific diff lines
- False positives must be marked as Assumption, not Fact

## Blocking Conditions
- Patch references non-existent files
- Patch contains syntax errors in diff format

## Examples of Allowed Behavior
- Review that proposed.patch correctly fixes the target issue
- Identify that a proposed change would break API compatibility

## Examples of Forbidden Behavior
- Editing the patch to fix issues
- Approving the patch for application