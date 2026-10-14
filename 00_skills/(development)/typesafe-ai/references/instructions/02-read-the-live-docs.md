<!-- Package: 00_skills/(development)/typesafe-ai; relative command/resource examples resolve from that package or workspace root. -->

## Read the live docs

**The live TypeSafe docs are the source of truth. Read them as part of the task.**
This skill gives direction; the docs carry current concepts, prompting guidance,
API contracts, SDK usage, models, limits, and worked examples.

- Start with the [documentation index](https://docs.typesafe.ai/llms.txt) to discover
  relevant pages and cookbooks. Use targeted reads rather than loading the entire site.
- Mintlify serves Markdown by appending `.md` to a page path, for example
  [how to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md).
  Follow links from the index; convert extensionless documentation page links to
  `.md` when useful. Resolve relative links against `https://docs.typesafe.ai`.
- Before writing an integration, read the current API or chosen SDK page and the
  question guidance relevant to the design. For a new workflow, also inspect the
  closest cookbook: it often shows a better decomposition than a generic classifier.
- If the index is unavailable, use the direct links below or the site's navigation.
  If Markdown fetching fails, try the normal page. If live access is unavailable,
  use available local docs or installed SDK types, state that limitation, and avoid
  inventing version-dependent details.

| Task | Start here; follow the relevant details |
| --- | --- |
| Understand the programming model | [System One](https://docs.typesafe.ai/concepts/system-one.md), [building guide](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md) |
| Explore what to build | [Use-case map](https://docs.typesafe.ai/concepts/use-case-map.md), then relevant cookbooks from the index |
| Prepare inputs and questions | [State](https://docs.typesafe.ai/concepts/state.md), [primitives](https://docs.typesafe.ai/primitives.md), then the chosen primitive's page |
| Decide how to handle uncertainty | [Confidence](https://docs.typesafe.ai/confidence.md) |
| Write API code | [HTTP API](https://docs.typesafe.ai/api.md), [Python SDK](https://docs.typesafe.ai/sdk/python.md), or [JavaScript SDK](https://docs.typesafe.ai/sdk/javascript.md) |
| Update an older integration | [Migration guide](https://docs.typesafe.ai/migrating-to-v1.md) and the installed SDK's current reference |
