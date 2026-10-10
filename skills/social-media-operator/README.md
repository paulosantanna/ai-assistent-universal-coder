# Social Media Operator Skill

Governed TikTok and Instagram operations via browser-based authentication sessions.

## Quick Start

### 1. Get Login Instructions
```bash
# Via MCP
social_media.auth.login_instructions(platform="tiktok")
social_media.auth.login_instructions(platform="instagram")
```

### 2. Export Cookies from Browser
- Install "Cookie Editor" or "EditThisCookie" extension
- Log into platform normally
- Export cookies as JSON
- Save outside workspace (e.g., `~/Downloads/tiktok-cookies.json`)

### 3. Create Session
```bash
social_media.session.open_cookie_file(
  platform="tiktok",
  cookie_file_path="/home/user/Downloads/tiktok-cookies.json"
)
```

### 4. Validate & Use
```bash
social_media.session.validate(session_ref="sess_...")
social_media.tiktok.profile(session_ref="sess_...")
social_media.tiktok.videos(session_ref="sess_...", count=20)
```

## Session Management

### List Sessions
```bash
social_media.session.list(platform="tiktok")
```

### Check Session Info
```bash
social_media.session.info(platform="tiktok", session_ref="sess_...")
```

### Close Session
```bash
social_media.session.close(platform="tiktok", session_ref="sess_...")
```

## Platform Operations

### TikTok
| Operation | Description |
|-----------|-------------|
| `tiktok_profile` | Get authenticated user profile |
| `tiktok_videos` | List user videos with pagination |

### Instagram
| Operation | Description |
|-----------|-------------|
| `instagram_profile` | Get profile (self or by username) |
| `instagram_media` | List user media/posts |
| `instagram_insights` | Get media insights (business accounts) |

## Session Lifecycle

- **Max Lifetime**: 30 days
- **Actual Lifetime**: Min(30 days, cookie expiry)
- **Auto-refresh**: 15 min on active use
- **Auto-cleanup**: Expired sessions removed on access
- **Storage**: Encrypted (AES-256-GCM) in `.aeos/social-sessions/`

## Security

- ✅ Cookies never exposed in logs/outputs
- ✅ Encrypted at rest
- ✅ Domain-scoped (TikTok cookies only work on TikTok)
- ✅ HTTPS only
- ✅ Automatic redaction
- ✅ No OAuth tokens or API keys stored

## Cookie Export Formats Supported

1. **JSON Array** (Chrome extensions): `[{"name": "...", "value": "...", "domain": "...", ...}]`
2. **Netscape Format** (cookies.txt): `domain\tTRUE\t/\tFALSE\t0\tname\tvalue`
3. **Chrome DevTools Protocol**: `{"cookies": [...]}`

## Required Cookies

### TikTok
- `sessionid` - Session identifier
- `tt_webid` - User identifier
- `s_v_web_id` - Web session ID

### Instagram
- `sessionid` - Session identifier
- `csrftoken` - CSRF protection
- `ds_user_id` - User ID

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| `SESSION_EXPIRED` | Session TTL exceeded | Re-authenticate |
| `COOKIE_EXPIRED` | Platform cookie expired | Re-authenticate |
| `MISSING_COOKIES` | Required cookies not in export | Re-export with full cookies |
| `INVALID_DOMAIN` | Cookie domain mismatch | Check export domain |
| `VALIDATION_FAILED` | Test request failed | Re-authenticate |

## Integration with AEOS

```yaml
# In playbook or skill composition
required_mcps: [social-media, browser]
capabilities:
  - SOCIAL_MEDIA_SESSION_CREATE
  - TIKTOK_PROFILE_READ
  - INSTAGRAM_MEDIA_LIST
quality_gates:
  - Session validates before operations
  - Visual verification for publishing
  - Cookie expiry respected
```

## Troubleshooting

**"No valid cookies found"**
- Ensure you're logged in when exporting
- Check domain includes `.tiktok.com` or `.instagram.com`
- Try Netscape format if JSON fails

**"Session expired" after 1 day**
- Platform may have short cookie TTL
- Check "Remember me" on login
- Some platforms rotate cookies frequently

**"Domain not allowed"**
- Cookie export missed subdomain cookies
- Export from root domain (tiktok.com, not www.tiktok.com)
- Include all platform cookie domains