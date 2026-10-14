<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Default Behaviors by Status

The subagent returns with one of the following statuses. This table defines the **default behavior** for each status. User instructions can override any of these.

| Status              | Default Behavior                                                                                                                                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ci_success`        | Exit with success. Log "CI passed successfully!"                                                                                                                  |
| `fix_auto_applying` | Fix will be auto-applied by self-healing. Do NOT call MCP. Record `last_cipe_url`, spawn new subagent in wait mode to poll for new CIPE.                          |
| `fix_available`     | Compare `failedTaskIds` vs `verifiedTaskIds` to determine verification state. See **Fix Available Decision Logic** section below.                                 |
| `fix_failed`        | Self-healing failed to generate fix. Attempt local fix based on `taskOutputSummary`. If successful → commit, push, loop. If not → exit with failure.              |
| `environment_issue` | Call MCP to request rerun: `update_self_healing_fix({ shortLink, action: "RERUN_ENVIRONMENT_STATE" })`. New CIPE spawns automatically. Loop to poll for new CIPE. |
| `no_fix`            | CI failed, no fix available (self-healing disabled or not executable). Attempt local fix if possible. Otherwise exit with failure.                                |
| `no_new_cipe`       | Expected CIPE never spawned (CI workflow likely failed before Nx tasks). Report to user, attempt common fixes if configured, or exit with guidance.               |
| `polling_timeout`   | Subagent polling timeout reached. Exit with timeout.                                                                                                              |
| `cipe_canceled`     | CIPE was canceled. Exit with canceled status.                                                                                                                     |
| `cipe_timed_out`    | CIPE timed out. Exit with timeout status.                                                                                                                         |
| `error`             | Increment `no_progress_count`. If >= 3 → exit with circuit breaker. Otherwise wait 60s and loop.                                                                  |

### Fix Available Decision Logic

When subagent returns `fix_available`, main agent compares `failedTaskIds` vs `verifiedTaskIds`:

#### Step 1: Categorize Tasks

1. **Verified tasks** = tasks in both `failedTaskIds` AND `verifiedTaskIds`
2. **Unverified tasks** = tasks in `failedTaskIds` but NOT in `verifiedTaskIds`
3. **E2E tasks** = unverified tasks where target contains "e2e" (task format: `<project>:<target>` or `<project>:<target>:<config>`)
4. **Verifiable tasks** = unverified tasks that are NOT e2e

#### Step 2: Determine Path

| Condition                               | Path                                     |
| --------------------------------------- | ---------------------------------------- |
| No unverified tasks (all verified)      | Apply via MCP                            |
| Unverified tasks exist, but ALL are e2e | Apply via MCP (treat as verified enough) |
| Verifiable tasks exist                  | Local verification flow                  |

#### Step 3a: Apply via MCP (fully/e2e-only verified)

- Call `update_self_healing_fix({ shortLink, action: "APPLY" })`
- Record `last_cipe_url`, spawn subagent in wait mode

#### Step 3b: Local Verification Flow

When verifiable (non-e2e) unverified tasks exist:

1. **Detect package manager:**
   - `pnpm-lock.yaml` exists → `pnpm nx`
   - `yarn.lock` exists → `yarn nx`
   - Otherwise → `npx nx`

2. **Run verifiable tasks in parallel:**
   - Spawn `general` subagents to run each task concurrently
   - Each subagent runs: `<pm> nx run <taskId>`
   - Collect pass/fail results from all subagents

3. **Evaluate results:**

| Result                    | Action                       |
| ------------------------- | ---------------------------- |
| ALL verifiable tasks pass | Apply via MCP                |
| ANY verifiable task fails | Apply-locally + enhance flow |

1. **Apply-locally + enhance flow:**
   - Run `nx apply-locally <shortLink>`
   - Enhance the code to fix failing tasks
   - Run failing tasks again to verify fix
   - If still failing → increment `local_verify_count`, loop back to enhance
   - If passing → commit and push, record `expected_commit_sha`, spawn subagent in wait mode

2. **Track attempts** (wraps step 4):
   - Increment `local_verify_count` after each enhance cycle
   - If `local_verify_count >= local_verify_attempts` (default: 3):
     - Get code in commit-able state
     - Commit and push with message indicating local verification failed
     - Report to user:

       ```
       [ci-monitor] Local verification failed after <N> attempts. Pushed to CI for final validation. Failed: <taskIds>
       ```

     - Record `expected_commit_sha`, spawn subagent in wait mode (let CI be final judge)

#### Commit Message Format

```bash
git commit -m "fix(<projects>): <brief description>

