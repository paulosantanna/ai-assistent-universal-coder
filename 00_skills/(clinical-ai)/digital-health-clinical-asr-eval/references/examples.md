# Examples

## Examples

**Scenario A — first eval on a fresh cycle-1 manifest.** User: *"I have `manifest.jsonl` with 200 clinical audio rows already, with `term` and `entity_category` fields. How do I score it?"* → Skip Stage 2 entirely. Run the audio-existence pre-flight. Pick `parakeet-tdt-0.6b-v2` (default) and echo the choice + resolved function-id. Run the inlined Step 3b recipe (`transcribe_manifest(...)`). Score the four metrics. Produce the five-section leaderboard. Read the by-`ipa_source` split to the user. Apply the decision tree against drug KER.

**Scenario B — interpreting a mixed result.** User: *"Eval shows KER 0.05 on rows tagged `merriam-webster` but 0.40 on rows tagged `magpie_g2p`. Should I fine-tune?"* → No — this is the special case. The model is fine; the pronunciation hints aren't covering the long-tail terms. Route the user back to `/digital-health-clinical-asr-build` Step 2d to audition the `magpie_g2p` rows and append verified IPA to `pronunciation_overrides.csv`. Re-run Stage 3 after the rebuild before reconsidering Stage 4.

## Out of scope

- fine-tuning
- setup
- manifest authoring
