---
name: demo
description: "Record a demo video of a web app feature or flow on a real desktop (Docker, Xvfb, XFCE, real X cursor), producing an mp4 plus a click/hover/scroll/type telemetry file. Takes a flow description, an existing demo name or path, or init. Use when the user says \"record a demo of the checkout\", \"gravar um demo dessa feature\", \"make a screencast of this flow\", \"video for the changelog\", \"re-record the checkout demo\", \"refresh the demo video\", or \"demo init\". Do NOT use for general browser testing or automation that needs no video (use playwright-skill), page debugging or network inspection (use chrome-devtools), or static screenshots."
license: CC-BY-4.0
metadata:
  author: "github.com/wcalderipe"
  version: 1.0.0
  owner_agent: codenavi-agent
---

# demo

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

Source: Tech Leads Club, commit `3483c99f895c376c2dddc052687907716faa4d96`; original procedure/resources retain attribution and source hashes in the upstream manifest.

