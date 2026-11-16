---
name: "revisar-pr"
description: "Review a PR diff against requirements and conventions, ranked findings. Use for revisar PR. Do NOT use for security review (revisar-seguranca-pr)."
license: "CC-BY-4.0"
metadata:
  author: "AEOS"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# revisar-pr

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Workflow

1. Inspect the exact repository/PR/head diff, requirement and applicable AGENTS/conventions. Do not infer the requirement from implementation; missing spec limits adherence judgment.
2. Run the [code-review lens](lenses/code-reviewer.md) as a bounded read-only pass of codenavi-agent. Examine every changed file, callers and relevant behavior evidence; exclude author identity from the judgment.
3. Separate introduced problems from pre-existing issues. Report high/medium-confidence findings by blocker/major/minor/nit, with file:line and concrete suggestion; omit unsupported low-confidence claims.
4. Use the verdict format APROVAR / APROVAR COM RESSALVAS / PEDIR MUDANCAS. Include what could not be verified. A sequential lens is not an independent blind agent review.
5. Return the report locally. Remote posting, code fixes and merging require their own authorization; do not infer them from review.

Input: actual diff, spec and repository evidence. Output: verdict, ordered findings, pre-existing observations and missing checks. Source: IMG_2763–IMG_2764.

## Examples and failure handling

Example: “revise this PR against story X” → inspect exact diff/spec and return ordered findings with the code-review verdict; “post the review” is a separate remote action. Error: no spec → leave requirement adherence unverified rather than infer it.

## Retained resources

- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
