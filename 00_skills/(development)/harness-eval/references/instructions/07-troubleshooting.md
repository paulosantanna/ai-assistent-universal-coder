<!-- Package: 00_skills/(development)/harness-eval; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

### Trap gate FAIL (Track B or C)

Cause: KEEP/KEEP-CORE plants were deck duplicates, or blind judge mis-family. Solution: use skill’s fixed plant templates; rescore plants; re-merge.

### Track A false missing `.agents/...`

Cause: bad path normalization. Solution: skill script must use `normalize_cite` (strip `./` only). Re-run Track A from `$SKILL_DIR/scripts/`.

### Subagent blocked

Cause: missing/allowlisted model or `*-fast` blocked. Solution: re-spawn with an allowlisted non-fast model.

### Track C Slim looks wrong after model change

Expected: usefulness is model-sensitive. Re-run C1+C2 on a second model; intersection of Slim bands is the safe delete set.

### Mixed apply rewrote conventions / removed modules

Cause: apply agent re-judged from the Mixed path list instead of following KEEP/CUT. Solution: apply only via `11-mixed-apply.md`; if that file is missing, re-run `merge_usefulness.py`; if Keep-core/Slim cells are vague, re-score those IDs before apply.

### T2 empty / skill `references/` missing from inventory

Cause: path normalize used `lstrip("./")` and turned `.agents/…` into `agents/…`. Solution: `doc_scope.normalize_rel` must strip only a `./` prefix (same rule as Track A).

### ADRs appeared in Track C

Cause: old inventory treated all one-hop `docs/**` as T2. Solution: v1.7+ excludes decision-record trees; only user-approved optional doc types (never ADR/RFC) can enter T2.

### Slim stub broke another skill that loads that file

Cause: content OVERLAP/Slim without fan-in — older runs, or apply skipped the gate. Solution: restore the checklist body; re-merge with `merge_usefulness.py` (fan-in scans full skill trees). Confirm with `slim_fanin.py --path <P>`.

### Scripts missing

Cause: incomplete skill folder. Solution: restore `$SKILL_DIR/scripts/` and `references/`.
