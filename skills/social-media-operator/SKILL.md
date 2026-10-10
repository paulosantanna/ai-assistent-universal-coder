# Social Media Operator Skill

## Mission
Governed TikTok and Instagram operations via browser-based authentication sessions. Sessions persist for 30 days or until platform cookies expire, whichever comes first. No OAuth API keys required - uses manual browser login with cookie import.

## Capabilities
- SOCIAL_MEDIA_SESSION_CREATE
- SOCIAL_MEDIA_SESSION_VALIDATE
- SOCIAL_MEDIA_SESSION_LIST
- SOCIAL_MEDIA_SESSION_CLOSE
- TIKTOK_PROFILE_READ
- TIKTOK_VIDEOS_LIST
- INSTAGRAM_PROFILE_READ
- INSTAGRAM_MEDIA_LIST
- INSTAGRAM_INSIGHTS_READ
- SOCIAL_MEDIA_AUTH_GUIDE

## Required MCPs
- social-media
- browser (for visual verification)

## Risk Level
Medium - handles authentication cookies but never exposes them. All mutations require approval gates.

## Authentication Model
**Browser-based manual authentication:**
1. User opens browser to platform login URL
2. User logs in normally (2FA, password, etc.)
3. User exports cookies via browser extension or DevTools
4. Skill imports cookies to create encrypted session
5. Session valid for 30 days or until cookies expire

**No API keys, OAuth apps, or developer accounts needed.**

## Session Lifecycle
```
CREATE (import cookies) → VALIDATE (test request) → OPERATE (API calls) → CLOSE (cleanup)
     ↓                        ↓                        ↓
  30 days max           Auto-refresh           Auto-cleanup
  or cookie expiry      on use                 on expiry
```

## Security Rules
- Cookies stored encrypted (AES-256-GCM) in `.aeos/social-sessions/`
- Never logged, printed, or exposed to evidence/notebook
- Domain-scoped: TikTok cookies only work on *.tiktok.com
- HTTPS only for all API requests
- Automatic cleanup of expired sessions
- Redaction of all sensitive fields in outputs

## Quality Gates
- Session must validate before operations
- All mutations require `approved=true`, `change_id`, `rollback_ref`
- Visual verification via browser MCP for publishing operations
- Cookie expiry respected - session dies when platform logs out
- Max 30-day session lifetime regardless of cookie expiry

## Platform-Specific Operations

### TikTok
- Profile: username, follower count, bio, verification status
- Videos: list with pagination, view counts, engagement metrics
- Note: Limited official API - uses internal web endpoints

### Instagram
- Profile: username, bio, follower/following counts, business category
- Media: posts, reels, stories (if accessible), engagement metrics
- Insights: reach, impressions, engagement (business/creator accounts only)
- Note: Uses internal web endpoints, not Graph API

## Usage Patterns

### Initial Setup
```
1. social_media.auth.login_instructions(platform="tiktok")
2. User follows instructions, exports cookies
3. social_media.session.open_cookie_file(platform="tiktok", cookie_file_path="/path/to/cookies.json")
4. social_media.session.validate(session_ref="...")
5. Session ready for operations
```

### Ongoing Operations
```
- social_media.tiktok.profile(session_ref="...")
- social_media.tiktok.videos(session_ref="...", count=50)
- social_media.instagram.profile(session_ref="...", username="brand")
- social_media.instagram.media(session_ref="...", user_id="12345", count=20)
- social_media.instagram.insights(session_ref="...", media_id="abc")
```

### Maintenance
```
- social_media.session.list(platform="tiktok")  # Check expiry
- social_media.session.validate(session_ref="...")  # Pre-operation check
- social_media.session.close(session_ref="...")  # Manual cleanup
```

## Cookie Export Instructions

### Chrome/Edge (Recommended)
1. Install "Cookie Editor" or "EditThisCookie" extension
2. Log into TikTok/Instagram
3. Click extension → Export → JSON
4. Save file outside workspace (e.g., `~/Downloads/tiktok-cookies.json`)

### Firefox
1. Open DevTools (F12) → Storage → Cookies
2. Right-click → Copy All → Paste into JSON file
3. Or use "cookies.txt" extension for Netscape format

### DevTools (All Browsers)
1. F12 → Application/Storage → Cookies
2. Filter for platform domain
3. Copy as JSON array manually

## Error Handling
- `SESSION_EXPIRED` → Re-run login flow
- `COOKIE_EXPIRED` → Platform logged out, re-authenticate
- `INVALID_DOMAIN` → Cookie domain mismatch, check export
- `MISSING_COOKIES` → Required cookies not found in export
- `VALIDATION_FAILED` → Session invalid, re-authenticate

## Compliance
- Respects platform Terms of Service
- No scraping, automation, or bot behavior
- Manual human login required
- Rate limits respected via session caching
- No credential storage beyond session cookies