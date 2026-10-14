<!-- Package: 00_skills/(gtm)/gtm-engineering; relative command/resource examples resolve from that package or workspace root. -->

## 2. Architecture Over Tools

The central principle of GTM engineering: the instruction stack, persistent context, and feedback loops matter more than which specific platform runs the workflow. Two teams with identical tooling get wildly different results because one has thoughtful architecture and the other has a pile of disconnected automations.

### The Instruction Stack

Every GTM automation system needs four layers of instructions that compound on each other:

```
+-----------------------------------------------------------+
|  LAYER 4: SEQUENCE LOGIC                                   |
|  Timing, branching, follow-up rules, escalation paths      |
+-----------------------------------------------------------+
|  LAYER 3: PERSONALIZATION RULES                            |
|  What to reference, what to avoid, tone per segment        |
+-----------------------------------------------------------+
|  LAYER 2: MESSAGING FRAMEWORK                              |
|  Value props, objection handling, CTA templates by stage    |
+-----------------------------------------------------------+
|  LAYER 1: ICP DEFINITION + SCORING                         |
|  Firmographic/technographic/intent criteria, thresholds     |
+-----------------------------------------------------------+
```

**Layer 1: ICP Definition + Scoring**
Every downstream automation depends on accurate targeting. Define who you sell to with scored criteria, not loose descriptions. This layer feeds routing, personalization, and sequence decisions.

- Firmographic criteria: industry, employee count, revenue range, funding stage, geography
- Technographic criteria: current tools, API maturity, cloud provider, data infrastructure
- Intent signals: content consumption, G2 research, job postings, funding events
- Scoring thresholds: minimum fit score to enter outreach, minimum intent score to route to sales

**Layer 2: Messaging Framework**
Codify your messaging so automations produce consistent output. Store this as structured data, not scattered documents.

- Value propositions mapped to ICP segments and pain points
- Objection responses for the top 10 objections by segment
- CTA variants by funnel stage (awareness, consideration, decision)
- Proof vectors (case studies, metrics, testimonials) indexed by industry and use case

**Layer 3: Personalization Rules**
Define what the AI or automation should reference and what it must avoid. Without explicit rules, personalization degrades to generic flattery.

- Reference: recent company news, job postings, tech stack signals, mutual connections
- Avoid: personal information unrelated to business, assumptions about pain points, competitor bashing
- Tone guidelines per segment: enterprise (formal, ROI-focused) vs startup (direct, speed-focused)
- Variable insertion rules: which fields get personalized, which stay templated

**Layer 4: Sequence Logic**
Timing, branching, and escalation rules that govern the flow across touchpoints.

- Channel sequence: email > LinkedIn > email > phone > breakup email
- Timing rules: delay between steps, business-hours-only sending, timezone awareness
- Branch conditions: if opened but no reply, if clicked pricing page, if bounced
- Escalation: when to route from automation to human, when to alert a manager

### Persistent Context

Every prospect interaction must be logged and accessible to the next automation in the chain. Without persistent context, each touchpoint starts from zero.

**Implementation pattern:**

```
Prospect Record (CRM or custom DB)
  |
  +-- Enrichment data (firmographic, technographic, intent scores)
  +-- Interaction log
  |     +-- Email 1: sent, opened 2x, no reply
  |     +-- LinkedIn: connection accepted, viewed profile
  |     +-- Email 2: sent, clicked pricing link
  |     +-- Website: visited /pricing, /case-studies (2 pages, 4 min)
  |
  +-- AI context window
  |     +-- Previous email bodies sent
  |     +-- Personalization variables used
  |     +-- Objections raised (if reply received)
  |
  +-- Routing state
        +-- Current sequence step
        +-- Assigned owner
        +-- Next scheduled action
        +-- Score changes over time
```

### Feedback Loops

The system must learn from outcomes. Without feedback loops, automations repeat the same mistakes at scale.

| Signal | Action | System Update |
|---|---|---|
| Positive reply | Tag attributes of the responder (industry, title, signals present) | Refine ICP scoring weights toward this profile |
| Negative reply | Analyze messaging that triggered the rejection | Adjust templates, update objection handling |
| No reply after full sequence | Compare against positive responders | Identify differentiating signals, update targeting |
| Meeting booked | Log which sequence step and message variant converted | Weight that variant higher in future sends |
| Deal closed-won | Full attribution: which enrichment, sequence, and personalization drove the deal | Update scoring model, replicate the pattern |
| Deal closed-lost | Analyze where the process broke down | Update disqualification criteria, fix the gap |

### Architecture vs Tools: Decision Framework

| Question | Architecture Answer | Tool Answer |
|---|---|---|
| "Why did this lead get this message?" | Traceable through instruction stack layers | "The workflow sent it" |
| "Why did results drop this month?" | Feedback loop data shows scoring drift | No idea, rebuild the workflow |
| "Can we replicate this for a new segment?" | Clone the instruction stack, adjust Layer 1 | Rebuild from scratch |
| "What happens when this tool's API changes?" | Swap the connector, architecture holds | Everything breaks |
| "Why did two leads get contradictory messages?" | Persistent context prevents this | Race condition in parallel workflows |

---
