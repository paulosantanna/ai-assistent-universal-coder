# Skill: Repo Scanner

## Mission

Analyze a local repository or ecosystem folder and generate a factual technical map.

## Allowed Actions

- Read files.
- List directories.
- Detect languages.
- Detect build tools.
- Detect frameworks.
- Detect Docker/CI/test files.
- Generate Markdown reports.

## Forbidden Actions

- Edit source files.
- Delete files.
- Execute destructive commands.
- Read secrets values.
- Persist credentials.
- Declare conclusions without evidence.

## Inputs

- workspace path
- scan depth
- ignored directories
- output directory

## Outputs

- ecosystem-map.md
- stack-report.md
- risk-report.md
- recommended-playbooks.md
- evidence/index.md

## Evidence Required

- files inspected
- stack indicators
- dependency files
- detected risks
- confidence level

## Quality Gates

- Must cite detected files.
- Must distinguish facts from assumptions.
- Must produce risk report.
- Must produce recommended next actions.
