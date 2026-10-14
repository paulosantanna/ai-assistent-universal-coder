---
name: dark-videos-pipeline-expert
description: 'Operate the dark-videos pipeline: mine the last 24h, rank the top 20 with LAYA, frame from the project template, and publish through the existing dispatch. Use when mining, framing, scheduling, or posting shorts in dark-videos. Do not use for a second publisher, cookie export, or posting below the app''s red team.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# Dark Videos Pipeline Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission

Run the dark-videos one-click pipeline so a real execution mines, frames, and schedules posts. LAYA heat is a 0–10 reading. The top 20 stays ordered by velocity plus LAYA. A score under 9.5 still stays in that top. Performance: minimal API calls, cached reads, target_count=10 by default, dry_run simulation first. Support immediate and scheduled publishing across TikTok, Instagram Reels, and YouTube Shorts. Integrated LAYA learning loop feeds post-performance data back into future ranking predictions.

## Activate

Mining, framing, captions, tags, red team, prime-time schedule, or real posting in `dark-videos`.

## Do not activate

A new poster, a scraper that bypasses the YouTube Data API, Instagram hashtag search, or any path that publishes a dry run. Do not fill connector gaps with synthetic samples in real runs.

## Contract

1. Read connector and account state before starting a run. Check `MINING_YOUTUBE_API_KEY` and `MINING_PROVIDER_BASE_URL` environment variables.
2. A real run (`dry_run` false) with no connector fails as `connectors_unconfigured`. Do not fill that gap with the synthetic sample. Use `target_count=10` instead of default 20 for 50% fewer resources.
3. Simulation (`dry_run` true) may use the synthetic sample. Those URLs are `.invalid` and are not posted. Cache mining results for 10s to avoid redundant API calls.
4. Frame, description, and five tags per network come from the creative stages already in the repo. One frame per video; one description + max 5 tags per network. Do not add a second caption or frame path.
5. Publish only through `publishing.dispatch`. TikTok stays `SELF_ONLY` until the app audit. The file is deleted after a real post. Dispatch is the only publisher; MCP may only enqueue via `pipeline.start_run`.
6. Never print API keys, session cookies, or CSRF tokens. Cache time-to-live: status 5s, mining 10s, enqueue 3s.

## Stop

Stop when the YouTube key or an active Instagram/TikTok account is missing, when the red team blocks a piece, or when a step would post outside dispatch. Also stop when:
- Heat under 9.5 remains inside the top 20 (do not re-rank solely for badge)
- target_count exceeds available candidates (fail fast with `insufficient_candidates`)
- Pipeline stage gate gives "fail" verdict (early termination)
- Attempt to create a second publisher or post outside dispatch

## Token discipline

Read `references/INDEX.md`. Open only the mining, frame, heat, or publish note that the mission needs. Cache TTL: status 5s, mining 10s, enqueue 3s. Never expose credentials in logs or tool outputs.

### Environment Variables for Performance

| Variable | Purpose | Optimized Default |
|---|---|---|
| `MINING_YOUTUBE_API_KEY` | YouTube Data API key for mining | Required for real runs |
| `MINING_PROVIDER_BASE_URL` | Optional Instagram/TikTok provider base URL | Off by default (hashtag search stays off) |
| `DARKVIDEOS_DESKTOP=1` | Forces `dry_run=false` for real execution | Use for actual posts |
| `DARKVIDEOS_API_BASE` | Local API base URL | `http://127.0.0.1:8000` |

## Reference Files

- `references/mining.md` - Connectors, synthetic sample, lookback widening
- `references/frame.md` - Framing and copy generation (one frame per video, one description + max 5 tags)
- `references/heat.md` - Heat scoring and top 20 (sort: `0.65 * baseline velocity + 0.35 * LAYA signal`, heat >= 9.5 badge does not remove from top 20)
- `references/publish.md` - Publishing dispatch and accounts (dispatch is the only publisher)

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
