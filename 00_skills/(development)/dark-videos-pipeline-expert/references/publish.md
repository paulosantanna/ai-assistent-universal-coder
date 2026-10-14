# Publish

`default_params` stores `effective_dry_run`. The desktop (`DARKVIDEOS_DESKTOP=1` and fakes off) forces `dry_run` false. Outside the desktop, a saved simulation flag still simulates: dispatch writes `SIMULATED` and does not call the network.

## Scheduling System

The pipeline supports both immediate and scheduled publishing across all three platforms:

### Immediate Publishing
- Posts execute immediately after framing
- TikTok: posts via dispatch (remains `SELF_ONLY` until app audit completes)
- Instagram: opens browser window, user completes click flow ("Novo post" → select file → "Avançar" → "Compartilhar")
- YouTube Shorts: API upload with `status.publishAt: null` for immediate publish

### Scheduled Publishing
- Posts can be queued for future execution via `schedule` parameter
- Schedule format: ISO8601 timestamp `YYYY-MM-DDTHH:MM:SSZ` or cron expression
- Scheduled posts are persisted in the dispatch queue
- At scheduled time, dispatch executes the post according to platform rules

**Schedule Parameter Options:**
- `schedule`: ISO8601 timestamp (e.g., `2026-10-15T14:30:00Z`) for specific time
- `cron`: Cron expression (e.g., `0 9 * * *` for daily 9AM UTC) - via render-deploy integration
- `delay_minutes`: Number of minutes to delay after mining/framing

### Platform-Scheduled Publishing Details

**TikTok:**
- Scheduled posts queue in dispatch
- At execution time: posts via internal web endpoints
- Remains `SELF_ONLY` until app audit completes (even when scheduled)
- Use `DARKVIDEOS_DESKTOP=1` for real scheduled execution

**Instagram:**
- Scheduled posts queue in dispatch
- At execution time: opens browser window, user completes click flow
- **Cannot fully automate** - user interaction required per platform rules
- Alternative: Schedule via Meta Business Suite after pipeline generates media

**YouTube Shorts:**
- Scheduled posts: API upload with `status.publishAt` set to ISO8601 timestamp
- Video uploads as "private" until scheduled time
- Automatically becomes public at scheduled time
- Appears in YouTube Studio as "Scheduled"
- Supports recurring cron schedules

**Schedule Persistence:**
- Schedule rows persisted only for active connected accounts
- Platform with no account stays on last-run plan with "sem conta" badge
- Does not enter queue until account connected
- Accounts persist 30 days (IG/TikTok cookies) or until API key revoked (YouTube)

## Posting Execution

Dispatch is the only publisher. It composes the framed file, then posts according to platform rules, then deletes the local media.

**Posting Workflow:**
1. Dispatch composes final file from framed video + description + tags
2. Platform-specific posting executes:
   - TikTok: internal web endpoint post
   - Instagram: browser window with user click flow
   - YouTube Shorts: Data API upload
3. `publications.last_error` captures any post errors for Agenda translation
4. Local media deleted after successful post

**Media Management:**
- Classified file lives in `~/.local/share/dark-videos/media` (default `PUBLISHING_MEDIA_TMP_DIR`)
- ffmpeg must be on PATH or under WinGet Gyan.FFmpeg package
- Missing binary reported as `compose_unavailable`
- Dispatch copies file before posting; deletes after post completes

**Do not post from the MCP.** `pipeline.start_run` only asks the local API to enqueue the same pipeline.

## Error Handling

- `publications.last_error`: Error code translated by Agenda for review
- Platform-specific failures don't block entire pipeline (per-video error handling)
- Failed posts still have local media deleted to prevent accumulation
- Retry logic: enqueue failed posts on next run if within retry window
