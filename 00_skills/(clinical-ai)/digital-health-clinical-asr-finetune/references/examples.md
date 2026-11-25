# Examples

## Examples

**Scenario A — gate met.** User: *"Drug KER 0.42, 130 rows. SFT?"* → Yes (gate cleared). `parakeet-tdt-0.6b-v2` (verified 0.513 → 0.128). No local GPU? Step 4a (Brev) → 4b (split) → 4d (stock SFT) → 4e (offline re-eval). If cycle-2 drug KER drops ≥ 20% relative, keep the `.nemo`; otherwise back to `/digital-health-clinical-asr-build`.

**Scenario B — Nemotron Streaming.** User: *"SFT `nvidia/nemotron-speech-streaming-en-0.6b`?"* → No (UNK collapse). Substitute `parakeet-tdt-0.6b-v2`. Riva chunks non-streaming bases for streaming serving — base doesn't need to be streaming-native.

**Scenario C — cycle 2 KER unchanged.** User: *"KER barely moved."* → Back to `/digital-health-clinical-asr-build`. Signal density beats LR sweeps. If `magpie_g2p` rows are bad but `merriam-webster` rows are good, the gap is pronunciation-coverage — `/digital-health-clinical-asr-build` Step 2d.

## Out of scope

- setup
- first-pass scoring
- generic word boosting
