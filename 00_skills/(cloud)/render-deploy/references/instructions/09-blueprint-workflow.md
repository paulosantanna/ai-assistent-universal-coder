<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Blueprint Workflow

### Step 1: Analyze Codebase

Analyze the codebase to determine framework/runtime, build and start commands, required env vars, datastores, and port binding. Use the detailed checklists in [references/codebase-analysis.md](../tlc/references/codebase-analysis.md).

### Step 2: Generate render.yaml

Create a `render.yaml` Blueprint file following the Blueprint specification.

Complete specification: [references/blueprint-spec.md](../tlc/references/blueprint-spec.md)

**Key Points:**

- Always use `plan: free` unless user specifies otherwise
- Include ALL environment variables the app needs
- Mark secrets with `sync: false` (user fills these in Dashboard)
- Use appropriate service type: `web`, `worker`, `cron`, `static`, or `pserv`
- Use appropriate runtime: [references/runtimes.md](../tlc/references/runtimes.md)

**Basic Structure:**

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: JWT_SECRET
        sync: false # User fills in Dashboard

databases:
  - name: postgres
    databaseName: myapp_db
    plan: free
```

**Service Types:**

- `web`: HTTP services, APIs, web applications (publicly accessible)
- `worker`: Background job processors (not publicly accessible)
- `cron`: Scheduled tasks that run on a cron schedule
- `static`: Static sites (HTML/CSS/JS served via CDN)
- `pserv`: Private services (internal only, within same account)

Service type details: [references/service-types.md](../tlc/references/service-types.md)
Runtime options: [references/runtimes.md](../tlc/references/runtimes.md)
Template example: use the Basic Structure shown above. The pinned upstream package supplies no assets directory; obtain any additional required template before relying on it.

### Step 2.5: Immediate Next Steps (Always Provide)

After creating `render.yaml`, always give the user a short, explicit checklist and run validation immediately when the CLI is available:

1. **Authenticate (CLI)**: run `render whoami -o json` (if not logged in, run `render login` or set `RENDER_API_KEY`)
2. **Validate (recommended)**: run `render blueprints validate`
   - If the CLI isn't installed, offer to install it and provide the command.
3. **Commit + push**: `git add render.yaml && git commit -m "Add Render deployment configuration" && git push origin main`
4. **Open Dashboard**: Use the Blueprint deeplink and complete Git OAuth if prompted
5. **Fill secrets**: Set env vars marked `sync: false`
6. **Deploy**: Click "Apply" and monitor the deploy

### Step 3: Validate Configuration

Validate the render.yaml file to catch errors before deployment. If the CLI is installed, run the commands directly; only prompt the user if the CLI is missing:

```bash
render whoami -o json  # Ensure CLI is authenticated (won't always prompt)
render blueprints validate
```

Fix any validation errors before proceeding. Common issues:

- Missing required fields (`name`, `type`, `runtime`)
- Invalid runtime values
- Incorrect YAML syntax
- Invalid environment variable references

Configuration guide: [references/configuration-guide.md](../tlc/references/configuration-guide.md)

### Step 4: Commit and Push

**IMPORTANT:** You must merge the `render.yaml` file into your repository before deploying.

Ensure the `render.yaml` file is committed and pushed to your Git remote:

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

If there is no Git remote yet, stop here and guide the user to create a GitHub/GitLab/Bitbucket repo, add it as `origin`, and push before continuing.

**Why this matters:** The Dashboard deeplink will read the render.yaml from your repository. If the file isn't merged and pushed, Render won't find the configuration and deployment will fail.

Verify the file is in your remote repository before proceeding to the next step.

### Step 5: Generate Deeplink

Get the Git repository URL:

```bash
git remote get-url origin
```

This will return a URL from your Git provider. **If the URL is SSH format, convert it to HTTPS:**

| SSH Format                        | HTTPS Format                      |
| --------------------------------- | --------------------------------- |
| `git@github.com:user/repo.git`    | `https://github.com/user/repo`    |
| `git@gitlab.com:user/repo.git`    | `https://gitlab.com/user/repo`    |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**Conversion pattern:** Replace `git@<host>:` with `https://<host>/` and remove `.git` suffix.

Format the Dashboard deeplink using the HTTPS repository URL:

```
https://dashboard.render.com/blueprint/new?repo=<REPOSITORY_URL>
```

Example:

```
https://dashboard.render.com/blueprint/new?repo=https://github.com/username/repo-name
```

### Step 6: Guide User

**CRITICAL:** Ensure the user has merged and pushed the render.yaml file to their repository before clicking the deeplink. If the file isn't in the repository, Render cannot read the Blueprint configuration and deployment will fail.

Provide the deeplink to the user with these instructions:

1. **Verify render.yaml is merged** - Confirm the file exists in your repository on GitHub/GitLab/Bitbucket
2. Click the deeplink to open Render Dashboard
3. Complete Git provider OAuth if prompted
4. Name the Blueprint (or use default from render.yaml)
5. Fill in secret environment variables (marked with `sync: false`)
6. Review services and databases configuration
7. Click "Apply" to deploy

The deployment will begin automatically. Users can monitor progress in the Render Dashboard.

### Step 7: Verify Deployment

After the user deploys via Dashboard, verify everything is working.

**Check deployment status via MCP:**

```
list_deploys(serviceId: "<service-id>", limit: 1)
```

Look for `status: "live"` to confirm successful deployment.

**Check for runtime errors (wait 2-3 minutes after deploy):**

```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 20)
```

**Check service health metrics:**

```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

If errors are found, proceed to the **Post-deploy verification and basic triage** section below.

---

# Method 2: Direct Service Creation (Quick Single-Service Deployments)

For simple deployments without Infrastructure-as-Code, create services directly via MCP tools.
