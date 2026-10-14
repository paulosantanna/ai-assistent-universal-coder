<!-- Package: 00_skills/(quality)/tlc-generative-engine-optimization; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1 — Audit request

**User:** "Can you audit my blog for AI search visibility?"

**Actions:**

1. Check `robots.txt` → `OAI-SearchBot` is missing a `Disallow` but also missing an explicit `Allow` — confirm default is allow.
2. Validate JSON-LD on the homepage → `datePublished` is missing, `author` has no `url`.
3. Run pillar sweep → Trustworthy: partial (no author bio page); Quotable: fail (no FAQ schema on FAQ page).
4. Return findings table with three priority tiers.

**Result:** Prioritized list: fix `techarticle.jsonld`, add author bio, add `FAQPage` schema. Clear, actionable, no ranking promises.

### Example 2 — Create request

**User:** "Create a new GEO-optimized article page for my Next.js blog."

**Actions:**

1. Draft `<head>` from `templates/page-metadata.html`.
2. Generate `templates/techarticle.jsonld` filled with real title, author, dates.
3. Structure content using `templates/quotable-article-outline.md`: direct-answer intro, H2/H3 sections, sources list.
4. Confirm `robots.txt` allows `OAI-SearchBot`.
5. Run checklist — all eight items pass.

**Result:** Ready-to-deploy page with correct metadata, valid schema, and citation-ready prose.

### Example 3 — llms.txt request

**User:** "Write an llms.txt for my documentation site."

**Actions:**

1. Inventory the three or four most useful pages for an AI agent.
2. Apply `templates/llms.txt` format: H1 site name → blockquote description → `## Key pages` with Markdown links → optional `## Technical files`.
3. Remind the user that `llms.txt` is not a crawler-control file and doesn't guarantee citations.

**Result:** A concise, standards-compliant `llms.txt` with honest caveats.
