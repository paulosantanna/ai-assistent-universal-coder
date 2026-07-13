# Enterprise Playbook: language-upgrade-research-implementation

## Objective

Start a language or runtime upgrade with official documentation research,
compatibility analysis, implementation plan, tests and rollback evidence.

## Inputs

- target project path;
- source language/runtime version;
- target language/runtime version;
- framework versions;
- deployment target;
- test command allowlist.

## Required Agents

- Root
- Language Researcher
- Architect
- Coder
- Tester
- Security
- Judge

## Required MCPs

- filesystem-readonly
- filesystem-write-sandbox
- git-readonly
- test-runner-controlled
- complete-docs
- docs-java-11, when Java 11 is involved
- docs-java-17, when Java 17 is involved
- docs-java-21, when Java 21 is involved
- docs-java-25, when Java 25 is involved
- docs-java-26, when Java 26 is involved
- docs-python-current, when Python is involved
- docs-node-current, when Node.js is involved
- docs-typescript-current, when TypeScript is involved
- docs-angular-current, when Angular is involved
- docs-javascript-current, when JavaScript is involved

## Execution Flow

1. Capture repository status and current runtime files with read-only MCPs.
2. Select only the documentation MCPs for the source and target runtimes.
3. Run:
   - `language_docs.version_status`;
   - `language_docs.migration_delta`;
   - `language_docs.source_policy`;
   - `language_docs.lookup_symbol` for deprecated or changed APIs.
4. Build a compatibility matrix for syntax, standard library, dependencies, build
   system, tests, containers, CI and deployment runtime.
5. Generate a sandbox migration plan:
   - file change manifest;
   - dependency update plan;
   - test plan;
   - rollback plan;
   - risk register.
6. Apply implementation only in sandbox until approved.
7. Run allowed tests and language-specific validators.
8. Generate a documentation package with `complete-docs`.
9. Run Judge and block merge if compatibility evidence is incomplete.

## Blocking Conditions

- source or target version is unknown;
- official documentation is not available through the selected MCP;
- dependency compatibility is unknown;
- test suite cannot run and no alternative verification exists;
- rollback plan is missing;
- generated files are not traceable;
- Judge does not pass.

## Outputs

- `.aeos/reports/{execution_id}/language-upgrade-research.md`
- `.aeos/evidence/{execution_id}/migration-delta.json`
- `.aeos/tmp/{execution_id}/upgrade-sandbox/`
- `.aeos/reports/{execution_id}/compatibility-matrix.md`
- `.aeos/reports/{execution_id}/rollback-plan.md`
