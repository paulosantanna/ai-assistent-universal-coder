<!-- Package: 00_skills/(quality)/tlc-generative-engine-optimization; relative command/resource examples resolve from that package or workspace root. -->

## Operating Modes

### Mode 1 — Create (new GEO-ready page)

1. Plan page structure: one topic, one H1, question-based H2s/H3s.
2. Apply `templates/page-metadata.html` (canonical, hreflang, meta description).
3. Add `templates/techarticle.jsonld` (or `faqpage.jsonld` for FAQ pages).
4. Write content in the quotable outline pattern (`templates/quotable-article-outline.md`): short direct answer → supporting detail → sources.
5. Update `robots.txt` to allow AI crawlers (`templates/robots-ai-crawlers.txt`).
6. Add or update `llms.txt` if the site wants to guide AI agents (`templates/llms.txt`).
7. Run the GEO page checklist (in `references/pillars-and-workflow.md`).

### Mode 2 — Audit (score an existing page or site)

1. Crawl check: read `robots.txt` — are `OAI-SearchBot` and `BingBot` allowed?
2. Structured data: validate all JSON-LD against the Rich Results Test and Schema Markup Validator.
3. Pillar sweep: for each of the six pillars, mark pass / partial / fail.
4. Produce a **prioritized findings table** (Pillar → Finding → Severity → Fix).
5. Identify quick wins (metadata, schema, robots) vs. content rewrites.

### Mode 3 — Improve (apply fixes)

1. Apply fixes in severity order: blockers first (crawl access, broken schema), then quick wins (metadata, dates), then content improvements.
2. Re-validate structured data after every schema change.
3. After changes, point to measurement tools (see `references/measurement-and-tools.md`) so the user can track AI visibility over time.
