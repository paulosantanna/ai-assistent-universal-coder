<!-- Package: 00_skills/(tooling)/social-media-operator; relative command/resource examples resolve from that package or workspace root. -->

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
