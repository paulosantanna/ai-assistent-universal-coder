<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Choose Your Deployment Method (Git Repo)

Both methods require a Git repository pushed to GitHub, GitLab, or Bitbucket. (If using `runtime: image`, the repo can be minimal and only contain `render.yaml`.)

| Method              | Best For                           | Pros                                                      |
| ------------------- | ---------------------------------- | --------------------------------------------------------- |
| **Blueprint**       | Multi-service apps, IaC workflows  | Version controlled, reproducible, supports complex setups |
| **Direct Creation** | Single services, quick deployments | Instant creation, no render.yaml file needed              |

### Method Selection Heuristic

Use this decision rule by default unless the user requests a specific method. Analyze the codebase first; only ask if deployment intent is unclear (e.g., DB, workers, cron).

**Use Direct Creation (MCP) when ALL are true:**

- Single service (one web app or one static site)
- No separate worker/cron services
- No attached databases or Key Value
- Simple env vars only (no shared env groups)
  If this path fits and MCP isn't configured yet, stop and guide MCP setup before proceeding.

**Use Blueprint when ANY are true:**

- Multiple services (web + worker, API + frontend, etc.)
- Databases, Redis/Key Value, or other datastores are required
- Cron jobs, background workers, or private services
- You want reproducible IaC or a render.yaml committed to the repo
- Monorepo or multi-env setup that needs consistent configuration

If unsure, ask a quick clarifying question, but default to Blueprint for safety. For a single service, strongly prefer Direct Creation via MCP and guide MCP setup if needed.
