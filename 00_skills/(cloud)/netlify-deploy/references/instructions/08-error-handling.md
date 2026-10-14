<!-- Package: 00_skills/(cloud)/netlify-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Error Handling

Common issues and solutions:

**"Not logged in"**
→ Run `npx netlify login`

**"No site linked"**
→ Run `npx netlify link` or `npx netlify init`

**"Build failed"**
→ Check build command and publish directory in netlify.toml or CLI prompts
→ Verify dependencies are installed
→ Review build logs for specific errors

**"Publish directory not found"**
→ Verify build command ran successfully
→ Check publish directory path is correct
