<!-- Package: 00_skills/(monitoring)/sentry; relative command/resource examples resolve from that package or workspace root. -->

## API requirements

Always use these endpoints (GET only):

- List issues: `/api/0/projects/{org_slug}/{project_slug}/issues/`
- Issue detail: `/api/0/issues/{issue_id}/`
- Events for issue: `/api/0/issues/{issue_id}/events/`
- Event detail: `/api/0/projects/{org_slug}/{project_slug}/events/{event_id}/`
