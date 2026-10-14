<!-- Package: 00_skills/(tooling)/social-media-operator; relative command/resource examples resolve from that package or workspace root. -->

## Security Rules
- Cookies stored encrypted (AES-256-GCM) in `.aeos/social-sessions/`
- Never logged, printed, or exposed to evidence/notebook
- Domain-scoped: TikTok cookies only work on *.tiktok.com
- HTTPS only for all API requests
- Automatic cleanup of expired sessions
- Redaction of all sensitive fields in outputs
