<!-- Package: 00_skills/(cloud)/cloudflare-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Authentication (Required Before Deploy)

Verify auth before `wrangler deploy`, `wrangler pages deploy`, or `npm run deploy`:

```bash
npx wrangler whoami    # Shows account if authenticated
```

Not authenticated? → `references/wrangler/auth.md`

- Interactive/local: `wrangler login` (one-time OAuth)
- CI/CD: Set `CLOUDFLARE_API_TOKEN` env var
