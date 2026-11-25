# Examples

## Examples

**Scenario A — fresh oncology benchmark.** User: *"We're seeing chemo drug names mistranscribed. Where do I start?"* → Step 2a: confirm specialty is oncology, ask about which drugs (immunotherapy biologics, platinum agents, taxanes). Propose ~10 candidates: `cisplatin`, `paclitaxel`, `pembrolizumab`, `nivolumab`, `carboplatin`, `docetaxel`, `bevacizumab`, `trastuzumab`, `cetuximab`, `pemetrexed`. Write `term_seed.csv` with all `entity_category=drug`. Step 2b: brief `/data-designer` for 4 context variants each = 40 sentences. Step 2c: MW lookup for each — biologics like `pembrolizumab` will likely fall to `magpie_g2p`; platinum agents likely hit MW. Step 2d: synthesize one QA wav per term, walk the user through the `pembrolizumab` etc. clips, propose IPA candidates with `-mab` suffix stress patterns. Step 2e: on approval, run 10 terms × 2 voices × 2 noise levels × 3 contexts = 120 rows.

**Scenario B — appending to an existing cycle.** User: *"I have a cycle-1 manifest and I want to add 5 more procedures."* → Re-run only Steps 2a (specialty interview just for the new terms), 2b (sentence gen for the additions), 2c (IPA pipeline for the additions), 2d (audition the new terms), and 2e (synthesize only the new term rows). Append to the existing `manifest.jsonl`. **Do not regenerate audio for existing terms** — cycle isolation is intentional so leaderboards diff cycle N vs cycle N+1 cleanly.

## Out of scope

- scoring
- setup
- fine-tune
