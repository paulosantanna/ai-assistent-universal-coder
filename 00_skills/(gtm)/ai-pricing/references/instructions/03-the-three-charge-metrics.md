<!-- Package: 00_skills/(gtm)/ai-pricing; relative command/resource examples resolve from that package or workspace root. -->

## The Three Charge Metrics

Every AI pricing decision starts with choosing your charge metric. This is the unit of value you bill for. Get this wrong and everything downstream breaks.

| Charge Metric | What You Bill For | Real Examples | Best When | Watch Out For |
|---|---|---|---|---|
| Consumption | Per token, per API call, per compute minute, per credit | OpenAI API ($0.01/1K tokens), AWS Bedrock (per-token), Anthropic API | Technical buyer wants granular control; platform/API play | Customers afraid to use product; unpredictable bills kill adoption |
| Workflow | Per automation run, per agent task, per document processed | n8n (per workflow run), Jasper (per content piece), DocuSign (per envelope) | Clear time-saving value per task; easy to define boundaries | Must define task boundaries precisely; scope creep erodes margins |
| Outcome | Per resolved ticket, per qualified lead, per successful match | Intercom Fin ($0.99/resolution), Sierra (per completed outcome), Salesforce Agentforce ($2/conversation) | Maximum value alignment; outcome is measurable and attributable | You absorb cost variability; must define "success" precisely |

### Decision Framework: Picking Your Charge Metric

```
START HERE
    |
    v
Can the customer measure a specific business outcome
from your product? (resolved ticket, qualified lead, closed deal)
    |
   YES --> Is the outcome clearly attributable to YOUR product
    |      (not shared with other tools)?
    |          |
    |         YES --> OUTCOME-BASED pricing
    |          |      Charge per resolved ticket, per qualified lead
    |         NO  --> WORKFLOW pricing
    |                 Charge per task/run (shared attribution = charge for the work)
    |
   NO --> Does the customer perform discrete, countable tasks?
    |      (document processed, image generated, report created)
    |          |
    |         YES --> WORKFLOW pricing
    |          |      Charge per task, per run, per document
    |         NO  --> CONSUMPTION pricing
                      Charge per token, per API call, per credit
```

### Credit Systems: The Abstraction Layer

Credits sit between raw consumption and the customer. They let you change underlying costs without repricing. 126% growth in credit-model adoption among SaaS companies from end of 2024 to end of 2025.

**How credits work in practice:**

| Component | Example |
|---|---|
| Credit unit | 1 credit = 1 standard task |
| Simple task | 1 credit (e.g., summarize email) |
| Medium task | 3 credits (e.g., draft response) |
| Complex task | 10 credits (e.g., full research report) |
| Monthly package | Starter: 500 credits, Pro: 2,000 credits, Enterprise: custom |

**When to use credits vs. direct metering:**

| Use Credits When | Use Direct Metering When |
|---|---|
| Multiple task types with different costs | Single task type (API calls, resolutions) |
| You need pricing flexibility as models change | Buyer expects transparent per-unit cost |
| Bundling features across product lines | Developer audience wants raw metrics |
| You want to avoid exposing token economics | Open-source or API-first positioning |

**Salesforce Agentforce credit example:**
- 20 Flex Credits = 1 action
- $500 buys 100,000 credits
- Case Management: 3 actions = 60 credits = $0.30 per case
- Field Service Scheduling: 6 actions = 120 credits = $0.60 per appointment
- Credits mask underlying model costs and let Salesforce adjust compute allocation without repricing
