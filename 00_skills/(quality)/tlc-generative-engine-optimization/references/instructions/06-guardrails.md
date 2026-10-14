<!-- Package: 00_skills/(quality)/tlc-generative-engine-optimization; relative command/resource examples resolve from that package or workspace root. -->

## Guardrails

- **Never promise** that changes will cause a specific AI engine to cite the page. Citation is an engine decision.
- **Structured data must match visible page content exactly.** Mismatches violate Google's policies and can suppress the page.
- **`llms.txt` is optional.** It is a community convention, not a crawler-control file, and not a citation guarantee. Recommend it only when the site wants to guide AI agent navigation.
- **`robots.txt` is the only authoritative crawler-control file.** `llms.txt` has no effect on crawling.
- **Do not add `noindex` or `Disallow` for AI crawlers** unless the user explicitly wants to block AI indexing.
- Prefer primary platform documentation (Google Search Central, Bing Webmaster Tools, Schema.org) over third-party summaries.
