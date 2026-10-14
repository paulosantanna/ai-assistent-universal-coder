<!-- Package: 00_skills/(tooling)/social-media-operator; relative command/resource examples resolve from that package or workspace root. -->

## Authentication Model
**Browser-based manual authentication:**
1. User opens browser to platform login URL
2. User logs in normally (2FA, password, etc.)
3. User exports cookies via browser extension or DevTools
4. Skill imports cookies to create encrypted session
5. Session valid for 30 days or until cookies expire

**No API keys, OAuth apps, or developer accounts needed.**
