<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Direct Creation Workflow

Use the concise steps below, and refer to [references/direct-creation.md](../tlc/references/direct-creation.md) for full MCP command examples and follow-on configuration.

### Step 1: Analyze Codebase

Use [references/codebase-analysis.md](../tlc/references/codebase-analysis.md) to determine runtime, build/start commands, env vars, and datastores.

### Step 2: Create Resources via MCP

Create the service (web or static) and any required databases or key-value stores. See [references/direct-creation.md](../tlc/references/direct-creation.md).

If MCP returns an error about missing Git credentials or repo access, stop and guide the user to connect their Git provider in the Render Dashboard, then retry.

### Step 3: Configure Environment Variables

Add required env vars via MCP after creation. See [references/direct-creation.md](../tlc/references/direct-creation.md).

Remind the user that secrets can be set in the Dashboard if they prefer not to pass them via MCP.

### Step 4: Verify Deployment

Check deploy status, logs, and metrics. See [references/direct-creation.md](../tlc/references/direct-creation.md).

---

For service discovery, configuration details, quick commands, and common issues, see [references/deployment-details.md](../tlc/references/deployment-details.md).

---

# Post-deploy verification and basic triage (All Methods)

Keep this short and repeatable. If any check fails, fix it before redeploying.

1. Confirm the latest deploy is `live` and serving traffic
2. Hit the health endpoint (or root) and verify a 200 response
3. Scan recent error logs for a clear failure signature
4. Verify required env vars and port binding (`0.0.0.0:$PORT`)

Detailed checklist and commands: [references/post-deploy-checks.md](../tlc/references/post-deploy-checks.md)

If the service fails to start or health checks time out, use the basic triage guide:
[references/troubleshooting-basics.md](../tlc/references/troubleshooting-basics.md)
