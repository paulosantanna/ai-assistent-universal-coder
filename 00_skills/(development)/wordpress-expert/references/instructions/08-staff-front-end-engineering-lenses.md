<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Staff Front-End Engineering lenses

Use internal lenses, never subagents:

- `wordpress-architecture`: hooks, lifecycle, REST, capabilities, plugin/theme boundaries;
- `staff-frontend`: semantic HTML, CSS architecture, JS, responsive behavior, design systems, performance;
- `gutenberg-blocks`: blocks, patterns, templates, Site Editor, theme.json;
- `classic-theme`: template hierarchy, child themes, functions.php, enqueueing;
- `plugin-engineering`: **complete plugin universe** — every installed regular/must-use/file plugin, hooks, settings, CPTs, REST endpoints, activation/uninstall;
- `clean-code-maintainability`: bounded responsibilities, readable names, small coherent units, collision-safe namespaces/prefixes, thin bootstrap code and supportable file structure;
- `ai-assisted-engineering`: project context, explicit instructions, documentation grounding, incremental generation, diff review and evidence-backed verification;
- `accessibility`: WCAG-oriented keyboard/focus/contrast/semantics/ARIA validation;
- `wordpress-security`: capabilities, nonce, validation, sanitization, escaping, upload safety;
- `wordpress-performance`: asset budgets, image strategy, caching, query cost, Core Web Vitals considerations;
- `external-integrations`: APIs, deep links, payments, marketplaces, social links, webhooks and brand assets;
- `production-operations`: backup, staging, deploy, cache purge, smoke, rollback and incident recovery.

Before medium/high-risk mutation ask: **Would a Staff Front-End/WordPress Engineer implement this change this way in production, considering WordPress extension points, clean code, accessibility, performance, security, rollback and maintainability?**
