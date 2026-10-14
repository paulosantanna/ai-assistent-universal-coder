<!-- Package: 00_skills/(cloud)/netlify-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Authentication Pattern

The skill uses the **pre-authenticated Netlify CLI** approach:

1. Check authentication status with `npx netlify status`
2. If not authenticated, guide user through `npx netlify login`
3. Fail gracefully if authentication cannot be established

Authentication uses either:

- **Browser-based OAuth** (primary): `netlify login` opens browser for authentication
- **API Key** (alternative): Set `NETLIFY_AUTH_TOKEN` environment variable
