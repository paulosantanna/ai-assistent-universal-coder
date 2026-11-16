---
name: gh-address-comments
description: "Address review comments on the open GitHub PR of this branch via gh CLI. Use for 'address PR comments'. Do NOT use for CI debugging (gh-fix-ci)."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  short-description: Address comments in a GitHub PR review
  owner_agent: codenavi-agent
---

# PR Comment Handler

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
