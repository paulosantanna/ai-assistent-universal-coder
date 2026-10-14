<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Prerequisites Check

When starting a deployment, verify these requirements in order:

**1. Confirm Source Path (Git vs Docker)**

If using Git-based methods (Blueprint or Direct Creation), the repo must be pushed to GitHub/GitLab/Bitbucket. Blueprints that reference a prebuilt image still require a Git repo with `render.yaml`.

```bash
git remote -v
```

- If no remote exists, stop and ask the user to create/push a remote **or** switch to Docker image deploy.

**2. Check MCP Tools Availability (Preferred for Single-Service)**

MCP tools provide the best experience. Check if available by attempting:

```
list_services()
```

If MCP tools are available, you can skip CLI installation for most operations.

**3. Check Render CLI Installation (for Blueprint validation)**

```bash
render --version
```

If not installed, offer to install:

- macOS: `brew install render`
- Linux/macOS: `curl -fsSL https://raw.githubusercontent.com/render-oss/cli/main/bin/install.sh | sh`

**4. MCP Setup (if MCP isn't configured)**

If `list_services()` fails because MCP isn't configured, ask whether they want to set up MCP (preferred) or continue with the CLI fallback. If they choose MCP, ask which AI tool they're using, then provide the matching instructions below. Always use their API key.

### Cursor

Walk the user through these steps:

1. Get a Render API key:

```
https://dashboard.render.com/u/*/settings#api-keys
```

2. Add this to `~/.cursor/mcp.json` (replace `<YOUR_API_KEY>`):

```json
{
  "mcpServers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

3. Restart Cursor, then retry `list_services()`.

### Claude Code

Walk the user through these steps:

1. Get a Render API key:

```
https://dashboard.render.com/u/*/settings#api-keys
```

2. Add the MCP server with Claude Code (replace `<YOUR_API_KEY>`):

```bash
claude mcp add --transport http render https://mcp.render.com/mcp --header "Authorization: Bearer <YOUR_API_KEY>"
```

3. Restart Claude Code, then retry `list_services()`.

### Other Tools

If the user is on another AI app, direct them to the Render MCP docs for that tool's setup steps and install method.

### Workspace Selection

After MCP is configured, have the user set the active Render workspace with a prompt like:

```
Set my Render workspace to [WORKSPACE_NAME]
```

**5. Check Authentication (CLI fallback only)**

If MCP isn't available, use the CLI instead and verify you can access your account:

```bash
# Check if user is logged in (use -o json for non-interactive mode)
render whoami -o json
```

If `render whoami` fails or returns empty data, the CLI is not authenticated. The CLI won't always prompt automatically, so explicitly prompt the user to authenticate:

If neither is configured, ask user which method they prefer:

- **API Key (CLI)**: `export RENDER_API_KEY="rnd_xxxxx"` (Get from https://dashboard.render.com/u/*/settings#api-keys)
- **Login**: `render login` (Opens browser for OAuth)

**6. Check Workspace Context**

Verify the active workspace:

```
get_selected_workspace()
```

Or via CLI:

```bash
render workspace current -o json
```

To list available workspaces:

```
list_workspaces()
```

If user needs to switch workspaces, they must do so via Dashboard or CLI (`render workspace set`).

Once prerequisites are met, proceed with deployment workflow.

---

# Method 1: Blueprint Deployment (Recommended for Complex Apps)
