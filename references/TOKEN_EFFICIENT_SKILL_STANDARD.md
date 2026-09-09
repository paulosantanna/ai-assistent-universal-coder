# AEOS Token-Efficient Skill Standard

## Objective

Reduce model context consumption without reducing verification depth, security coverage or evidence quality.

This standard optimizes **what is loaded**, not **what is verified**.

## Non-negotiable rule

A token budget may change retrieval order, batching, deduplication and progressive disclosure. It MUST NOT suppress a required security check, test, evidence source, approval gate or risk control.

## Progressive disclosure contract

Every new substantial skill uses:

```text
skill/
├── SKILL.md                  # compact routing + execution contract
└── references/
    ├── INDEX.md              # compact topic index, always cheap to inspect
    └── *.md                  # loaded only when selected by mission/risk
```

The normal context path is:

`registry metadata → SKILL.md → references/INDEX.md → 0..N selected references`

Never load every reference by default.

## Measurable accounting

For each skill-context resolution record exact values:

- `skill_bytes` — UTF-8 bytes loaded from SKILL.md;
- `index_bytes` — UTF-8 bytes loaded from references/INDEX.md;
- `reference_bytes_loaded` — exact bytes of selected references;
- `candidate_reference_bytes` — exact bytes of all candidate references;
- `bytes_avoided` — candidate bytes not loaded;
- `references_selected` and `references_available`;
- hashes of loaded references for cache/deduplication.

Do not report an exact token count unless a tokenizer for the actual target model was used. Byte reduction is exact; token reduction is model/tokenizer dependent.

## Selection

1. Resolve objective, stack/version and risk before loading deep references.
2. Use INDEX tags/keywords to rank references.
3. Load the smallest set that satisfies the evidence need.
4. Default maximum: 3 references for ordinary work, 5 for high/critical-risk work.
5. A required verification source may exceed the reference count limit. Correctness and safety win over budget.
6. Deduplicate identical content by SHA-256 before adding it to context.
7. Prefer pointers/excerpts to repeated full source files.
8. Reuse already verified evidence when its source hash and freshness constraints still match.

## Skill authoring

`SKILL.md` should contain only:

- mission and boundaries;
- invocation criteria;
- BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF procedure;
- required inputs/outputs;
- risk/stop conditions;
- reference-selection instructions.

Long version matrices, checklists, framework details, examples and source catalogs belong under `references/`.

## Security exception

Security skills are allowed to load additional references/checks whenever threat/risk scope requires them. Token optimization MUST NOT create blind spots.

## Verification

A skill is token-efficient only if the system can show fewer exact context bytes were loaded than the available reference corpus while still satisfying its required verification gates. Claims such as “uses fewer tokens” without context accounting are not evidence.
