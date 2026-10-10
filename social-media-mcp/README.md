# Social Media MCP - TikTok & Instagram

Browser-based authentication for TikTok and Instagram. No OAuth apps, no API keys - just manual browser login with cookie import.

## Features

- 🔐 **Browser-based auth**: User logs in manually, exports cookies
- 📦 **Encrypted sessions**: AES-256-GCM encrypted storage in `.aeos/social-sessions/`
- ⏱️ **30-day max lifetime**: Sessions expire at 30 days or when platform cookies expire
- 🔒 **Domain-scoped**: TikTok cookies only work on `*.tiktok.com`
- 🌐 **HTTPS only**: All API requests over TLS
- 🧹 **Auto-cleanup**: Expired sessions removed automatically
- 📝 **Full redaction**: Cookies never appear in logs/outputs

## Installation

```bash
cd social-media-mcp
npm install
```

## Quick Start

### 1. Get Login Instructions

```bash
# Via MCP (stdio)
echo '{"action": "social_media.auth.login_instructions", "params": {"platform": "tiktok"}}' | node index.mjs
```

### 2. Export Cookies from Browser

**Easiest: Browser Extension**
1. Install "Cookie Editor" (Chrome/Edge) or "Cookie Quick Manager" (Firefox)
2. Go to `https://www.tiktok.com` or `https://www.instagram.com`
3. Log in normally (including 2FA)
4. Click extension → Export → Save as JSON
5. Save outside workspace (e.g., `~/Downloads/tiktok-cookies.json`)

**Alternative: DevTools**
1. F12 → Application/Storage → Cookies
2. Select platform domain
3. Copy cookies as JSON array

### 3. Create Session

```bash
echo '{
  "action": "social_media.session.open_cookie_file",
  "params": {
    "platform": "tiktok",
    "cookie_file_path": "/home/user/Downloads/tiktok-cookies.json"
  }
}' | node index.mjs
```

Response:
```json
{
  "success": true,
  "data": {
    "status": "SESSION_CREATED",
    "platform": "tiktok",
    "session_ref": "sess_abc123...",
    "cookie_count": 5,
    "expires_at": "2026-11-08T10:30:00.000Z",
    "days_valid": 30
  }
}
```

### 4. Use Session

```bash
# Get TikTok profile
echo '{"action": "social_media.tiktok.profile", "params": {"session_ref": "sess_abc123..."}}' | node index.mjs

# Get TikTok videos
echo '{"action": "social_media.tiktok.videos", "params": {"session_ref": "sess_abc123...", "count": 20}}' | node index.mjs

# Get Instagram profile
echo '{"action": "social_media.instagram.profile", "params": {"session_ref": "sess_xyz789...", "username": "brandname"}}' | node index.mjs

# Get Instagram media
echo '{"action": "social_media.instagram.media", "params": {"session_ref": "sess_xyz789...", "user_id": "123456789"}}' | node index.mjs
```

## MCP Actions

### Session Management

| Action | Description | Auth Required |
|--------|-------------|---------------|
| `social_media.session.open_cookie_file` | Import cookies, create session | ✅ |
| `social_media.session.info` | Get session info (no cookies) | ❌ |
| `social_media.session.list` | List all sessions for platform | ❌ |
| `social_media.session.close` | Delete session | ✅ |
| `social_media.session.validate` | Test session with API call | ❌ |

### Platform Operations

| Action | Platform | Description |
|--------|----------|-------------|
| `social_media.tiktok.profile` | TikTok | Get authenticated user profile |
| `social_media.tiktok.videos` | TikTok | List user videos (paginated) |
| `social_media.instagram.profile` | Instagram | Get profile (self or by username) |
| `social_media.instagram.media` | Instagram | List user media/posts |
| `social_media.instagram.insights` | Instagram | Get media insights (business accounts) |

### Utility

