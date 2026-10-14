# Publishing Dispatch and Accounts

## Dispatch is the Only Publisher

- `publishing.dispatch` is the sole authorized publisher
- No second publisher or posting outside dispatch
- TikTok stays `SELF_ONLY` until app audit
- File deleted after a real post

## Platform Publishers

### TikTok (`publishers/tiktok.py`)

- `SELF_ONLY` mode until app audit completes
- Post through dispatch only
- No direct posting outside the dispatch flow

### Instagram (`publishers/instagram.py`)

- Browser-based posting automation (`browser_post.py`)
- Clicks "Novo post", waits for `input[type=file]`
- Clicks "Avançar" and "Compartilhar" only inside `div[role=dialog]`
- Dispatch coordinates the publishing flow

### YouTube (`publishers/youtube.py`)

- YouTube API publishing
- Managed through dispatch orchestrator

## Account Management

- Accounts configured per platform
- Instagram/TikTok accounts require browser authentication
- YouTube accounts use API keys
- Account state checked before publishing

## Post-Flight

- File deleted after a real post
- Dispatch tracks post status
- Failed posts do not retry outside dispatch

## Do Not Activate For

- A new poster without proper connector configuration
- A scraper that bypasses the YouTube Data API
- Any path that publishes a dry run
- Filling connector gaps with synthetic samples in real runs
- Creating a second publisher or posting outside dispatch