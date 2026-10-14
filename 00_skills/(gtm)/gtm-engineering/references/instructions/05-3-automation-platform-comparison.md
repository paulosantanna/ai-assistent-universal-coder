<!-- Package: 00_skills/(gtm)/gtm-engineering; relative command/resource examples resolve from that package or workspace root. -->

## 3. Automation Platform Comparison

Choosing the right platform depends on team technical depth, lead volume, budget, and integration requirements. No single tool wins across all dimensions.

### n8n vs Make vs Zapier: Detailed Comparison

| Dimension | n8n | Make (Integromat) | Zapier |
|---|---|---|---|
| **Architecture** | Self-hosted or cloud, node-based | Cloud-native, visual scenario builder | Cloud-native, trigger-action model |
| **Technical depth required** | Medium-High (JSON, expressions, code nodes) | Medium (visual data mapping, some formulas) | Low (point-and-click, templates) |
| **AI/LLM integration** | Best-in-class: 70+ AI nodes, LangChain native | Good: HTTP module + AI modules | Good: built-in AI actions, ChatGPT plugin |
| **Self-hosting** | Yes (Docker, Kubernetes) | No | No |
| **Pricing model** | Execution-based (self-host: free/paid tiers) | Operation-based (per data operation) | Task-based (per trigger + action) |
| **Price at 10K ops/month** | ~$20-50 (self-hosted) or ~$50 (cloud) | ~$30-60 | ~$100-200 |
| **Price at 100K ops/month** | ~$50-100 (self-hosted) or ~$200 (cloud) | ~$150-300 | ~$500-1,500+ |
| **Max integrations** | 400+ (plus HTTP/webhook for anything) | 1,500+ | 7,000+ |
| **Error handling** | Native retry, error workflows, manual replay | Built-in retry, error routes, break modules | Basic retry, error paths on paid plans |
| **Version control** | JSON export, Git-friendly | Scenario export (JSON) | Limited (no native Git support) |
| **Data sovereignty** | Full control (self-hosted) | EU/US cloud regions | US cloud (enterprise: custom) |
| **Branching/routing** | If/Switch nodes, merge nodes | Routers, filters, iterators | Paths (paid), Filters |
| **Code execution** | JavaScript, Python nodes built-in | JavaScript in some modules | Limited (Code by Zapier, basic JS/Python) |
| **Webhook support** | Full (trigger + respond) | Full (trigger + respond) | Full (trigger + respond) |
| **Best for GTM** | Complex multi-step AI workflows, data pipelines | Visual workflow design, moderate complexity | Simple integrations, non-technical teams |

### Enterprise iPaaS: Tray.io vs Workato

For larger organizations with complex integration needs, enterprise iPaaS platforms provide governance, compliance, and scale.

| Dimension | Tray.io | Workato |
|---|---|---|
| **Target** | Mid-market to enterprise | Enterprise |
| **Pricing** | Custom (typically $10K+/year) | Custom (typically $10K+/year) |
| **Strength** | Low-code visual builder for "citizen developers" | Enterprise-grade governance + AI copilots |
| **Integrations** | 600+ connectors | 1,000+ connectors |
| **AI features** | Merlin AI for building workflows | Copilot suite for building, mapping, documenting |
| **Compliance** | SOC2, GDPR, HIPAA | SOC2, GDPR, HIPAA, FedRAMP |
| **GTM use** | Marketing ops, sales ops, RevOps automation | Full GTM + finance + HR + IT automation |
| **When to choose** | Teams that need enterprise features but want accessible building | Organizations requiring full audit trails and enterprise compliance |

### Platform Selection Decision Tree

```
START: What is your team's technical depth?
  |
  +-- Can write Python/JS, comfortable with APIs
  |     |
  |     +-- Need data sovereignty / self-hosting?
  |     |     +-- YES --> n8n (self-hosted)
  |     |     +-- NO --> Need enterprise compliance?
  |     |           +-- YES --> Workato or Tray.io
  |     |           +-- NO --> n8n (cloud) or Make
  |     |
  |     +-- Volume > 100K operations/month?
  |           +-- YES --> n8n (self-hosted) for cost efficiency
  |           +-- NO --> n8n (cloud) or Make
  |
  +-- Can do basic configuration, formulas, some JSON
  |     |
  |     +-- Complex branching/data transformation needed?
  |     |     +-- YES --> Make
  |     |     +-- NO --> Zapier or Make
  |     |
  |     +-- Budget-constrained?
  |           +-- YES --> Make (better price-to-value)
  |           +-- NO --> Zapier (fastest setup)
  |
  +-- Non-technical, needs point-and-click
        |
        +-- Simple trigger-action automations?
        |     +-- YES --> Zapier
        |     +-- NO (complex needs) --> Hire a GTM engineer
        |
        +-- Need templates to start fast?
              +-- YES --> Zapier (7,000+ integrations, templates)
              +-- NO --> Make (better long-term value)
```

---


For API-first stack design, data pipelines, GTM agents, event-driven architecture, monitoring, cost optimization, patterns, and internal tools read `references/implementation-guide.md`.