| Action | Description |
|--------|-------------|
| `social_media.platforms.list` | List supported platforms |
| `social_media.auth.login_instructions` | Get browser login instructions |
| `social_media.api.fetch` | Generic authenticated API call |
| `social_media.health` | Health check |

## Cookie Requirements

### TikTok
Required cookies (must be present in export):
- `sessionid` - Session identifier
- `tt_webid` - User identifier  
- `s_v_web_id` - Web session ID

Cookie domains accepted:
- `.tiktok.com`
- `tiktok.com`

### Instagram
Required cookies:
- `sessionid` - Session identifier
- `csrftoken` - CSRF protection
- `ds_user_id` - User ID

Cookie domains accepted:
- `.instagram.com`
- `instagram.com`
- `.facebook.com`
- `facebook.com`

## Supported Cookie Formats

1. **JSON Array** (Chrome extensions)
   ```json
   [{"name": "sessionid", "value": "abc", "domain": ".tiktok.com", "path": "/", "secure": true}]
   ```

2. **Netscape Format** (cookies.txt)
   ```
   .tiktok.com	TRUE	/	TRUE	1735689600	sessionid	abc123
   ```

3. **Chrome DevTools Protocol**
   ```json
   {"cookies": [{"name": "sessionid", "value": "abc", "domain": ".tiktok.com", ...}]}
   ```

## Session Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CREATE    │────▶│  VALIDATE   │────▶│   OPERATE   │────▶│    CLOSE    │
│ (import)    │     │ (test req)  │     │ (API calls) │     │ (cleanup)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
  30 days max         Auto-refresh         Cache GET          Auto-cleanup
  or cookie expiry    on active use        30 sec             on expiry
```

## Security

- **Encryption**: AES-256-GCM with runtime-generated key
- **Storage**: `.aeos/social-sessions/` (outside git tracking)
- **Redaction**: All sensitive fields redacted in outputs
- **Domain validation**: Cookies only sent to matching platform domains
- **No persistence**: Cookies never written to logs, evidence, notebook

## Cookie Export Helper

Validate your cookie file before importing:

```bash
node export-helper.js tiktok ~/Downloads/tiktok-cookies.json
node export-helper.js instagram ~/Downloads/ig-cookies.txt
```

Output shows:
- Platform detected
- Cookie count & required cookies present/missing
- Expiry information
- Ready-to-use confirmation

## Integration with AEOS

### Register MCP
Add to your AEOS configuration:
```yaml
# aeos/mcps/social-media.mcp.yaml (already created)
```

### Register Skill
```yaml
# aeos/registries/skills.social-media-operator.additions.yaml (already created)
```

### Use in Playbook
```yaml
required_mcps: [social-media, browser]
capabilities:
  - SOCIAL_MEDIA_SESSION_CREATE
  - TIKTOK_PROFILE_READ
  - INSTAGRAM_MEDIA_LIST
quality_gates:
  - Session validates before operations
  - Visual verification for publishing via browser MCP
  - Cookie expiry respected
```

## Troubleshooting

### "No valid cookies found"
- Ensure logged in when exporting
- Check domain includes platform domains
- Try different export method

### "Session expired" quickly
- Platform may have short cookie TTL
- Enable "Remember me" on login
- Some platforms rotate cookies frequently

### "Domain not allowed"
- Export missed subdomain cookies
- Export from root domain (tiktok.com, not www.tiktok.com)
- Include all platform cookie domains

### "Missing required cookies"
- Export ALL cookies for domain, not just a few
- Some extensions filter by default - disable filters
- DevTools copy sometimes misses HttpOnly cookies

## Architecture

```
social-media-mcp/
├── index.mjs              # Main MCP entry point
├── session-manager.mjs    # Session lifecycle, encryption, cookie handling
├── export-helper.js       # Cookie validation utility
├── package.json           # Dependencies
├── session-manager.test.mjs  # Unit tests
└── README.md              # This file
```

## Testing

```bash
npm test
```

## License

MIT - Part of AEOS Project