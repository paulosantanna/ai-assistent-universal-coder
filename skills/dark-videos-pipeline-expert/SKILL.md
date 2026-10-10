---
name: dark-videos-pipeline-expert
description: "Operate the dark-videos pipeline: mine the last 24h, rank the top 20 with JEV, frame from the project template, and publish through the existing dispatch. Use when mining, framing, scheduling, or posting shorts in dark-videos. Do not use for a second publisher, cookie export, or posting below the app's red team."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# Dark Videos Pipeline Expert

Governance: CodENavi Full Workspace v2

## Mission

Run the dark-videos one-click pipeline so a real execution mines, frames, and schedules posts. JEV heat is a 0–10 reading. The top 20 stays ordered by velocity plus JEV. A score under 9.5 still stays in that top.

## Activate

Mining, framing, captions, tags, red team, prime-time schedule, or real posting in `dark-videos`.

## Do not activate

A new poster, a scraper that bypasses the YouTube Data API, Instagram hashtag search, or any path that publishes a dry run.

## Contract

1. Read connector and account state before starting a run.
2. A real run (`dry_run` false) with no connector fails as `connectors_unconfigured`. Do not fill that gap with the synthetic sample.
3. Simulation may use the synthetic sample. Those URLs are `.invalid` and are not posted.
4. Frame, description, and five tags per network come from the creative stages already in the repo.
5. Publish only through `publishing.dispatch`. TikTok stays `SELF_ONLY` until the app audit. The file is deleted after a real post.
6. Never print API keys, session cookies, or CSRF tokens.

## Stop

Stop when the YouTube key or an active Instagram/TikTok account is missing, when the red team blocks a piece, or when a step would post outside dispatch.

## Token discipline

Read `references/INDEX.md`. Open only the mining, frame, heat, or publish note that the mission needs.
