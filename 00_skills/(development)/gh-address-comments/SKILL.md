---
name: gh-address-comments
description: Address review and issue comments on the open GitHub PR for the current branch using gh CLI. Use when user says "address PR comments", "fix review feedback", "respond to PR review", or "handle PR comments". Verifies gh auth first and prompts to authenticate if not logged in. Do NOT use for creating PRs, CI debugging (use gh-fix-ci), or general Git operations.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  short-description: Address comments in a GitHub PR review
  owner_agent: codenavi-agent
---

# PR Comment Handler

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Guide to find the open PR for the current branch and address its comments with gh CLI.

**Prerequisites:** Ensure `gh` is authenticated before running commands. Check authentication status with `gh auth status`. If not authenticated, instruct the user to run `gh auth login` to authenticate with GitHub.

## 1) Inspect comments needing attention

- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification

- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments

- Apply fixes for the selected comments

Notes:

- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
