# Skill: Architecture Mapper

## Mission

Analyze a codebase structure and produce an architectural map including modules, dependencies, layers, and patterns.

## Allowed Actions

- Read source files.
- List directories and module structures.
- Detect architectural patterns (MVC, hexagonal, layered, etc.).
- Map module dependencies.
- Detect configuration and routing files.
- Generate Architecture Decision Records (ADRs).
- Generate Markdown reports.

## Forbidden Actions

- Edit source files.
- Delete files.
- Execute commands.
- Access runtime environments.
- Declare architectural degradation without evidence.

## Inputs

- workspace path
- scan depth
- existing ADR directory

## Outputs

- architecture-map.md
- module-dependency-graph.md
- adr/*.md
- tech-debt-report.md

## Evidence Required

- module structure
- dependency declarations
- framework configuration files
- detected patterns with file citations
- routing/endpoint definitions

## Quality Gates

- Must cite specific files for each architectural claim.
- Must distinguish observed patterns from inferred intent.
- Must flag inconsistent patterns.
- Must produce actionable ADR proposals.
