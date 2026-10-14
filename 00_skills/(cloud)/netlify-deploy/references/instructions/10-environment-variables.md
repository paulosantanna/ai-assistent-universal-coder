<!-- Package: 00_skills/(cloud)/netlify-deploy; relative command/resource examples resolve from that package or workspace root. -->

## Environment Variables

For secrets and configuration:

1. Never commit secrets to Git
2. Set in Netlify dashboard: Site Settings → Environment Variables
3. Access in builds via `process.env.VARIABLE_NAME`
