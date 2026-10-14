---
name: "revisar-pr"
description: "Review a concrete pull-request diff against its requirement, behavior, contracts and repository conventions; return evidence-ranked findings and a local verdict. Use for revisar PR, parecer do diff or code review. Do NOT use for deep security review (revisar-seguranca-pr), remediate unless requested, post a review or decide/execute merge."
license: "CC-BY-4.0"
metadata:
  author: "AEOS"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# revisar-pr

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

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
