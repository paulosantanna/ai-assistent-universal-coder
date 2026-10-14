<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Security Requirements for API Keys and Secrets

**CRITICAL - You must protect user credentials:**

When handling Render API keys or any secrets:

1. **NEVER ask users to paste API keys directly in chat** - Instead, instruct them to set environment variables:

   ```bash
   export RENDER_API_KEY="rnd_xxxxx"
   ```

2. **NEVER include actual API keys in examples** - Always use placeholders like `<YOUR_API_KEY>` or `rnd_xxxxx`

3. **Guide users to secure storage** - Direct them to:
   - Set environment variables for CLI authentication
   - Use Render Dashboard for service secrets (env vars marked `sync: false`)
   - Never commit secrets to Git

4. **When users need an API key**, provide this guidance:
   - "Get your API key from: https://dashboard.render.com/u/*/settings#api-keys"
   - "Set it as an environment variable: `export RENDER_API_KEY='your-key-here'`"
   - "Never share or commit this key"

5. **For MCP configuration**, show the structure but emphasize:
   - Replace `<YOUR_API_KEY>` with their actual key
   - This file should not be committed to version control
   - The key should be kept private

6. **If a user accidentally shares a secret in chat**, immediately:
   - Warn them the key may be compromised
   - Instruct them to revoke it in Render Dashboard
   - Guide them to create a new key
