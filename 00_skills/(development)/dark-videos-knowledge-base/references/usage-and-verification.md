# Example Usage and Failure Handling

## When Selecting This Skill

Read `references/INDEX.md` first. Open only the mining, frame, heat, or publish note that the mission needs.

## Environment Variables for Performance

| Variable | Purpose | Optimized Default |
|---|---|---|
| `MINING_YOUTUBE_API_KEY` | YouTube Data API key for mining | Required for real runs |
| `MINING_PROVIDER_BASE_URL` | Optional Instagram/TikTok provider base URL | Off by default (hashtag search stays off) |
| `DARKVIDEOS_DESKTOP=1` | Forces `dry_run=false` for real execution | Use for actual posts |
| `DARKVIDEOS_API_BASE` | Local API base URL | `http://127.0.0.1:8000` |

## Contract Requirements

1. **Read connector and account state before starting a run.** Check `MINING_YOUTUBE_API_KEY` and `MINING_PROVIDER_BASE_URL` environment variables.

2. **Real run (`dry_run=false`) with no connector fails as `connectors_unconfigured`.** Do not fill that gap with the synthetic sample. Use `target_count=10` instead of default 20 for 50% fewer resources.

3. **Simulation (`dry_run=true`) may use the synthetic sample.** Those URLs are `.invalid` and are not posted. Cache mining results for 10s to avoid redundant API calls.

4. **Frame, description, and five tags per network come from the creative stages already in the repo.** One frame per video; one description + max 5 tags per network. Do not add a second caption or frame path.

5. **Publish only through `publishing.dispatch`.** TikTok stays `SELF_ONLY` until the app audit. The file is deleted after a real post. Dispatch is the only publisher; MCP may only enqueue via `pipeline.start_run`.

6. **Never print API keys, session cookies, or CSRF tokens.** Cache time-to-live: status 5s, mining 10s, enqueue 3s.

## Stop Conditions

Stop when any of these occur:

- YouTube key or active Instagram/TikTok account is missing
- Red team blocks a piece
- Step would post outside dispatch
- Heat under 9.5 remains inside the top 20 (do not re-rank solely for badge)
- `target_count` exceeds available candidates (fail fast with `insufficient_candidates`)
- Pipeline stage gate gives "fail" verdict (early termination)
- Attempt to create a second publisher or post outside dispatch

## Token Discipline

- Read `references/INDEX.md`. Open only the mining, frame, heat, or publish note that the mission needs.
- Cache TTL: status 5s, mining 10s, enqueue 3s.
- Never expose credentials in logs or tool outputs.

## Reference Files to Read

- `references/mining.md` - Connectors, synthetic sample, lookback widening
- `references/frame.md` - Framing and copy generation
- `references/heat.md` - Heat scoring and top 20
- `references/publish.md` - Publishing dispatch and accounts
- `references/provenance.md` - Provenance and source freshness