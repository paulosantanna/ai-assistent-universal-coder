<!-- Package: 00_skills/(quality)/tlc-generative-engine-optimization; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

| Symptom                                              | Likely cause                                                             | Fix                                                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Rich Results Test shows no schema                    | JSON-LD is in a JS-rendered `<script>` tag loaded after DOMContentLoaded | Move JSON-LD to a static `<script type="application/ld+json">` in server-rendered HTML |
| Schema validation error: "required property missing" | `datePublished`, `author`, or `headline` absent                          | Add all required fields; check Schema.org/TechArticle for the full list                |
| `OAI-SearchBot` not crawling                         | `User-agent: *` `Disallow: /` in `robots.txt` blocks all bots            | Add explicit `Allow: /` for `OAI-SearchBot` above the wildcard rule                    |
| `llms.txt` not picked up by agents                   | File not at `https://example.com/llms.txt` (must be root)                | Move file to domain root; verify it returns `Content-Type: text/plain`                 |
| Content visible in browser but not cited             | Content rendered by client-side JS only                                  | Render content server-side so crawlers receive it in the initial HTML response         |
