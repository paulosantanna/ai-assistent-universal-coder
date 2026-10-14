<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Main Loop

### Step 1: Initialize Tracking

```
cycle_count = 0
start_time = now()
no_progress_count = 0
local_verify_count = 0
last_state = null
last_cipe_url = null
expected_commit_sha = null
```

### Step 2: Spawn Subagent

Spawn the `ci-watcher` subagent to poll CI status:

**Fresh start (first spawn, no expected CIPE):**

```
Task(
  agent: "ci-watcher",
  prompt: "Monitor CI for branch '<branch>'.
           Subagent timeout: <subagent-timeout> minutes.
           New-CIPE timeout: <new-cipe-timeout> minutes.
           Verbosity: <verbosity>."
)
```

**After action that triggers new CIPE (wait mode):**

```
Task(
  agent: "ci-watcher",
  prompt: "Monitor CI for branch '<branch>'.
           Subagent timeout: <subagent-timeout> minutes.
           New-CIPE timeout: <new-cipe-timeout> minutes.
           Verbosity: <verbosity>.

           WAIT MODE: A new CIPE should spawn. Ignore old CIPE until new one appears.
           Expected commit SHA: <expected_commit_sha>
           Previous CIPE URL: <last_cipe_url>"
)
```

### Step 3: Handle Subagent Response

When subagent returns:

1. Check the returned status
2. Look up default behavior in the table above
3. Check if user instructions override the default
4. Execute the appropriate action
5. **If action expects new CIPE**, update tracking (see Step 3a)
6. If action results in looping, go to Step 2

### Step 3a: Track State for New-CIPE Detection

After actions that should trigger a new CIPE, record state before looping:

| Action                        | What to Track                                 | Subagent Mode |
| ----------------------------- | --------------------------------------------- | ------------- |
| Fix auto-applying             | `last_cipe_url = current cipeUrl`             | Wait mode     |
| Apply via MCP                 | `last_cipe_url = current cipeUrl`             | Wait mode     |
| Apply locally + push          | `expected_commit_sha = $(git rev-parse HEAD)` | Wait mode     |
| Reject + fix + push           | `expected_commit_sha = $(git rev-parse HEAD)` | Wait mode     |
| Fix failed + local fix + push | `expected_commit_sha = $(git rev-parse HEAD)` | Wait mode     |
| No fix + local fix + push     | `expected_commit_sha = $(git rev-parse HEAD)` | Wait mode     |
| Environment rerun             | `last_cipe_url = current cipeUrl`             | Wait mode     |
| No-new-CIPE + auto-fix + push | `expected_commit_sha = $(git rev-parse HEAD)` | Wait mode     |

**CRITICAL**: When passing `expectedCommitSha` or `last_cipe_url` to the subagent, it enters **wait mode**:

- Subagent will **completely ignore** the old/stale CIPE
- Subagent will only wait for new CIPE to appear
- Subagent will NOT return to main agent with stale CIPE data
- Once new CIPE detected, subagent switches to normal polling

**Why wait mode matters for context preservation**: Stale CIPE data can be very large (task output summaries, suggested fix patches, reasoning). If subagent returns this to main agent, it pollutes main agent's context with useless data since we already processed that CIPE. Wait mode keeps stale data in the subagent, never sending it to main agent.

### Step 4: Progress Tracking

After each action:

- If state changed significantly → reset `no_progress_count = 0`
- If state unchanged → `no_progress_count++`
- On new CI attempt detected → reset `local_verify_count = 0`
