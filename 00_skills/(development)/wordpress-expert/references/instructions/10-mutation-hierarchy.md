<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Mutation hierarchy

Prefer in order:

1. existing plugin/theme/site-editor supported configuration;
2. block/pattern/template/theme.json changes;
3. child theme or site-specific plugin;
4. custom plugin/block using documented hooks/APIs;
5. direct database/file mutation only when no safer supported path exists and rollback is proven.

Never edit WordPress core for feature work.
