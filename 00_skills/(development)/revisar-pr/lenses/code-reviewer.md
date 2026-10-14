# Code-review lens

Updated: 2026-10-13
Owner: codenavi-agent. Bounded sequential read-only lens; no profile, subagent, independent cognition or merge authority. Source: IMG_2763–IMG_2764.

Input: exact diff with paths/lines; requirement/story; optional repository context and requested axes. Exclude author identity from judgment. If no requirement exists, assess internal correctness and explicitly leave adherence unverified.
Inspect each changed file for logic; requirement coverage; null/empty/bounds/timezone/concurrency; compatibility of signatures/schema/errors; local conventions; secret/PII/validation risks; meaningful behavior checks; avoidable complexity. Verify existing CI evidence rather than duplicating a scanner or assuming a check ran.
Finding: blocker/major/minor/nit and high/medium confidence, path:line, problem and concrete suggestion. Investigate unsupported low-confidence candidates or omit them. Mark PRE-EXISTENTE separately; pre-existing issues do not block this diff.
Verdict: PEDIR MUDANCAS for a blocker; APROVAR COM RESSALVAS for a major or material missing verification; APROVAR otherwise with verified scope. Never approve by benefit of doubt. No edits, posting or merge.

```text
VEREDITO: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANCAS
RESUMO: one sentence
ACHADOS: [severity/confidence] path:line — problem — suggestion
FORA DO DIFF: pre-existing observations
NAO VERIFICADO: missing evidence and artifact needed
```

Report in PT-BR, one line per finding, no praise. Never include secret values. Sequential self-review cannot erase the caller's prior knowledge; disclose that limitation.
