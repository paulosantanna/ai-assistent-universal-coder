# Mining Module Knowledge

## Connectors

Real connectors are configured via environment variables:

| Variable | Purpose |
|---|---|
| `MINING_YOUTUBE_API_KEY` | YouTube Data API key (required for real runs) |
| `MINING_PROVIDER_BASE_URL` | Optional Instagram/TikTok provider base URL |
| `MINING_PROVIDER_API_KEY` | Instagram/TikTok API key |

### YouTube Connector (`connectors/youtube.py`)

- Uses YouTube Data API for video search and metadata
- Supports search queries with configurable lookback period
- Falls back to yt-dlp when API key unavailable

### Instagram Connector (`connectors/instagram_hashtag.py`)

- Hashtag-based search (stays off by default)
- Requires `MINING_PROVIDER_BASE_URL` and `MINING_PROVIDER_API_KEY`

### TikTok Connector (`connectors/tiktok.py` - implied)

- Part of optional provider configuration

### yt-dlp Fallback (`connectors/ytdlp_feed.py`, `connectors/ytdlp_search.py`)

- Used when no API keys are configured
- Fixed queries for public Shorts search
- Lookback widening: 7 → 14 → 30 → 90 days until `target_count` filled

## Mining Stages

1. **AcquireStage** - Fetch videos from connectors
2. **DedupStage** - Remove duplicates using fingerprint comparison
3. **RankStage** - Rank by velocity + LAYA heat
4. **GateStage** - Stage gate validation

## Heat Scoring

Heat = `0.65 * baseline_velocity + 0.35 * LAYA_signal`

- Heat >= 9.5: Badge stays in top 20 (does not remove)
- Heat < 9.5: May be removed from top 20
- LAYA learning loop feeds post-performance data back into future ranking

## Synthetic Samples

- Used only in `dry_run` mode
- Titles/captions include their own ID to prevent rejection
- Limited to dry runs with no connector configured
- `.invalid` URLs, no real posts

## Failure Handling

- No connector + real run → `connectors_unconfigured` error (does not invent sample)
- Insufficient candidates → `insufficient_candidates` failure
- Repeated videos (same caption simhash) leave the ranking
- Real run that selects fewer than `target_count` fails in RankStage