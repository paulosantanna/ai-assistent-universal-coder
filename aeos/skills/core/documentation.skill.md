# Skill: Documentation

## Mission

Generate comprehensive, accurate, and maintainable documentation for a codebase, including architecture, APIs, and operational procedures.

## Allowed Actions

- Read source files and project structure.
- Read existing documentation.
- Generate Markdown documentation files.
- Generate ADR documents.
- Generate runbooks.
- Generate API reference documentation.
- Validate documentation against standards.

## Forbidden Actions

- Edit source code.
- Delete existing documentation without evidence.
- Generate documentation that contradicts code.
- Include secrets or credentials in output.
- Claim functionality not present in code.

## Inputs

- workspace path
- documentation scope
- output directory
- style guide / standards LCP

## Outputs

- architecture-documentation.md
- adr-directory/*.md
- api-reference.md
- runbook.md
- operational-guide.md

## Evidence Required

- source files cited for each documented component
- architecture map
- detected patterns
- public API signatures

## Quality Gates

- Must reflect actual code, not intent.
- Must cover all public APIs.
- Must include at least one diagram (ASCII or Mermaid).
- Must pass documentation standards validation.
