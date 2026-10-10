# Social Media Integration - Implementation Summary

## Overview
Implemented browser-based authentication for TikTok and Instagram that replaces OAuth API with manual browser login + cookie import. Sessions persist for 30 days or until platform cookies expire.

## Files Created

### MCP Core
```
social-media-mcp/
├── index.mjs                    # Main MCP entry point (stdio transport)
├── session-manager.mjs          # Session lifecycle, encryption, cookie handling
├── export-helper.js             # Cookie validation utility
├── package.json                 # Dependencies and scripts
├── vitest.config.ts             # Test configuration
├── session-manager.test.mjs     # Unit tests (18 passing)
└── README.md                    # Complete documentation
```

### MCP Configuration
```
aeos/mcps/social-media.mcp.yaml  # MCP definition with tools, security, contracts
```

### Skill
```
skills/social-media-operator/
├── SKILL.md                     # Skill definition
├── README.md                    # Usage documentation
```

### Skill Registry
```
aeos/registries/skills.social-media-operator.additions.yaml
```

## Key Features

### 1. Browser-Based Authentication (No OAuth)
- User opens browser → logs in normally (including 2FA)
- Exports cookies via extension (Cookie Editor, EditThisCookie) or DevTools
- Imports cookies to create encrypted session
- **No API keys, no developer accounts, no OAuth apps needed**

### 2. Encrypted Session Storage
- AES-256-GCM encryption with runtime-generated key
- Stored in `.aeos/social-sessions/` (outside git tracking)
- Automatic cleanup of expired sessions
- Max 30-day lifetime OR platform cookie expiry (whichever comes first)

### 3. Domain-Scoped Security
- TikTok cookies only work on `*.tiktok.com`
- Instagram cookies only work on `*.instagram.com`, `*.facebook.com`
- HTTPS only for all API requests
- Full redaction of sensitive fields in all outputs

### 4. Platform Operations

#### TikTok
- `tiktok.profile` - Get authenticated user profile
- `tiktok.videos` - List user videos with pagination

#### Instagram
- `instagram.profile` - Get profile (self or by username)
- `instagram.media` - List user media/posts
- `instagram.insights` - Get media insights (business/creator accounts)

### 5. Session Management
| Action | Description |
|--------|-------------|
| `open_cookie_file` | Import cookies, create session |
| `session_info` | Get session info (no cookies exposed) |
| `session_list` | List all sessions for platform |
| `session_close` | Delete session |
| `session_validate` | Test session with API call |

## Usage Flow

```bash
# 1. Get login instructions
social_media.auth.login_instructions(platform="tiktok")

# 2. User exports cookies from browser (extension/DevTools)
#    Saves to ~/Downloads/tiktok-cookies.json

# 3. Create session
social_media.session.open_cookie_file(
  platform="tiktok",
  cookie_file_path="~/Downloads/tiktok-cookies.json"
)
# Returns: session_ref, expires_at, days_valid

# 4. Validate & use
social_media.session.validate(session_ref="sess_...")
social_media.tiktok.profile(session_ref="sess_...")
social_media.tiktok.videos(session_ref="sess_...", count=20)

# 5. Later: list/close sessions
social_media.session.list(platform="tiktok")
social_media.session.close(session_ref="sess_...")
```

## Cookie Requirements

### TikTok (required in export)
- `sessionid` - Session identifier
- `tt_webid` - User identifier
- `s_v_web_id` - Web session ID

### Instagram (required in export)
- `sessionid` - Session identifier
- `csrftoken` - CSRF protection
- `ds_user_id` - User ID

## Supported Cookie Formats
1. **JSON Array** (Chrome extensions): `[{"name": "...", "value": "...", "domain": "...", ...}]`
2. **Netscape Format** (cookies.txt): `domain\tTRUE\t/\tFALSE\t0\tname\tvalue`
3. **Chrome DevTools Protocol**: `{"cookies": [...]}`

## Cookie Export Helper
Validate before importing:
```bash
node export-helper.js tiktok ~/Downloads/tiktok-cookies.json
node export-helper.js instagram ~/Downloads/ig-cookies.txt
```

Shows:
- Platform detected
- Cookie count & required cookies present/missing
- Expiry information
- Ready-to-use confirmation

## Integration with AEOS

### 1. Register MCP
Already created: `aeos/mcps/social-media.mcp.yaml`

### 2. Register Skill
Already created: `aeos/registries/skills.social-media-operator.additions.yaml`

### 3. Use in Playbook/Skill Composition
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
  - Max 30-day session lifetime
```

## Security Model
- ✅ Cookies never exposed in logs/outputs/evidence/notebook
- ✅ Encrypted at rest (AES-256-GCM)
- ✅ Domain-scoped (cookies only sent to matching domains)
- ✅ HTTPS only
- ✅ Automatic redaction of all sensitive fields
- ✅ No credential persistence beyond session cookies
- ✅ Sessions auto-expire at 30 days or cookie expiry

## Testing
```bash
cd social-media-mcp
npm test
# 18 tests passing
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "No valid cookies found" | Ensure logged in when exporting; check domain |
| "Session expired" quickly | Enable "Remember me"; some platforms rotate cookies |
| "Domain not allowed" | Export from root domain; include all subdomains |
| "Missing required cookies" | Export ALL cookies; disable extension filters |

## Architecture Decisions

1. **No OAuth** - Uses browser cookies like a real user
2. **Encrypted local storage** - Not in database, not in cloud
3. **30-day max** - Balances convenience with security
4. **Platform cookie expiry respected** - Session dies when platform logs out
5. **Manual login required** - Prevents automation/bot detection
6. **Redaction by default** - Defense in depth for sensitive data