Failed tasks: <taskId1>, <taskId2>
Local verification: passed|enhanced|failed-pushing-to-ci"
```

### Unverified Fix Flow (No Verification Attempted)

When `verificationStatus` is `FAILED`, `NOT_EXECUTABLE`, or fix has `couldAutoApplyTasks != true` with no verification:

- Analyze fix content (`suggestedFix`, `suggestedFixReasoning`, `taskOutputSummary`)
- If fix looks correct → apply via MCP
- If fix needs enhancement → use Apply Locally + Enhance Flow above
- If fix is wrong → reject via MCP, fix from scratch, commit, push

### Auto-Apply Eligibility

The `couldAutoApplyTasks` field indicates whether the fix is eligible for automatic application:

- **`true`**: Fix is eligible for auto-apply. Subagent keeps polling while verification is in progress. Returns `fix_auto_applying` when verified, or `fix_available` if verification fails.
- **`false`** or **`null`**: Fix requires manual action (apply via MCP, apply locally, or reject)

**Key point**: When subagent returns `fix_auto_applying`, do NOT call MCP to apply - self-healing handles it. Just spawn a new subagent in wait mode.

### Apply vs Reject vs Apply Locally

- **Apply via MCP**: Calls `update_self_healing_fix({ shortLink, action: "APPLY" })`. Self-healing agent applies the fix in CI and a new CIPE spawns automatically. No local git operations needed.
- **Apply Locally**: Runs `nx apply-locally <shortLink>`. Applies the patch to your local working directory and sets state to `APPLIED_LOCALLY`. Use this when you want to enhance the fix before pushing.
- **Reject via MCP**: Calls `update_self_healing_fix({ shortLink, action: "REJECT" })`. Marks fix as rejected. Use only when the fix is completely wrong and you'll fix from scratch.

### Apply Locally + Enhance Flow

When the fix needs enhancement (use `nx apply-locally`, NOT reject):

1. Apply the patch locally: `nx apply-locally <shortLink>` (this also updates state to `APPLIED_LOCALLY`)
2. Make additional changes as needed
3. Commit and push:

   ```bash
   git add -A
   git commit -m "fix: resolve <failedTaskIds>"
   git push origin $(git branch --show-current)
   ```

4. Loop to poll for new CIPE

### Reject + Fix From Scratch Flow

When the fix is completely wrong:

1. Call MCP to reject: `update_self_healing_fix({ shortLink, action: "REJECT" })`
2. Fix the issue from scratch locally
3. Commit and push:

   ```bash
   git add -A
   git commit -m "fix: resolve <failedTaskIds>"
   git push origin $(git branch --show-current)
   ```

4. Loop to poll for new CIPE

### Environment Issue Handling

When `failureClassification == 'ENVIRONMENT_STATE'`:

1. Call MCP to request rerun: `update_self_healing_fix({ shortLink, action: "RERUN_ENVIRONMENT_STATE" })`
2. New CIPE spawns automatically (no local git operations needed)
3. Loop to poll for new CIPE with `previousCipeUrl` set

### No-New-CIPE Handling

When `status == 'no_new_cipe'`:

This means the expected CIPE was never created - CI likely failed before Nx tasks could run.

1. **Report to user:**

   ```
   [ci-monitor] No CI attempt for <sha> after 10 min. Check CI provider for pre-Nx failures (install, checkout, auth). Last CI attempt: <previousCipeUrl>
   ```

2. **If user configured auto-fix attempts** (e.g., `--auto-fix-workflow`):
   - Detect package manager: check for `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
   - Run install to update lockfile:

     ```bash
     pnpm install   # or npm install / yarn install
     ```

   - If lockfile changed:

     ```bash
     git add pnpm-lock.yaml  # or appropriate lockfile
     git commit -m "chore: update lockfile"
     git push origin $(git branch --show-current)
     ```

   - Record new commit SHA, loop to poll with `expectedCommitSha`

3. **Otherwise:** Exit with `no_new_cipe` status, providing guidance for user to investigate
