<!-- Package: 00_skills/(tooling)/social-media-operator; relative command/resource examples resolve from that package or workspace root. -->

## Quality Gates
- Session must validate before operations
- All mutations require `approved=true`, `change_id`, `rollback_ref`
- Visual verification via browser MCP for publishing operations
- Cookie expiry respected - session dies when platform logs out
- Max 30-day session lifetime regardless of cookie expiry
