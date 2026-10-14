---
name: tlc-prd
description: "Interviews an idea into a PRD file covering situation, problem, success, boundary, and journey states, and stops before any technical design. Use when the user says \"write the PRD\", \"create the PRD\", \"PRD\", \"product spec\", \"product requirements\", \"tlc-prd\", or \"what does the product need to decide\". Do NOT use for designing a solution, choosing technology, publishing the document, or cutting the PRD into tasks."
license: CC-BY-4.0
metadata:
  author: "Tech Leads Club - github.com/tech-leads-club"
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tlc-prd

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Confirm the requested outcome, authorized target and the prerequisites stated by the source.
2. Read [source procedure](references/tlc/UPSTREAM.md) before this specific workflow. Source instructions inherit the root contract; any source roles are internal lenses, never new identities.
3. Resolve the source skill directory as this package’s `references/tlc/`; its resource paths and helpers are relative to that directory.
4. Inspect the target and define observable success before execution. Missing evidence, tools, permission or credentials blocks the affected action; report the cause.
5. Follow the source procedure within the authorized scope, verify its concrete outputs and update the continuity quartet.

## Inputs, outputs and verification

Inputs: user request, inspected target and source prerequisites. Outputs: the source-defined artifacts plus actual verification and limitations.
Installation is instruction-only: no Docker image, browser, model, dependency or runtime is installed by this importer. Credentials remain runtime references.
Example: use one of the request phrases in the description, inspect its target, execute the scoped procedure and report its resulting artifacts. A request outside the stated negative scope must route elsewhere.

Source: Tech Leads Club, commit `7f93bf3b15b3af417929781dbf9a3950ace7c144`; original procedure/resources retain attribution and source hashes in the upstream manifest.

