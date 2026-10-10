# Mining

Real connectors are YouTube Data API (`MINING_YOUTUBE_API_KEY`) and the optional provider (`MINING_PROVIDER_BASE_URL` plus `MINING_PROVIDER_API_KEY`) for Instagram and TikTok. Instagram hashtag search stays off.

`MineStage` uses those connectors when they are configured. If none are configured and the run is real (`dry_run` false), it raises `connectors_unconfigured` and does not invent a sample. Simulation (`dry_run` true) may use the synthetic sample. Each synthetic title and caption includes its own id so a later sample is not rejected as the same text.

The mining page says "Nenhum vídeo novo" when a run exists and every candidate was a repeat. "Nenhuma mineração ainda" means there is no run state yet.

Without a Data API key, public Shorts search uses several fixed queries and widens the lookback from 7 days to 14, 30, and 90 until the pool can fill `target_count` plus the reserve. A real run that still selects fewer than `target_count` fails in `RankStage` and does not edit or schedule that short list. Repeats of a used video, including the same caption simhash, leave the ranking and the next candidate takes the slot. The synthetic sample stays limited to a dry run with no connector.
