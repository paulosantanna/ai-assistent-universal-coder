<!-- Package: 00_skills/(cloud)/render-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Prerequisites for Direct Creation

**Repository must be pushed to a Git provider.** Render clones your repository to build and deploy services.

```bash
git remote -v  # Verify remote exists
git push origin main  # Ensure code is pushed
```

Supported providers: GitHub, GitLab, Bitbucket

If no remote exists, stop and ask the user to create/push a remote or switch to Docker image deploy.

**Note:** MCP does not support creating image-backed services. Use the Dashboard/API for prebuilt Docker image deploys.
